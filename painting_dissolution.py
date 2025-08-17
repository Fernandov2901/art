#!/usr/bin/env python3
"""
Painting Dissolution Animation
The entire painting dissolves into particles and then reconstructs itself
"""

import numpy as np
from PIL import Image, ImageEnhance, ImageDraw
import os
import sys
import random
import math

class Particle:
    def __init__(self, x, y, color, original_x, original_y):
        self.original_x = original_x
        self.original_y = original_y
        self.x = x
        self.y = y
        self.color = color
        self.size = random.uniform(1, 3)
        self.opacity = 255
        
        # Random initial velocity for explosion
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 8)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        
        # Add some randomness to the original position for reconstruction
        self.target_x = original_x + random.uniform(-2, 2)
        self.target_y = original_y + random.uniform(-2, 2)

class PaintingDissolution:
    def __init__(self, image):
        self.image = image
        self.width, self.height = image.size
        self.particles = []
        self.create_particles()
    
    def create_particles(self):
        """Convert every pixel of the painting into a particle"""
        print("🔥 Converting painting to particles...")
        img_array = np.array(self.image)
        
        # Sample every nth pixel to keep particle count manageable
        step = 3  # Take every 3rd pixel
        
        for y in range(0, self.height, step):
            for x in range(0, self.width, step):
                color = tuple(img_array[y, x])
                # Skip very dark pixels to reduce particle count
                if sum(color) > 50:  # Skip nearly black pixels
                    particle = Particle(x, y, color, x, y)
                    self.particles.append(particle)
        
        print(f"✨ Created {len(self.particles)} particles")
    
    def update_particles_dissolution(self, frame_index, total_frames):
        """Update particles during dissolution phase (first half)"""
        progress = (frame_index / (total_frames * 0.5))  # 0 to 1 for first half
        progress = min(1.0, progress)
        
        for particle in self.particles:
            # Explosion phase - particles fly away from original position
            explosion_factor = progress * 2  # Accelerate explosion
            
            particle.x = particle.original_x + particle.vx * explosion_factor * 20
            particle.y = particle.original_y + particle.vy * explosion_factor * 20
            
            # Add gravity and air resistance
            particle.vy += 0.3 * explosion_factor  # Gravity
            particle.vx *= 0.98  # Air resistance
            particle.vy *= 0.98
            
            # Fade out particles as they spread
            particle.opacity = int(255 * (1 - progress * 0.7))
            particle.size = particle.size * (1 + progress * 0.5)
    
    def update_particles_reconstruction(self, frame_index, total_frames):
        """Update particles during reconstruction phase (second half)"""
        mid_point = total_frames * 0.5
        progress = (frame_index - mid_point) / (total_frames * 0.5)  # 0 to 1 for second half
        progress = max(0.0, min(1.0, progress))
        
        for particle in self.particles:
            # Reconstruction phase - particles return to original positions
            current_x = particle.x
            current_y = particle.y
            
            # Smoothly interpolate back to target position
            ease_factor = 1 - (1 - progress) ** 3  # Ease-in cubic
            
            particle.x = current_x + (particle.target_x - current_x) * ease_factor * 0.1
            particle.y = current_y + (particle.target_y - current_y) * ease_factor * 0.1
            
            # Fade particles back in
            particle.opacity = int(255 * (0.3 + progress * 0.7))
            particle.size = max(1, particle.size * (1 - progress * 0.3))
    
    def render_frame(self, frame_index, total_frames):
        """Render a single frame of the animation"""
        # Create blank canvas
        canvas = Image.new('RGB', (self.width, self.height), (20, 20, 30))  # Dark background
        draw = ImageDraw.Draw(canvas, 'RGBA')
        
        # Update particle positions based on animation phase
        if frame_index < total_frames * 0.5:
            self.update_particles_dissolution(frame_index, total_frames)
        else:
            self.update_particles_reconstruction(frame_index, total_frames)
        
        # Sort particles by distance for proper depth rendering
        sorted_particles = sorted(self.particles, key=lambda p: p.x + p.y)
        
        # Render all particles
        for particle in sorted_particles:
            if particle.opacity > 5:  # Only render visible particles
                r, g, b = particle.color
                alpha = max(0, min(255, int(particle.opacity)))
                color = (r, g, b, alpha)
                size = max(1, int(particle.size))
                
                x, y = int(particle.x), int(particle.y)
                
                # Only draw if particle is within canvas bounds
                if -size <= x <= self.width + size and -size <= y <= self.height + size:
                    draw.ellipse([x - size//2, y - size//2, x + size//2, y + size//2], fill=color)
        
        return canvas

def main():
    if len(sys.argv) != 2:
        print("Usage: python painting_dissolution.py <painting_file>")
        print("Available paintings:")
        paintings = [f for f in os.listdir('.') if f.startswith('Painting') and f.endswith('.jpeg')]
        for painting in paintings:
            print(f"  - {painting}")
        sys.exit(1)
    
    IMAGE_PATH = sys.argv[1]
    OUTPUT_GIF = f"dissolution_{os.path.splitext(IMAGE_PATH)[0]}.gif"
    
    print(f"🎨 Creating DISSOLUTION animation for {IMAGE_PATH}...")
    print("💥 Phase 1: Painting dissolves into particles")
    print("🔄 Phase 2: Particles reconstruct the painting")
    
    if not os.path.exists(IMAGE_PATH):
        print(f"❌ Error: Image file '{IMAGE_PATH}' not found!")
        sys.exit(1)
    
    try:
        print("📸 Loading and processing image...")
        img = Image.open(IMAGE_PATH).convert("RGB")
        
        # Resize for processing (smaller for better performance)
        max_size = 400  # Smaller for more manageable particle count
        if max(img.size) > max_size:
            ratio = max_size / max(img.size)
            new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
        
        print(f"🖼️ Image size: {img.size}")
        
        # Create dissolution animation
        dissolution = PaintingDissolution(img)
        
        # Generate frames: 30 for dissolution + 30 for reconstruction
        total_frames = 60
        print(f"🎬 Generating {total_frames} frames...")
        frames = []
        
        for i in range(total_frames):
            if i % 10 == 0:
                phase = "Dissolution" if i < total_frames * 0.5 else "Reconstruction"
                print(f"✨ Frame {i+1}/{total_frames} - {phase}")
            
            frame = dissolution.render_frame(i, total_frames)
            
            # Add slight color enhancement
            time_factor = i / total_frames
            if i > total_frames * 0.7:  # Enhance colors during reconstruction
                saturation = 1.0 + 0.3 * (i - total_frames * 0.7) / (total_frames * 0.3)
                enhancer = ImageEnhance.Color(frame)
                frame = enhancer.enhance(saturation)
            
            frames.append(frame)
        
        print(f"🎞️ Exporting dissolution animation...")
        
        # Save as animated GIF
        frames[0].save(
            OUTPUT_GIF,
            save_all=True,
            append_images=frames[1:],
            duration=150,  # 150ms per frame = ~6.7fps for smoother motion
            loop=0,
            optimize=True
        )
        
        duration = total_frames * 0.15  # 6.7fps
        file_size = os.path.getsize(OUTPUT_GIF) / (1024 * 1024)  # MB
        print(f"🌟 {OUTPUT_GIF} created!")
        print(f"🎯 Effect: FULL DISSOLUTION → RECONSTRUCTION | Duration: {duration:.1f}s | Size: {file_size:.1f}MB")
        print(f"💫 The painting completely dissolves and then magically rebuilds itself!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
