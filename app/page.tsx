'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { Sparkles, Upload, Download, Wand2, Palette, Zap, Star } from 'lucide-react'
import ImageUploader from './components/image-uploader'
import AnimationPreview from './components/animation-preview'
import ProcessingStatus from './components/processing-status'

export default function Home() {
  const [uploadedImage, setUploadedImage] = useState<string | null>(null)
  const [uploadedFile, setUploadedFile] = useState<File | null>(null)
  const [isProcessing, setIsProcessing] = useState(false)
  const [animationUrl, setAnimationUrl] = useState<string | null>(null)
  const [processingProgress, setProcessingProgress] = useState(0)
  const [error, setError] = useState<string | null>(null)

  const handleImageUpload = (imageUrl: string, file?: File) => {
    setUploadedImage(imageUrl)
    setUploadedFile(file || null)
    setAnimationUrl(null)
    setError(null)
  }

  const handleGenerateAnimation = async () => {
    if (!uploadedFile) return
    
    setIsProcessing(true)
    setProcessingProgress(0)
    setError(null)
    
    try {
      // Create form data
      const formData = new FormData()
      formData.append('image', uploadedFile)
      
      // Simulate progress updates
      const progressInterval = setInterval(() => {
        setProcessingProgress(prev => {
          if (prev >= 90) {
            clearInterval(progressInterval)
            return 90
          }
          return prev + 10
        })
      }, 800)
      
      // Make API call
      const response = await fetch('/api/generate-animation', {
        method: 'POST',
        body: formData,
      })
      
      clearInterval(progressInterval)
      
      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.error || 'Failed to generate animation')
      }
      
      const data = await response.json()
      setProcessingProgress(100)
      
      // Wait a bit to show 100% progress
      setTimeout(() => {
        setIsProcessing(false)
        setAnimationUrl(data.animationUrl)
      }, 1000)
      
    } catch (err) {
      console.error('Error generating animation:', err)
      setError(err instanceof Error ? err.message : 'Failed to generate animation')
      setIsProcessing(false)
      setProcessingProgress(0)
    }
  }

  return (
    <div className="min-h-screen particle-bg">
      {/* Header */}
      <header className="relative z-10">
        <div className="container mx-auto px-4 py-8">
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center"
          >
            <div className="flex items-center justify-center gap-3 mb-4">
              <Sparkles className="w-8 h-8 text-primary-400 animate-glow" />
              <h1 className="text-4xl md:text-6xl font-bold gradient-text">
                Particle Painting Animator
              </h1>
              <Sparkles className="w-8 h-8 text-primary-400 animate-glow" />
            </div>
            <p className="text-xl md:text-2xl text-gray-300 max-w-3xl mx-auto">
              Transform your paintings into magical particle animations that dissolve and reconstruct
            </p>
          </motion.div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 pb-16">
        <div className="grid lg:grid-cols-2 gap-8 max-w-7xl mx-auto">
          {/* Left Column - Upload & Controls */}
          <motion.div
            initial={{ opacity: 0, x: -50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="space-y-8"
          >
            {/* Features */}
            <div className="glass-effect rounded-2xl p-6">
              <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
                <Wand2 className="w-6 h-6 text-primary-400" />
                Magical Features
              </h2>
              <div className="space-y-3">
                <div className="flex items-center gap-3">
                  <Star className="w-5 h-5 text-yellow-400" />
                  <span>200,000+ tiny particles</span>
                </div>
                <div className="flex items-center gap-3">
                  <Star className="w-5 h-5 text-yellow-400" />
                  <span>3D flying motion</span>
                </div>
                <div className="flex items-center gap-3">
                  <Star className="w-5 h-5 text-yellow-400" />
                  <span>Perfect reconstruction</span>
                </div>
                <div className="flex items-center gap-3">
                  <Star className="w-5 h-5 text-yellow-400" />
                  <span>Ultra-HD quality</span>
                </div>
              </div>
            </div>

            {/* Image Upload */}
            <ImageUploader onImageUpload={handleImageUpload} />

            {/* Error Display */}
            {error && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="bg-red-500/20 border border-red-500/30 rounded-xl p-4"
              >
                <p className="text-red-400 text-center font-medium">
                  ❌ {error}
                </p>
              </motion.div>
            )}

            {/* Generate Button */}
            {uploadedImage && (
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.5 }}
              >
                <button
                  onClick={handleGenerateAnimation}
                  disabled={isProcessing}
                  className="w-full bg-gradient-to-r from-primary-500 to-purple-600 hover:from-primary-600 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed text-white font-bold py-4 px-8 rounded-2xl text-xl transition-all duration-300 transform hover:scale-105 active:scale-95 flex items-center justify-center gap-3"
                >
                  {isProcessing ? (
                    <>
                      <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-white"></div>
                      Creating Magic...
                    </>
                  ) : (
                    <>
                      <Zap className="w-6 h-6" />
                      Generate Particle Animation
                    </>
                  )}
                </button>
              </motion.div>
            )}

            {/* Processing Status */}
            {isProcessing && (
              <ProcessingStatus progress={processingProgress} />
            )}
          </motion.div>

          {/* Right Column - Preview & Results */}
          <motion.div
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, delay: 0.4 }}
            className="space-y-8"
          >
            {/* Animation Preview */}
            <AnimationPreview
              uploadedImage={uploadedImage}
              animationUrl={animationUrl}
              isProcessing={isProcessing}
            />

            {/* How It Works */}
            <div className="glass-effect rounded-2xl p-6">
              <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
                <Palette className="w-5 h-5 text-primary-400" />
                How It Works
              </h3>
              <div className="space-y-3 text-sm text-gray-300">
                <p>1. <strong>Upload</strong> your painting image</p>
                <p>2. <strong>Generate</strong> the particle animation</p>
                <p>3. <strong>Download</strong> your magical creation</p>
                <p>4. <strong>Share</strong> the wonder with others!</p>
              </div>
            </div>
          </motion.div>
        </div>
      </main>

      {/* Floating Particles Background */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden">
        {[...Array(20)].map((_, i) => (
          <motion.div
            key={i}
            className="absolute w-2 h-2 bg-primary-400/30 rounded-full"
            animate={{
              x: [0, 100, 0],
              y: [0, -100, 0],
              opacity: [0.3, 0.8, 0.3],
            }}
            transition={{
              duration: 8 + i * 0.5,
              repeat: Infinity,
              delay: i * 0.2,
            }}
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
            }}
          />
        ))}
      </div>
    </div>
  )
}
