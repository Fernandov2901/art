'use client';

import { useEffect, useRef, useState } from 'react';

interface Particle {
  x: number;
  y: number;
  originalX: number;
  originalY: number;
  r: number;
  g: number;
  b: number;
  a: number;
  vx: number;
  vy: number;
  vz: number;
  size: number;
  opacity: number;
  rotation: number;
  rotationSpeed: number;
}

interface ParticleAnimatorProps {
  imageUrl: string;
  onAnimationComplete: (animationUrl: string) => void;
}

export default function ParticleAnimator({ imageUrl, onAnimationComplete }: ParticleAnimatorProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [progress, setProgress] = useState(0);
  const [currentPhase, setCurrentPhase] = useState('');

  useEffect(() => {
    if (imageUrl && canvasRef.current) {
      generateAnimation();
    }
  }, [imageUrl]);

  const generateAnimation = async () => {
    if (!canvasRef.current) return;

    setIsGenerating(true);
    setProgress(0);
    setCurrentPhase('Initializing...');

    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d')!;

    // Load the image
    const img = new Image();
    img.crossOrigin = 'anonymous';
    
    img.onload = () => {
      // Set canvas size
      const maxSize = 400;
      let { width, height } = img;
      
      if (width > height) {
        if (width > maxSize) {
          height = (height * maxSize) / width;
          width = maxSize;
        }
      } else {
        if (height > maxSize) {
          width = (width * maxSize) / height;
          height = maxSize;
        }
      }

      canvas.width = width;
      canvas.height = height;

      // Draw image to get pixel data
      ctx.drawImage(img, 0, 0, width, height);
      const imageData = ctx.getImageData(0, 0, width, height);
      
      // Create particles
      setCurrentPhase('Creating particles...');
      setProgress(20);
      
      const particles = createParticles(imageData, 2);
      
      // Generate animation phases
      generateAnimationPhases(ctx, particles, imageData);
    };

    img.src = imageUrl;
  };

  const createParticles = (imageData: ImageData, step: number = 2): Particle[] => {
    const particles: Particle[] = [];
    const { data, width, height } = imageData;
    
    for (let y = 0; y < height; y += step) {
      for (let x = 0; x < width; x += step) {
        const index = (y * width + x) * 4;
        const r = data[index];
        const g = data[index + 1];
        const b = data[index + 2];
        const a = data[index + 3];
        
        if (a > 0) {
          particles.push({
            x: x,
            y: y,
            originalX: x,
            originalY: y,
            r, g, b, a,
            vx: 0,
            vy: 0,
            vz: 0,
            size: Math.random() * 2 + 1,
            opacity: 1,
            rotation: 0,
            rotationSpeed: (Math.random() - 0.5) * 0.2
          });
        }
      }
    }
    
    return particles;
  };

  const generateAnimationPhases = async (ctx: CanvasRenderingContext2D, particles: Particle[], originalImageData: ImageData) => {
    const canvas = ctx.canvas;
    const { width, height } = canvas;
    const frames: string[] = [];
    
    // Phase 1: Explosion
    setCurrentPhase('Generating explosion phase...');
    setProgress(40);
    
    const explosionFrames = generateExplosionPhase(ctx, particles, width, height);
    frames.push(...explosionFrames);
    
    // Phase 2: Floating
    setCurrentPhase('Generating floating phase...');
    setProgress(60);
    
    const floatingFrames = generateFloatingPhase(ctx, particles, width, height);
    frames.push(...floatingFrames);
    
    // Phase 3: Return
    setCurrentPhase('Generating return phase...');
    setProgress(80);
    
    const returnFrames = generateReturnPhase(ctx, particles, width, height);
    frames.push(...returnFrames);
    
    // Phase 4: Final painting
    setCurrentPhase('Generating final frames...');
    setProgress(90);
    
    const finalFrames = generateFinalFrames(ctx, originalImageData);
    frames.push(...finalFrames);
    
    // Create animation
    setCurrentPhase('Creating animation...');
    setProgress(95);
    
    const animationUrl = await createAnimation(frames, width, height);
    
    setProgress(100);
    setCurrentPhase('Complete!');
    setIsGenerating(false);
    
    onAnimationComplete(animationUrl);
  };

  const generateExplosionPhase = (ctx: CanvasRenderingContext2D, particles: Particle[], width: number, height: number): string[] => {
    const frames: string[] = [];
    const totalFrames = 30;
    
    for (let frame = 0; frame < totalFrames; frame++) {
      ctx.clearRect(0, 0, width, height);
      
      particles.forEach(particle => {
        const progress = frame / totalFrames;
        const explosionForce = 100 * progress;
        
        // Add explosion velocity
        particle.vx = (particle.x - width / 2) * explosionForce / 100;
        particle.vy = (particle.y - height / 2) * explosionForce / 100;
        particle.vz = (Math.random() - 0.5) * explosionForce;
        
        // Update position
        particle.x += particle.vx * 0.1;
        particle.y += particle.vy * 0.1;
        
        // Draw particle
        ctx.save();
        ctx.globalAlpha = particle.opacity;
        ctx.fillStyle = `rgba(${particle.r}, ${particle.g}, ${particle.b}, ${particle.a / 255})`;
        ctx.translate(particle.x, particle.y);
        ctx.rotate(particle.rotation);
        ctx.fillRect(-particle.size/2, -particle.size/2, particle.size, particle.size);
        ctx.restore();
        
        particle.rotation += particle.rotationSpeed;
      });
      
      frames.push(canvasRef.current!.toDataURL());
    }
    
    return frames;
  };

  const generateFloatingPhase = (ctx: CanvasRenderingContext2D, particles: Particle[], width: number, height: number): string[] => {
    const frames: string[] = [];
    const totalFrames = 40;
    
    for (let frame = 0; frame < totalFrames; frame++) {
      ctx.clearRect(0, 0, width, height);
      
      particles.forEach(particle => {
        // Add floating motion
        particle.x += Math.sin(frame * 0.1 + particle.originalX * 0.01) * 0.5;
        particle.y += Math.cos(frame * 0.1 + particle.originalY * 0.01) * 0.5;
        
        // Draw particle
        ctx.save();
        ctx.globalAlpha = particle.opacity;
        ctx.fillStyle = `rgba(${particle.r}, ${particle.g}, ${particle.b}, ${particle.a / 255})`;
        ctx.translate(particle.x, particle.y);
        ctx.rotate(particle.rotation);
        ctx.fillRect(-particle.size/2, -particle.size/2, particle.size, particle.size);
        ctx.restore();
        
        particle.rotation += particle.rotationSpeed;
      });
      
      frames.push(canvasRef.current!.toDataURL());
    }
    
    return frames;
  };

  const generateReturnPhase = (ctx: CanvasRenderingContext2D, particles: Particle[], width: number, height: number): string[] => {
    const frames: string[] = [];
    const totalFrames = 40;
    
    for (let frame = 0; frame < totalFrames; frame++) {
      ctx.clearRect(0, 0, width, height);
      
      particles.forEach(particle => {
        // Calculate return position
        const targetX = particle.originalX;
        const targetY = particle.originalY;
        
        particle.x = particle.x + (targetX - particle.x) * 0.1;
        particle.y = particle.y + (targetY - particle.y) * 0.1;
        
        // Draw particle
        ctx.save();
        ctx.globalAlpha = particle.opacity;
        ctx.fillStyle = `rgba(${particle.r}, ${particle.g}, ${particle.b}, ${particle.a / 255})`;
        ctx.translate(particle.x, particle.y);
        ctx.rotate(particle.rotation);
        ctx.fillRect(-particle.size/2, -particle.size/2, particle.size, particle.size);
        ctx.restore();
        
        particle.rotation += particle.rotationSpeed;
      });
      
      frames.push(canvasRef.current!.toDataURL());
    }
    
    return frames;
  };

  const generateFinalFrames = (ctx: CanvasRenderingContext2D, originalImageData: ImageData): string[] => {
    const frames: string[] = [];
    const totalFrames = 10;
    
    for (let frame = 0; frame < totalFrames; frame++) {
      ctx.putImageData(originalImageData, 0, 0);
      frames.push(canvasRef.current!.toDataURL());
    }
    
    return frames;
  };

  const createAnimation = async (frames: string[], width: number, height: number): Promise<string> => {
    // For now, return the first frame as a static image
    // In a full implementation, you'd use a GIF encoder library
    return frames[0];
  };

  return (
    <div className="w-full max-w-2xl mx-auto">
      <canvas
        ref={canvasRef}
        className="w-full h-auto border border-gray-300 rounded-lg shadow-lg"
        style={{ display: isGenerating ? 'block' : 'none' }}
      />
      
      {isGenerating && (
        <div className="mt-4 p-4 bg-blue-50 rounded-lg">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-blue-800">{currentPhase}</span>
            <span className="text-sm text-blue-600">{progress}%</span>
          </div>
          <div className="w-full bg-blue-200 rounded-full h-2">
            <div
              className="bg-blue-600 h-2 rounded-full transition-all duration-300"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>
      )}
    </div>
  );
}
