'use client';

import { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { motion } from 'framer-motion';
import { Upload, X, Image as ImageIcon } from 'lucide-react';

interface ImageUploaderProps {
  onImageUpload: (file: File, dataUrl: string) => void;
}

export default function ImageUploader({ onImageUpload }: ImageUploaderProps) {
  const [preview, setPreview] = useState<string | null>(null);
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (file) {
      setUploadedFile(file);
      
      // Create preview URL
      const reader = new FileReader();
      reader.onload = (e) => {
        const dataUrl = e.target?.result as string;
        setPreview(dataUrl);
        onImageUpload(file, dataUrl);
      };
      reader.readAsDataURL(file);
    }
  }, [onImageUpload]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.gif', '.bmp', '.webp']
    },
    multiple: false,
    maxSize: 10 * 1024 * 1024 // 10MB
  });

  const removeImage = () => {
    setPreview(null);
    setUploadedFile(null);
    // Reset the parent state by calling onImageUpload with empty values
    onImageUpload({} as File, '');
  };

  return (
    <div className="space-y-4">
      {!preview ? (
        <motion.div
          {...getRootProps()}
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          className={`glass-effect rounded-2xl p-8 text-center cursor-pointer transition-all duration-300 ${
            isDragActive ? 'border-2 border-purple-400 bg-purple-900/20' : ''
          }`}
        >
          <input {...getInputProps()} />
          
          <div className="space-y-4">
            <div className="flex justify-center">
              <div className="w-20 h-20 bg-gradient-to-br from-purple-500 to-blue-600 rounded-full flex items-center justify-center">
                <Upload className="w-10 h-10 text-white" />
              </div>
            </div>
            
            <div>
              <h3 className="text-xl font-semibold text-white mb-2">
                {isDragActive ? 'Drop your painting here!' : 'Upload Your Painting'}
              </h3>
              <p className="text-gray-300">
                {isDragActive 
                  ? 'Release to upload' 
                  : 'Drag & drop an image, or click to browse'
                }
              </p>
            </div>
            
            <div className="text-sm text-gray-400">
              <p>Supports: JPEG, PNG, GIF, BMP, WebP</p>
              <p>Max size: 10MB</p>
            </div>
          </div>
        </motion.div>
      ) : (
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="glass-effect rounded-2xl p-6"
        >
          <div className="relative">
            <img
              src={preview}
              alt="Uploaded painting"
              className="w-full h-auto rounded-lg shadow-lg"
            />
            
            <button
              onClick={removeImage}
              className="absolute top-2 right-2 bg-red-500 hover:bg-red-600 text-white p-2 rounded-full shadow-lg transition-colors"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
          
          <div className="mt-4 text-center">
            <div className="flex items-center justify-center gap-2 text-green-400 mb-2">
              <ImageIcon className="w-5 h-5" />
              <span className="font-medium">Image uploaded successfully!</span>
            </div>
            <p className="text-sm text-gray-300">
              {uploadedFile?.name} ({(uploadedFile?.size / 1024 / 1024).toFixed(2)} MB)
            </p>
          </div>
        </motion.div>
      )}
    </div>
  );
}
