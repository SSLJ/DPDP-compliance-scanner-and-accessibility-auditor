import React, { useState, useRef } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

export default function UploadPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const [files, setFiles] = useState([]);
  const [dragActive, setDragActive] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const inputRef = useRef(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      validateAndAddFiles(Array.from(e.dataTransfer.files));
    }
  };

  const handleChange = (e) => {
    e.preventDefault();
    if (e.target.files && e.target.files.length > 0) {
      validateAndAddFiles(Array.from(e.target.files));
    }
  };

  const validateAndAddFiles = (selectedFiles) => {
    const validFiles = selectedFiles.filter(f => f.type === 'image/jpeg' || f.type === 'image/png');
    if (validFiles.length !== selectedFiles.length) {
      alert('Some files were ignored. Please only upload .png or .jpg image files.');
    }
    if (validFiles.length > 0) {
      setFiles(prev => [...prev, ...validFiles]);
    }
  };

  const removeFile = (indexToRemove) => {
    setFiles(files.filter((_, index) => index !== indexToRemove));
  };

  const handleContinue = async () => {
    if (files.length === 0) return;
    setIsUploading(true);

    const token = localStorage.getItem('token');
    if (!token) {
      alert('Authentication error. Please log in again.');
      navigate('/');
      return;
    }

    const formData = new FormData();
    files.forEach(file => formData.append('images', file));

    try {
      const response = await fetch('http://localhost:5000/api/upload', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        },
        body: formData
      });

      if (response.ok) {
        const data = await response.json();
        setIsUploading(false);
        const existingImageIds = location.state?.imageIds || [];
        const combinedImageIds = [...existingImageIds, ...data.image_ids];
        navigate('/select', { state: { imageIds: combinedImageIds } });
      } else {
        const errorData = await response.json();
        alert('Upload failed: ' + (errorData.error || 'Unknown error'));
        setIsUploading(false);
      }
    } catch (err) {
      console.error(err);
      alert('Network error connecting to the server.');
      setIsUploading(false);
    }
  };

  const triggerInput = () => {
    inputRef.current.click();
  };

  return (
    <>
      {/* SIBerNet Style Header */}
      <header className="w-full bg-sib-maroon flex-shrink-0 z-10 shadow-sm">
        <div className="max-w-[1200px] mx-auto flex items-center px-5" style={{ height: '90px' }}>
          <img
            src="/SIB_Logo.png"
            alt="South Indian Bank"
            className="w-auto object-contain cursor-pointer"
            style={{ height: '71.5px' }}
            onClick={() => navigate('/')}
            onError={e => { e.currentTarget.style.display = 'none' }}
          />
        </div>
      </header>

      {/* Main Upload Area */}
      <main className="flex-1 flex flex-col items-center justify-center px-4 py-12">
        <div className="w-full max-w-[700px] bg-white rounded-2xl shadow-card p-10 flex flex-col items-center">

          <div className="mb-8 text-center">
            <h1 className="text-[28px] font-display text-gray-900 font-semibold mb-2">Upload Source Document</h1>
            <p className="text-[14px] text-gray-500 font-normal">
              Please upload the document image (.jpg or .png) you wish to scan for DPDP compliance or accessibility auditing.
            </p>
          </div>

          <form
            className={`w-full border-2 border-dashed rounded-xl p-12 flex flex-col items-center justify-center transition-colors duration-200 cursor-pointer
              ${dragActive ? 'border-sib-maroon bg-red-50' : 'border-gray-300 bg-gray-50 hover:bg-gray-100'}`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
            onClick={triggerInput}
          >
            <input
              ref={inputRef}
              type="file"
              accept=".png, .jpg, .jpeg"
              multiple
              onChange={handleChange}
              className="hidden"
            />

            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" className="text-gray-400 mb-4">
              <path strokeLinecap="round" strokeLinejoin="round" d="M3 15v4c0 1.1.9 2 2 2h14a2 2 0 0 0 2-2v-4M17 8l-5-5-5 5M12 3v12" />
            </svg>

            <p className="text-gray-700 text-[15px] font-medium mb-1">
              Drag and drop your images here
            </p>
            <p className="text-gray-400 text-[13px]">
              or click to browse from your computer (select multiple)
            </p>

            {files.length > 0 && (
              <div className="mt-6 w-full max-w-[500px] flex flex-col gap-3 max-h-[200px] overflow-y-auto pr-2">
                {files.map((f, i) => (
                  <div key={i} className="p-3 bg-white rounded-lg shadow-sm border border-gray-200 flex items-center justify-between w-full">
                    <div className="flex items-center gap-3 overflow-hidden">
                      <div className="w-10 h-10 flex-shrink-0 rounded bg-red-50 flex items-center justify-center text-sib-maroon">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                          <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
                          <circle cx="8.5" cy="8.5" r="1.5" />
                          <polyline points="21 15 16 10 5 21" />
                        </svg>
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium text-gray-900 truncate" title={f.name}>{f.name}</p>
                        <p className="text-xs text-gray-500">{(f.size / 1024 / 1024).toFixed(2)} MB</p>
                      </div>
                    </div>
                    <button 
                      type="button"
                      onClick={(e) => { e.stopPropagation(); removeFile(i); }}
                      className="ml-2 text-gray-400 hover:text-red-500 transition-colors p-2 rounded-full hover:bg-gray-100"
                    >
                      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <line x1="18" y1="6" x2="6" y2="18"></line>
                        <line x1="6" y1="6" x2="18" y2="18"></line>
                      </svg>
                    </button>
                  </div>
                ))}
              </div>
            )}
          </form>

          <button
            onClick={handleContinue}
            disabled={files.length === 0 || isUploading}
            className={`btn-primary w-full max-w-[300px] h-[50px] rounded-lg text-white text-[14px] font-bold tracking-[0.06em] uppercase mt-10 transition-all duration-300
              ${files.length === 0 || isUploading ? 'opacity-50 cursor-not-allowed grayscale' : 'cursor-pointer hover:shadow-lg'}`}
          >
            {isUploading ? 'Uploading...' : `Upload ${files.length} Image${files.length !== 1 ? 's' : ''} & Continue`}
          </button>

        </div>
      </main>

      <footer className="w-full bg-[#2F2F2F] py-3 flex-shrink-0">
        <div className="max-w-[1200px] mx-auto px-5 flex items-center justify-between">
          <p className="text-white/35 text-[11px] font-medium">&copy; 2026 South Indian Bank. All rights reserved.</p>
        </div>
      </footer>
    </>
  );
}
