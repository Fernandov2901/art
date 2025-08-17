'use client'

import { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { motion } from 'framer-motion'
import { Upload, Image as ImageIcon, X } from 'lucide-react'

interface ImageUploaderProps {
  onImageUpload: (imageUrl: string, file?: File) => void
}

export default function ImageUploader({ onImageUpload }: ImageUploaderProps) {
  const [preview, setPreview] = useState<string | null>(null)
  const [dragActive, setDragActive] = useState(false)

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const file = acceptedFiles[0]
    if (file) {
      const reader = new FileReader()
      reader.onload = (e) => {
        const result = e.target?.result as string
        setPreview(result)
        onImageUpload(result, file)
      }
      reader.readAsDataURL(file)
    }
  }, [onImageUpload])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.gif', '.bmp']
    },
    multiple: false,
    maxSize: 10 * 1024 * 1024 // 10MB
  })

  const removeImage = () => {
    setPreview(null)
    onImageUpload('')
  }

  return (
    <div className="glass-effect rounded-2xl p-6">
      <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
        <ImageIcon className="w-6 h-6 text-primary-400" />
        Upload Your Painting
      </h2>
      
      {!preview ? (
        <div
          {...getRootProps()}
          className={`border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-all duration-300 ${
            isDragActive || dragActive
              ? 'border-primary-400 bg-primary-400/10'
              : 'border-gray-600 hover:border-primary-400 hover:bg-primary-400/5'
          }`}
          onDragEnter={() => setDragActive(true)}
          onDragLeave={() => setDragActive(false)}
        >
          <input {...getInputProps()} />
          <motion.div
            animate={{ scale: isDragActive ? 1.05 : 1 }}
            transition={{ duration: 0.2 }}
          >
            <Upload className="w-16 h-16 mx-auto mb-4 text-gray-400" />
            <p className="text-lg font-medium mb-2">
              {isDragActive ? 'Drop your painting here!' : 'Drag & drop your painting'}
            </p>
            <p className="text-gray-400 mb-4">
              or click to browse files
            </p>
            <p className="text-sm text-gray-500">
              Supports: JPEG, PNG, GIF, BMP (Max: 10MB)
            </p>
          </motion.div>
        </div>
      ) : (
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="relative"
        >
          <img
            src={preview}
            alt="Uploaded painting"
            className="w-full h-64 object-cover rounded-xl"
          />
          <button
            onClick={removeImage}
            className="absolute top-2 right-2 bg-red-500 hover:bg-red-600 text-white rounded-full p-2 transition-colors duration-200"
          >
            <X className="w-5 h-5" />
          </button>
          <div className="mt-4 text-center">
            <p className="text-green-400 font-medium">✓ Painting uploaded successfully!</p>
            <p className="text-sm text-gray-400 mt-1">Ready to generate animation</p>
          </div>
        </motion.div>
      )}
    </div>
  )
}
