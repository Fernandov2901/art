# 🎨 Particle Painting Animator

Transform your paintings into magical particle animations that dissolve and reconstruct! This web application allows users to upload paintings and generate stunning particle animations with over 200,000 particles in 3D space.

## ✨ Features

- **200,000+ Tiny Particles**: Every pixel becomes a particle for maximum detail
- **3D Flying Motion**: Particles fly around in realistic 3D space
- **Perfect Reconstruction**: Animation ends with the complete painting clearly visible
- **Ultra-HD Quality**: High-resolution output with smooth animations
- **Beautiful Web Interface**: Modern, responsive design with animations
- **Drag & Drop Upload**: Easy image upload with preview

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm
- Python 3.8+ with virtual environment
- Required Python packages: `numpy`, `PIL` (Pillow)

### Installation

1. **Clone and setup the project:**
   ```bash
   cd painting2
   ```

2. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

3. **Setup Python environment:**
   ```bash
   # Create virtual environment
   python3 -m venv painting_env
   
   # Activate virtual environment
   source painting_env/bin/activate  # On macOS/Linux
   # or
   .\painting_env\Scripts\activate  # On Windows
   
   # Install Python dependencies
   pip install numpy Pillow
   ```

4. **Start the development server:**
   ```bash
   npm run dev
   ```

5. **Open your browser:**
   Navigate to [http://localhost:3000](http://localhost:3000)

## 🎯 How It Works

1. **Upload**: Drag & drop your painting image (JPEG, PNG, GIF, BMP)
2. **Generate**: Click the generate button to create the particle animation
3. **Download**: Download your magical creation as an animated GIF
4. **Share**: Share the wonder with others!

## 🔧 Technical Details

### Frontend
- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first CSS framework
- **Framer Motion**: Smooth animations and transitions
- **React Dropzone**: Drag & drop file uploads

### Backend
- **Next.js API Routes**: Server-side API endpoints
- **Python Integration**: Executes particle animation scripts
- **File Processing**: Handles image uploads and GIF generation

### Animation Engine
- **Particle System**: Converts images to individual particles
- **3D Physics**: Realistic particle movement in 3D space
- **Animation Phases**: Explosion → Floating → Reconstruction
- **HD Output**: High-quality animated GIFs

## 📁 Project Structure

```
painting2/
├── app/                          # Next.js app directory
│   ├── components/               # React components
│   │   ├── image-uploader.tsx   # Image upload component
│   │   ├── animation-preview.tsx # Animation preview
│   │   └── processing-status.tsx # Processing status
│   ├── api/                      # API routes
│   │   └── generate-animation/   # Animation generation API
│   ├── globals.css               # Global styles
│   ├── layout.tsx                # Root layout
│   └── page.tsx                  # Main page
├── public/                       # Static files
│   └── animations/               # Generated animations
├── uploads/                      # Temporary uploads
├── perfect_final_painting.py     # Python animation script
├── package.json                  # Node.js dependencies
├── tailwind.config.js            # Tailwind configuration
└── README.md                     # This file
```

## 🎨 Animation Process

1. **Image Analysis**: Analyzes the uploaded painting
2. **Particle Creation**: Converts every pixel to a particle
3. **Explosion Phase**: Particles fly away from original positions
4. **Floating Phase**: Particles drift in 3D space with orbital motion
5. **Reconstruction**: Particles return to exact original positions
6. **Final Display**: Perfect painting reconstruction with enhanced clarity

## 🌟 Usage Examples

### Basic Usage
1. Open the web application
2. Upload a painting image
3. Click "Generate Particle Animation"
4. Wait for processing to complete
5. Download your animation

### Supported Formats
- **Input**: JPEG, PNG, GIF, BMP (Max: 10MB)
- **Output**: Animated GIF with 200,000+ particles

## 🔍 Troubleshooting

### Common Issues

**Python not found:**
- Ensure Python virtual environment is activated
- Check Python path in the API route

**Dependencies missing:**
- Run `pip install numpy Pillow` in the virtual environment
- Ensure all Node.js packages are installed with `npm install`

**Permission errors:**
- Check file permissions for uploads and animations directories
- Ensure Python script has execute permissions

### Performance Tips

- Use images under 10MB for faster processing
- Close other applications during animation generation
- Ensure adequate disk space for temporary files

## 🚀 Deployment

### Production Build
```bash
npm run build
npm start
```

### Environment Variables
- No additional environment variables required
- Ensure Python environment is available in production

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Built with Next.js and React
- Particle animation engine in Python
- Beautiful UI with Tailwind CSS and Framer Motion

---

**Happy animating! 🎨✨**
