import React, { useState, useRef } from 'react';
import { Upload, Image as ImageIcon, X, Loader2 } from 'lucide-react';

const ImageUpload = ({ onUpload, loading, disabled }) => {
  const [dragActive, setDragActive] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const fileInputRef = useRef(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleFile = (file) => {
    if (!file.type.startsWith('image/')) {
      alert('Please select an image file');
      return;
    }

    if (file.size > 10 * 1024 * 1024) { // 10MB limit
      alert('File size must be less than 10MB');
      return;
    }

    setSelectedFile(file);
    
    // Create preview
    const reader = new FileReader();
    reader.onload = (e) => setPreview(e.target.result);
    reader.readAsDataURL(file);
  };

  const handleFileInput = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  const handleUpload = () => {
    if (selectedFile) {
      onUpload(selectedFile);
    }
  };

  const handleClear = () => {
    setSelectedFile(null);
    setPreview(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const openFileDialog = () => {
    fileInputRef.current?.click();
  };

  return (
    <div className="upload-container">
      <h2>Upload ID Card Image</h2>
      <p className="upload-description">
        Upload an image of Vietnamese ID card (CCCD/CMND) to extract text information
      </p>

      <div
        className={`upload-area ${dragActive ? 'drag-active' : ''} ${disabled ? 'disabled' : ''}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onClick={openFileDialog}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept="image/*"
          onChange={handleFileInput}
          style={{ display: 'none' }}
          disabled={disabled}
        />

        {preview ? (
          <div className="preview-container">
            <img src={preview} alt="Preview" className="preview-image" />
            <button 
              className="clear-btn"
              onClick={(e) => {
                e.stopPropagation();
                handleClear();
              }}
            >
              <X size={20} />
            </button>
          </div>
        ) : (
          <div className="upload-placeholder">
            <Upload size={48} />
            <p>Drag and drop an image here, or click to select</p>
            <p className="file-types">Supports: JPG, PNG, BMP, TIFF</p>
          </div>
        )}
      </div>

      {selectedFile && (
        <div className="file-info">
          <div className="file-details">
            <ImageIcon size={20} />
            <span>{selectedFile.name}</span>
            <span className="file-size">
              {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
            </span>
          </div>
        </div>
      )}

      <div className="upload-actions">
        <button
          className="upload-btn"
          onClick={handleUpload}
          disabled={!selectedFile || loading || disabled}
        >
          {loading ? (
            <>
              <Loader2 className="spinner" />
              Processing...
            </>
          ) : (
            'Extract Text'
          )}
        </button>
      </div>
    </div>
  );
};

export default ImageUpload;

