import React from 'react';
import { FileText, Server } from 'lucide-react';

const Header = ({ serviceStatus }) => {
  const getStatusColor = (status) => {
    switch (status) {
      case 'healthy': return '#10b981';
      case 'unhealthy': return '#ef4444';
      default: return '#6b7280';
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'healthy': return 'Online';
      case 'unhealthy': return 'Offline';
      default: return 'Unknown';
    }
  };

  return (
    <header className="header">
      <div className="container">
        <div className="header-content">
          <div className="logo">
            <FileText className="logo-icon" />
            <h1>Vietnamese OCR Service</h1>
          </div>
          
          <div className="service-status">
            <Server className="status-icon" />
            <span 
              className="status-text"
              style={{ color: getStatusColor(serviceStatus?.status) }}
            >
              {getStatusText(serviceStatus?.status)}
            </span>
            {serviceStatus?.models_loaded && (
              <span className="models-loaded">Models Loaded</span>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;

