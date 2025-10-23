import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 seconds timeout
});

// OCR API functions
export const ocrAPI = {
  // Upload image and detect text
  detectText: async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await api.post('/detect', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    return response.data;
  },

  // Health check
  healthCheck: async () => {
    const response = await api.get('/health');
    return response.data;
  },

  // Get service info
  getServiceInfo: async () => {
    const response = await api.get('/info');
    return response.data;
  }
};

export default api;

