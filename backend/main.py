import os
import base64
import logging
import asyncio
from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
# pyrefly: ignore [missing-import]
import asyncpg
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv 

load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Config
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/dpdp")
JWT_SECRET = os.getenv("JWT_SECRET", "supersecret_dpdp_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Global DB pool
pool = None

async def cleanup_old_images():
    """Background task to delete images older than 15 minutes."""
    while True:
        try:
            await asyncio.sleep(300) # Run every 5 minutes
            if pool:
                async with pool.acquire() as conn:
                    # Delete records older than 15 minutes
                    result = await conn.execute(
                        "DELETE FROM images WHERE uploaded_at < NOW() - INTERVAL '15 minutes'"
                    )
                    deleted_count = int(result.split(" ")[-1]) if result.startswith("DELETE") else 0
                    if deleted_count > 0:
                        logger.info(f"Cleanup: Deleted {deleted_count} abandoned images.")
        except asyncio.CancelledError:
            logger.info("Cleanup task cancelled.")
            break
        except Exception as e:
            logger.error(f"Error in cleanup_old_images task: {e}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    global pool
    logger.info("Connecting to database...")
    pool = await asyncpg.create_pool(dsn=DATABASE_URL)
    
    # Init DB schema
    async with pool.acquire() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                user_id VARCHAR(100) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL
            );
        """)
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS images (
                id SERIAL PRIMARY KEY,
                user_id VARCHAR(100) NOT NULL,
                original_name VARCHAR(255) NOT NULL,
                filename VARCHAR(255) NOT NULL,
                image_data TEXT NOT NULL,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        # Sync initial users
        initial_users = [
            {'userId': 'E1001', 'password': 'Password123!'},
            {'userId': 'E1002', 'password': 'Password123!'},
            {'userId': 'E1003', 'password': 'Password123!'},
            {'userId': 'sanoj', 'password': 'sib123'},
            {'userId': 'admin', 'password': 'admin'},
            {'userId': 'Shaun', 'password': 'Sha123#'}
        ]
        for u in initial_users:
            hashed = pwd_context.hash(u['password'])
            await conn.execute("""
                INSERT INTO users (user_id, password_hash) 
                VALUES ($1, $2)
                ON CONFLICT (user_id) DO UPDATE SET password_hash = EXCLUDED.password_hash
            """, u['userId'], hashed)
        logger.info("Synced initial users.")
    
    # Start the background cleanup task
    cleanup_task = asyncio.create_task(cleanup_old_images())
    
    yield
    
    # Cancel the background cleanup task on shutdown
    cleanup_task.cancel()
    
    logger.info("Closing database connection...")
    await pool.close()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginRequest(BaseModel):
    userId: str
    password: str

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)

async def get_current_user(request: Request):
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token")
    token = token.split(" ")[1]
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        user_id: str = payload.get("userId")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except JWTError:
        raise HTTPException(status_code=403, detail="Could not validate credentials")

@app.post("/api/login")
async def login(req: LoginRequest):
    async with pool.acquire() as conn:
        user = await conn.fetchrow("SELECT * FROM users WHERE user_id = $1", req.userId)
        if not user or not pwd_context.verify(req.password, user['password_hash']):
            raise HTTPException(status_code=401, detail="Invalid User ID or password")
        
        access_token = create_access_token(
            data={"userId": user['user_id']},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        return {"message": "Login successful", "token": access_token}

@app.post("/api/upload")
async def upload_images(images: List[UploadFile] = File(...), user_id: str = Depends(get_current_user)):
    if not images:
        raise HTTPException(status_code=400, detail="No files uploaded.")
    
    image_ids = []
    async with pool.acquire() as conn:
        async with conn.transaction():
            for file in images:
                content = await file.read()
                b64_data = base64.b64encode(content).decode('utf-8')
                mime_type = file.content_type or "image/jpeg"
                data_uri = f"data:{mime_type};base64,{b64_data}"
                
                filename = f"{file.filename.split('.')[0]}_{int(datetime.utcnow().timestamp())}.{file.filename.split('.')[-1]}"
                
                inserted_id = await conn.fetchval(
                    "INSERT INTO images (user_id, original_name, filename, image_data) VALUES ($1, $2, $3, $4) RETURNING id",
                    user_id, file.filename, filename, data_uri
                )
                image_ids.append(inserted_id)
    return {"message": f"Successfully uploaded {len(images)} images.", "image_ids": image_ids}

@app.get("/api/images")
async def get_images(ids: str = None, user_id: str = Depends(get_current_user)):
    async with pool.acquire() as conn:
        if ids:
            id_list = [int(i) for i in ids.split(",")]
            records = await conn.fetch(
                "SELECT id, original_name, image_data, uploaded_at FROM images WHERE user_id = $1 AND id = ANY($2) ORDER BY uploaded_at DESC",
                user_id, id_list
            )
        else:
            records = await conn.fetch(
                "SELECT id, original_name, image_data, uploaded_at FROM images WHERE user_id = $1 ORDER BY uploaded_at DESC",
                user_id
            )
        return [
            {
                "id": r["id"],
                "name": r["original_name"],
                "data": r["image_data"],
                "uploaded_at": r["uploaded_at"].isoformat()
            }
            for r in records
        ]

@app.delete("/api/images/{image_id}")
async def delete_image(image_id: int, user_id: str = Depends(get_current_user)):
    async with pool.acquire() as conn:
        result = await conn.execute(
            "DELETE FROM images WHERE id = $1 AND user_id = $2", image_id, user_id
        )
        if result == "DELETE 0":
            raise HTTPException(status_code=404, detail="Image not found or unauthorized")
        return {"message": "Image deleted successfully"}
