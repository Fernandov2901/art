'use client'

import { motion } from 'framer-motion'
import { Sparkles, Zap, Star } from 'lucide-react'

interface ProcessingStatusProps {
  progress: number
}

export default function ProcessingStatus({ progress }: ProcessingStatusProps) {
  const steps = [
    { name: 'Analyzing Painting', icon: Sparkles, progress: 25 },
    { name: 'Creating Particles', icon: Star, progress: 50 },
    { name: 'Generating 3D Motion', icon: Zap, progress: 75 },
    { name: 'Finalizing Animation', icon: Sparkles, progress: 100 }
  ]

  const currentStep = steps.find(step => progress <= step.progress) || steps[0]

  return (
    <div className="glass-effect rounded-2xl p-6">
      <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
        <Zap className="w-5 h-5 text-primary-400" />
        Creating Your Animation
      </h3>
      
      {/* Progress Bar */}
      <div className="mb-6">
        <div className="flex justify-between text-sm mb-2">
          <span>Progress</span>
          <span>{progress}%</span>
        </div>
        <div className="w-full bg-gray-700 rounded-full h-3">
          <motion.div
            className="bg-gradient-to-r from-primary-500 to-purple-600 h-3 rounded-full"
            initial={{ width: 0 }}
            animate={{ width: `${progress}%` }}
            transition={{ duration: 0.5, ease: "easeOut" }}
          />
        </div>
      </div>

      {/* Current Step */}
      <div className="text-center mb-4">
        <motion.div
          animate={{ scale: [1, 1.1, 1] }}
          transition={{ duration: 1, repeat: Infinity }}
          className="inline-block"
        >
          <currentStep.icon className="w-8 h-8 mx-auto mb-2 text-primary-400" />
        </motion.div>
        <p className="font-medium text-primary-300">{currentStep.name}</p>
      </div>

      {/* Step Indicators */}
      <div className="space-y-3">
        {steps.map((step, index) => (
          <div key={step.name} className="flex items-center gap-3">
            <div className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold ${
              progress >= step.progress 
                ? 'bg-green-500 text-white' 
                : 'bg-gray-600 text-gray-400'
            }`}>
              {progress >= step.progress ? '✓' : index + 1}
            </div>
            <span className={`text-sm ${
              progress >= step.progress ? 'text-green-400' : 'text-gray-400'
            }`}>
              {step.name}
            </span>
          </div>
        ))}
      </div>

      {/* Fun Facts */}
      <div className="mt-6 p-4 bg-primary-400/10 rounded-xl border border-primary-400/20">
        <p className="text-sm text-center text-primary-300">
          💫 Creating {Math.floor(200000 + Math.random() * 50000).toLocaleString()} particles...
        </p>
        <p className="text-xs text-center text-primary-400/70 mt-1">
          Each particle has its own 3D physics and movement!
        </p>
      </div>
    </div>
  )
}
