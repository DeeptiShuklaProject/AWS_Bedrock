import React, { useState, useEffect } from 'react';
import { X, ZoomIn, ZoomOut, RotateCcw, Download, Maximize2 } from 'lucide-react';

const ImageViewerModal = ({ src, alt, onClose }) => {
  const [scale, setScale] = useState(1);

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [onClose]);

  if (!src) return null;

  return (
    <div 
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-md p-4 animate-fade-in"
      onClick={onClose}
    >
      <div 
        className="relative max-w-5xl w-full bg-[var(--bg-panel)] border border-[var(--border-color)] rounded-2xl overflow-hidden shadow-2xl flex flex-col max-h-[90vh]"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Modal Toolbar */}
        <div className="flex items-center justify-between px-5 py-3 border-b border-[var(--border-color)] bg-[var(--bg-sidebar)]">
          <div className="flex items-center gap-2 truncate pr-4">
            <Maximize2 size={16} className="text-cyan-400 shrink-0" />
            <span className="text-xs font-semibold text-[var(--text-primary)] truncate">
              {alt || 'Image Preview'}
            </span>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => setScale(prev => Math.min(prev + 0.25, 2.5))}
              className="p-1.5 rounded-lg bg-[var(--bg-panel)] border border-[var(--border-color)] text-[var(--text-secondary)] hover:text-white hover:border-indigo-500/40 transition-colors"
              title="Zoom In"
            >
              <ZoomIn size={16} />
            </button>
            <button
              onClick={() => setScale(prev => Math.max(prev - 0.25, 0.5))}
              className="p-1.5 rounded-lg bg-[var(--bg-panel)] border border-[var(--border-color)] text-[var(--text-secondary)] hover:text-white hover:border-indigo-500/40 transition-colors"
              title="Zoom Out"
            >
              <ZoomOut size={16} />
            </button>
            <button
              onClick={() => setScale(1)}
              className="p-1.5 rounded-lg bg-[var(--bg-panel)] border border-[var(--border-color)] text-[var(--text-secondary)] hover:text-white hover:border-indigo-500/40 transition-colors"
              title="Reset Zoom"
            >
              <RotateCcw size={16} />
            </button>
            <a
              href={src}
              target="_blank"
              rel="noopener noreferrer"
              download
              className="p-1.5 rounded-lg bg-[var(--bg-panel)] border border-[var(--border-color)] text-[var(--text-secondary)] hover:text-white hover:border-indigo-500/40 transition-colors"
              title="Open Original Image"
            >
              <Download size={16} />
            </a>
            <button
              onClick={onClose}
              className="p-1.5 rounded-lg bg-red-500/20 border border-red-500/30 text-red-400 hover:bg-red-500/30 transition-colors ml-2"
              title="Close (Esc)"
            >
              <X size={18} />
            </button>
          </div>
        </div>

        {/* Modal Image Area */}
        <div className="flex-1 overflow-auto p-6 flex items-center justify-center bg-[#090d16]">
          <img
            src={src}
            alt={alt || 'Documentation screenshot'}
            style={{ transform: `scale(${scale})`, transition: 'transform 0.2s ease-out' }}
            className="max-w-full max-h-[70vh] object-contain rounded-xl border border-[var(--border-color)] shadow-xl"
          />
        </div>

        {/* Caption */}
        {alt && (
          <div className="px-5 py-2.5 bg-[var(--bg-sidebar)] border-t border-[var(--border-color)] text-center text-xs text-[var(--text-secondary)]">
            Caption: <span className="text-[var(--text-primary)] italic">{alt}</span>
          </div>
        )}
      </div>
    </div>
  );
};

export default ImageViewerModal;
