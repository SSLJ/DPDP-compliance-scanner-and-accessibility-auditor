import React from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import LoginPage from './LoginPage'
import UploadPage from './UploadPage'
import SelectionPage from './SelectionPage'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/upload" element={<UploadPage />} />
        <Route path="/select" element={<SelectionPage />} />
      </Routes>
    </BrowserRouter>
  )
}
