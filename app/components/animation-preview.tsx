'use client'

import { motion } from 'framer-motion'
import { Download, Play, Image as ImageIcon } from 'lucide-react'

interface AnimationPreviewProps {
  uploadedImage: string | null
  animationUrl: string | null
  isProcessing: boolean
}

export default function AnimationPreview({ 
  uploadedImage, 
  animationUrl, 
  isProcessing 
}: AnimationPreviewProps) {
  if (!uploadedImage) {
    return (
      <div className="glass-effect rounded-2xl p-8 text-center">
        <ImageIcon className="w-16 h-16 mx-auto mb-4 text-gray-400" />
        <h3 className="text-xl font-bold mb-2">Preview Area</h3>
        <p className="text-gray-400">
          Upload a painting to see the preview and generated animation
        </p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Original Image Preview */}
      <div className="glass-effect rounded-2xl p-6">
        <h3 className="text-xl font-bold mb-4">Original Painting</h3>
        <div className="relative">
          <img
            src={uploadedImage}
            alt="Original painting"
            className="w-full h-48 object-cover rounded-xl"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent rounded-xl" />
          <div className="absolute bottom-3 left-3 text-white">
            <p className="font-medium">Your Masterpiece</p>
            <p className="text-sm opacity-80">Ready for transformation</p>
          </div>
        </div>
      </div>

      {/* Animation Preview */}
      <div className="glass-effect rounded-2xl p-6">
        <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
          <Play className="w-5 h-5 text-primary-400" />
          Generated Animation
        </h3>
        
        {isProcessing ? (
          <div className="text-center py-12">
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
              className="w-16 h-16 border-4 border-primary-400 border-t-transparent rounded-full mx-auto mb-4"
            />
            <p className="text-lg font-medium mb-2">Creating Your Animation</p>
            <p className="text-gray-400 text-sm">
              Converting painting to 200,000+ particles...
            </p>
          </div>
        ) : animationUrl ? (
          <div className="space-y-4">
            <div className="relative">
              <img
                src={animationUrl}
                alt="Generated animation"
                className="w-full h-48 object-cover rounded-xl"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent rounded-xl" />
              <div className="absolute bottom-3 left-3 text-white">
                <p className="font-medium">Particle Animation</p>
                <p className="text-sm opacity-80">Ready for download</p>
              </div>
            </div>
            
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className="w-full bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 text-white font-bold py-3 px-6 rounded-xl transition-all duration-300 flex items-center justify-center gap-2"
            >
              <Download className="w-5 h-5" />
              Download Animation
            </motion.button>
            
            <div className="text-center text-sm text-gray-400">
              <p>✨ 200,000+ particles • 3D motion • HD quality</p>
            </div>
          </div>
        ) : (
          <div className="text-center py-12">
            <div className="w-16 h-16 bg-primary-400/20 rounded-full mx-auto mb-4 flex items-center justify-center">
              <Play className="w-8 h-8 text-primary-400" />
            </div>
            <p className="text-lg font-medium mb-2">Ready to Generate</p>
            <p className="text-gray-400 text-sm">
              Click the generate button to create your particle animation
            </p>
          </div>
        )}
      </div>
    </div>
  )
}
