'use client';

import { motion } from 'framer-motion';
import { Download, Image as ImageIcon } from 'lucide-react';

interface AnimationPreviewProps {
  originalImage: string;
  animationUrl: string;
  isProcessing: boolean;
}

export default function AnimationPreview({ originalImage, animationUrl, isProcessing }: AnimationPreviewProps) {
  if (!originalImage) {
    return (
      <div className="glass-effect rounded-2xl p-8 text-center">
        <ImageIcon className="w-16 h-16 text-gray-400 mx-auto mb-4" />
        <h3 className="text-xl font-semibold text-gray-300 mb-2">No Image Selected</h3>
        <p className="text-gray-400">Upload a painting to see the preview here</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Original Image */}
      <div className="glass-effect rounded-2xl p-6">
        <h3 className="text-xl font-semibold text-white mb-4 flex items-center gap-2">
          <ImageIcon className="w-5 h-5" />
          Original Painting
        </h3>
        <div className="relative">
          <img
            src={originalImage}
            alt="Original painting"
            className="w-full h-auto rounded-lg shadow-lg"
          />
        </div>
      </div>

      {/* Animation Preview */}
      {isProcessing && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="glass-effect rounded-2xl p-6"
        >
          <h3 className="text-xl font-semibold text-white mb-4">
            🎭 Generating Animation...
          </h3>
          <div className="flex items-center justify-center py-8">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-400"></div>
          </div>
          <p className="text-center text-gray-300">
            Creating your magical particle animation...
          </p>
        </motion.div>
      )}

      {/* Generated Animation */}
      {animationUrl && !isProcessing && (
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="glass-effect rounded-2xl p-6"
        >
          <h3 className="text-xl font-semibold text-white mb-4">
            ✨ Your Particle Animation
          </h3>
          <div className="relative">
            <img
              src={animationUrl}
              alt="Generated particle animation"
              className="w-full h-auto rounded-lg shadow-lg"
            />
            <div className="absolute top-4 right-4">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="bg-purple-600 hover:bg-purple-700 text-white p-3 rounded-full shadow-lg transition-colors"
                onClick={() => {
                  const link = document.createElement('a');
                  link.href = animationUrl;
                  link.download = 'particle-animation.png';
                  link.click();
                }}
              >
                <Download className="w-5 h-5" />
              </motion.button>
            </div>
          </div>
          <p className="text-center text-gray-300 mt-4">
            🎉 Your animation is ready! Click the download button to save it.
          </p>
        </motion.div>
      )}

      {/* Instructions */}
      {!isProcessing && !animationUrl && originalImage && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="glass-effect rounded-2xl p-6"
        >
          <h3 className="text-xl font-semibold text-white mb-4">
            🚀 Ready to Animate!
          </h3>
          <div className="space-y-3 text-gray-300">
            <p>• Your painting is ready for transformation</p>
            <p>• Click "Generate Particle Animation" to start</p>
            <p>• Watch as it becomes thousands of flying particles</p>
            <p>• See the magic of perfect reconstruction!</p>
          </div>
        </motion.div>
      )}
    </div>
  );
}
