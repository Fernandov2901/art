'use client';

import { useState } from 'react';
import ImageUploader from './components/image-uploader';
import AnimationPreview from './components/animation-preview';
import ProcessingStatus from './components/processing-status';
import ParticleAnimator from './components/particle-animator';

export default function Home() {
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [imageUrl, setImageUrl] = useState<string>('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [animationUrl, setAnimationUrl] = useState<string>('');
  const [error, setError] = useState<string>('');

  const handleImageUpload = (file: File, dataUrl: string) => {
    setUploadedFile(file);
    setImageUrl(dataUrl);
    setAnimationUrl('');
    setError('');
  };

  const handleAnimationComplete = (url: string) => {
    setAnimationUrl(url);
    setIsProcessing(false);
  };

  const handleGenerateAnimation = () => {
    if (!imageUrl) return;
    
    setIsProcessing(true);
    setError('');
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 p-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-white mb-4">
            <span className="gradient-text">Particle Painting</span>
            <br />
            <span className="text-3xl text-blue-200">Animator</span>
          </h1>
          <p className="text-xl text-blue-100 max-w-2xl mx-auto">
            Transform your paintings into mesmerizing particle animations that explode, float, and reconstruct into the original artwork.
          </p>
        </div>

        {/* Main Content */}
        <div className="grid lg:grid-cols-2 gap-8 mb-8">
          {/* Left Column - Upload & Processing */}
          <div className="space-y-6">
            <ImageUploader onImageUpload={handleImageUpload} />
            
            {imageUrl && (
              <div className="space-y-4">
                <button
                  onClick={handleGenerateAnimation}
                  disabled={isProcessing}
                  className="w-full bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition-all duration-300 transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isProcessing ? 'Generating Animation...' : '🎨 Generate Particle Animation'}
                </button>
                
                {isProcessing && (
                  <ProcessingStatus />
                )}
              </div>
            )}
          </div>

          {/* Right Column - Preview */}
          <div className="space-y-6">
            <AnimationPreview 
              originalImage={imageUrl} 
              animationUrl={animationUrl}
              isProcessing={isProcessing}
            />
          </div>
        </div>

        {/* Particle Animator */}
        {isProcessing && imageUrl && (
          <div className="mt-8">
            <h2 className="text-2xl font-bold text-white text-center mb-6">
              🎭 Generating Your Particle Animation
            </h2>
            <ParticleAnimator 
              imageUrl={imageUrl}
              onAnimationComplete={handleAnimationComplete}
            />
          </div>
        )}

        {/* Error Display */}
        {error && (
          <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-red-800">{error}</p>
          </div>
        )}

        {/* Features */}
        <div className="mt-16 grid md:grid-cols-3 gap-8">
          <div className="text-center p-6 bg-white/10 backdrop-blur-sm rounded-xl border border-white/20">
            <div className="text-4xl mb-4">💥</div>
            <h3 className="text-xl font-semibold text-white mb-2">Explosion Effect</h3>
            <p className="text-blue-100">Watch your painting burst into thousands of colorful particles</p>
          </div>
          
          <div className="text-center p-6 bg-white/10 backdrop-blur-sm rounded-xl border border-white/20">
            <div className="text-4xl mb-4">✨</div>
            <h3 className="text-xl font-semibold text-white mb-2">3D Animation</h3>
            <p className="text-blue-100">Particles move in 3D space with rotation and depth</p>
          </div>
          
          <div className="text-center p-6 bg-white/10 backdrop-blur-sm rounded-xl border border-white/20">
            <div className="text-4xl mb-4">🎨</div>
            <h3 className="text-xl font-semibold text-white mb-2">Perfect Reconstruction</h3>
            <p className="text-blue-100">Particles return to form the original painting perfectly</p>
          </div>
        </div>
      </div>
    </main>
  );
}
