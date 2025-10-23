import React, { useState } from 'react';
import { FileText, Clock, CheckCircle, RotateCcw, Copy, Download } from 'lucide-react';

const ResultsDisplay = ({ results, onReset }) => {
  const [copiedText, setCopiedText] = useState('');

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    setCopiedText(text);
    setTimeout(() => setCopiedText(''), 2000);
  };

  const downloadResults = () => {
    const dataStr = JSON.stringify(results, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'ocr-results.json';
    link.click();
    URL.revokeObjectURL(url);
  };

  const formatText = (text) => {
    return text || 'No text detected';
  };

  const getClassDisplayName = (className) => {
    const classNames = {
      'name': 'Họ và tên',
      'id': 'Số CMND/CCCD',
      'dob': 'Ngày sinh',
      'gender': 'Giới tính',
      'nationality': 'Quốc tịch',
      'current_place1': 'Nơi thường trú (1)',
      'current_place2': 'Nơi thường trú (2)',
      'origin_place1': 'Quê quán (1)',
      'origin_place2': 'Quê quán (2)',
      'expire_date': 'Ngày hết hạn',
      'issue_date': 'Ngày cấp',
      'personal_identifi': 'Thông tin cá nhân'
    };
    return classNames[className] || className;
  };

  return (
    <div className="results-container">
      <div className="results-header">
        <h2>
          <FileText className="results-icon" />
          OCR Results
        </h2>
        <div className="results-actions">
          <button 
            className="action-btn secondary"
            onClick={downloadResults}
            title="Download JSON"
          >
            <Download size={16} />
          </button>
          <button 
            className="action-btn secondary"
            onClick={onReset}
            title="Upload New Image"
          >
            <RotateCcw size={16} />
          </button>
        </div>
      </div>

      <div className="results-stats">
        <div className="stat-item">
          <CheckCircle className="stat-icon" />
          <span>{results.detected_texts?.length || 0} texts detected</span>
        </div>
        <div className="stat-item">
          <Clock className="stat-icon" />
          <span>Processing time: {results.timing?.total_time?.toFixed(3)}s</span>
        </div>
      </div>

      <div className="results-content">
        {results.detected_texts?.length > 0 ? (
          <div className="text-results">
            {results.detected_texts.map((text, index) => (
              <div key={index} className="text-item">
                <div className="text-header">
                  <h4>{getClassDisplayName(text.class_name)}</h4>
                  <div className="text-meta">
                    <span className="confidence">
                      Confidence: {(text.confidence * 100).toFixed(1)}%
                    </span>
                    <button
                      className="copy-btn"
                      onClick={() => copyToClipboard(text.extracted_text)}
                      title="Copy text"
                    >
                      <Copy size={14} />
                      {copiedText === text.extracted_text ? 'Copied!' : 'Copy'}
                    </button>
                  </div>
                </div>
                <div className="text-content">
                  <p>{formatText(text.extracted_text)}</p>
                </div>
                <div className="text-bbox">
                  <small>
                    Position: ({text.bbox.x1}, {text.bbox.y1}) - ({text.bbox.x2}, {text.bbox.y2})
                  </small>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="no-results">
            <p>No text detected in the image</p>
          </div>
        )}
      </div>

      {results.timing && (
        <div className="timing-info">
          <h4>Processing Details</h4>
          <div className="timing-grid">
            <div className="timing-item">
              <span>YOLO Detection:</span>
              <span>{results.timing.detection_time?.toFixed(3)}s</span>
            </div>
            <div className="timing-item">
              <span>OCR Processing:</span>
              <span>{results.timing.ocr_time?.toFixed(3)}s</span>
            </div>
            <div className="timing-item">
              <span>Total Time:</span>
              <span>{results.timing.total_time?.toFixed(3)}s</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ResultsDisplay;

