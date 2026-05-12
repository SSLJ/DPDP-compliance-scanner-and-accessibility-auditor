import React from 'react';
import { useNavigate } from 'react-router-dom';

export default function SelectionPage() {
  const navigate = useNavigate();

  return (
    <>
      {/* SIBerNet Style Header */}
      <header className="w-full bg-sib-maroon flex-shrink-0 z-10 shadow-sm">
        <div className="max-w-[1200px] mx-auto flex items-center px-5" style={{ height: '90px' }}>
          <img
            src="https://www.southindianbank.bank.in/images/logo.png"
            alt="South Indian Bank"
            className="w-auto object-contain cursor-pointer"
            style={{ height: '65px', filter: 'brightness(0) invert(1)' }}
            onClick={() => navigate('/')}
            onError={e => { e.currentTarget.style.display = 'none' }}
          />
        </div>
      </header>

      {/* Main Selection Area */}
      <main className="flex-1 flex flex-col items-center justify-center px-4 py-12 relative overflow-hidden">
        
        {/* Decorative background elements matching login page */}
        <div className="absolute top-[-10%] left-[-5%] w-[40vw] h-[40vw] rounded-full bg-red-50/50 blur-3xl z-0 pointer-events-none"></div>
        <div className="absolute bottom-[-10%] right-[-5%] w-[30vw] h-[30vw] rounded-full bg-gray-200/50 blur-3xl z-0 pointer-events-none"></div>

        <div className="relative z-10 w-full max-w-[1000px] flex flex-col items-center">
          
          <div className="mb-12 text-center stagger-l">
            <span className="inline-block px-4 py-1.5 rounded-full bg-red-50 text-sib-maroon text-[11px] font-bold tracking-widest uppercase mb-4 border border-red-100">
              Analysis Tools
            </span>
            <h1 className="text-[36px] font-display text-gray-900 font-bold mb-3 tracking-tight">Select an Audit Module</h1>
            <p className="text-[15px] text-gray-500 font-normal max-w-[500px] mx-auto leading-relaxed">
              Choose the analysis tool to run against your uploaded document. Our AI engines will process the image and generate a comprehensive report.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 w-full stagger-r">
            
            {/* DPDP Compliance Card */}
            <div className="group cursor-pointer bg-white rounded-2xl shadow-card hover:shadow-[0_20px_40px_rgba(176,30,35,0.08)] transition-all duration-300 border border-transparent hover:border-sib-maroon/20 overflow-hidden flex flex-col h-[320px]">
              <div className="h-2 w-full bg-gradient-to-r from-[#C8282E] to-[#8A1519]"></div>
              <div className="p-10 flex flex-col h-full">
                <div className="w-14 h-14 rounded-xl bg-red-50 flex items-center justify-center text-sib-maroon mb-6 group-hover:scale-110 transition-transform duration-300">
                  <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
                  </svg>
                </div>
                <h2 className="text-[22px] font-display font-bold text-gray-900 mb-3 group-hover:text-sib-maroon transition-colors duration-200">
                  DPDP Compliance Scanner
                </h2>
                <p className="text-[14px] text-gray-500 leading-relaxed mb-8 flex-1">
                  Scan the document for personally identifiable information (PII) and ensure it meets Digital Personal Data Protection Act requirements.
                </p>
                <div className="flex items-center text-sib-maroon font-semibold text-[13px] tracking-wide uppercase">
                  Launch Scanner
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="ml-2 group-hover:translate-x-1 transition-transform">
                    <path d="M5 12h14M12 5l7 7-7 7"/>
                  </svg>
                </div>
              </div>
            </div>

            {/* Accessibility Auditor Card */}
            <div className="group cursor-pointer bg-white rounded-2xl shadow-card hover:shadow-[0_20px_40px_rgba(176,30,35,0.08)] transition-all duration-300 border border-transparent hover:border-sib-maroon/20 overflow-hidden flex flex-col h-[320px]">
              <div className="h-2 w-full bg-gray-200 group-hover:bg-gradient-to-r group-hover:from-gray-400 group-hover:to-gray-600 transition-all duration-300"></div>
              <div className="p-10 flex flex-col h-full">
                <div className="w-14 h-14 rounded-xl bg-gray-50 flex items-center justify-center text-gray-600 mb-6 group-hover:scale-110 group-hover:bg-gray-100 transition-all duration-300">
                  <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <circle cx="12" cy="12" r="10"/>
                    <path d="M12 16v-4"/>
                    <path d="M12 8h.01"/>
                  </svg>
                </div>
                <h2 className="text-[22px] font-display font-bold text-gray-900 mb-3 group-hover:text-gray-700 transition-colors duration-200">
                  Accessibility Auditor
                </h2>
                <p className="text-[14px] text-gray-500 leading-relaxed mb-8 flex-1">
                  Analyze UI contrast ratios, font readability, structure, and spacing to ensure compliance with WCAG guidelines for banking interfaces.
                </p>
                <div className="flex items-center text-gray-600 font-semibold text-[13px] tracking-wide uppercase">
                  Launch Auditor
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="ml-2 group-hover:translate-x-1 transition-transform">
                    <path d="M5 12h14M12 5l7 7-7 7"/>
                  </svg>
                </div>
              </div>
            </div>

          </div>
        </div>
      </main>

      <footer className="w-full bg-[#2F2F2F] py-3 flex-shrink-0 relative z-10">
        <div className="max-w-[1200px] mx-auto px-5 flex items-center justify-between">
          <p className="text-white/35 text-[11px] font-medium">&copy; 2026 South Indian Bank. All rights reserved.</p>
        </div>
      </footer>
    </>
  );
}
