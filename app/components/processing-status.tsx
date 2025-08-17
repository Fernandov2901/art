'use client';

import { motion } from 'framer-motion';

export default function ProcessingStatus() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="glass-effect rounded-2xl p-6"
    >
      <h3 className="text-xl font-semibold text-white mb-4 text-center">
        🎭 Processing Your Painting
      </h3>
      
      <div className="space-y-4">
        <div className="flex items-center gap-3">
          <div className="w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>
          <span className="text-gray-300">Image uploaded successfully</span>
        </div>
        
        <div className="flex items-center gap-3">
          <div className="w-3 h-3 bg-blue-400 rounded-full animate-pulse"></div>
          <span className="text-gray-300">Analyzing painting structure</span>
        </div>
        
        <div className="flex items-center gap-3">
          <div className="w-3 h-3 bg-purple-400 rounded-full animate-pulse"></div>
          <span className="text-gray-300">Preparing particle system</span>
        </div>
        
        <div className="flex items-center gap-3">
          <div className="w-3 h-3 bg-yellow-400 rounded-full animate-pulse"></div>
          <span className="text-gray-300">Ready for animation generation</span>
        </div>
      </div>
      
      <div className="mt-6 p-4 bg-blue-900/30 rounded-lg">
        <p className="text-sm text-blue-200 text-center">
          💡 <strong>Fun Fact:</strong> Your painting will be transformed into thousands of tiny particles that will dance, float, and perfectly reconstruct back into the original artwork!
        </p>
      </div>
    </motion.div>
  );
}
