# Vietnamese OCR Frontend

React frontend application for the Vietnamese OCR Service.

## Features

- 🖼️ **Image Upload**: Drag & drop or click to upload ID card images
- 🔍 **Real-time OCR**: Extract text from Vietnamese ID cards (CCCD/CMND)
- 📊 **Results Display**: Show detected text with confidence scores
- 📱 **Responsive Design**: Works on desktop and mobile devices
- 🎨 **Modern UI**: Clean and intuitive user interface

## Supported Image Formats

- JPG/JPEG
- PNG
- BMP
- TIFF

## Getting Started

### Prerequisites

- Node.js 16+ 
- npm or yarn
- Backend OCR service running on http://localhost:8000

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

### Development Server

The frontend will be available at http://localhost:3000

The development server is configured to proxy API requests to the backend at http://localhost:8000.

## Usage

1. **Upload Image**: Drag and drop an ID card image or click to select
2. **Process**: Click "Extract Text" to process the image
3. **View Results**: See detected text with confidence scores and bounding boxes
4. **Copy/Download**: Copy individual text or download full results as JSON

## API Integration

The frontend connects to the backend OCR API:

- `POST /api/v1/detect` - Upload image and get OCR results
- `GET /api/v1/health` - Check service health
- `GET /api/v1/info` - Get service information

## Components

- **Header**: Shows service status and models loaded
- **ImageUpload**: Handles file upload with drag & drop
- **ResultsDisplay**: Shows OCR results with copy/download options

## Styling

The app uses custom CSS with:
- Modern gradient designs
- Responsive grid layouts
- Smooth animations and transitions
- Mobile-first approach

