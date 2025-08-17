#!/usr/bin/env python3
"""
Enhanced Painting Dissolution Animation
Complete dissolution into 3D particles with full reconstruction
"""

import numpy as np
from PIL import Image, ImageEnhance, ImageDraw, ImageFilter
import os
import sys
import random
import math

class Particle3D:
    def __init__(self, x, y, z, color, original_x, original_y):
        self.original_x = original_x
        self.original_y = original_y
        self.original_z = 0
        
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        
        self.color = color
        self.base_size = random.uniform(0.8, 2.5)
        self.opacity = 255
        
        # 3D explosion velocity
        angle_xy = random.uniform(0, 2 * math.pi)
        angle_z = random.uniform(-math.pi/3, math.pi/3)  # Vertical spread
        speed = random.uniform(3, 12)
        
        self.vx = math.cos(angle_xy) * math.cos(angle_z) * speed
        self.vy = math.sin(angle_xy) * math.cos(angle_z) * speed
        self.vz = math.sin(angle_z) * speed
        
        # Rotation for 3D effect
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-10, 10)
        
        # Target position (with slight variation for organic feel)
        self.target_x = original_x + random.uniform(-1, 1)
        self.target_y = original_y + random.uniform(-1, 1)
        self.target_z = 0

class EnhancedDissolution:
    def __init__(self, image):
        self.image = image
        self.width, self.height = image.size
        self.particles = []
        self.create_particles()
    
    def create_particles(self):
        """Convert every pixel into a 3D particle with depth"""
        print("🔥 Converting painting to 3D particles...")
        img_array = np.array(self.image)
        
        # Create depth map from image brightness and edges
        gray = self.image.convert('L')
        edges = gray.filter(ImageFilter.FIND_EDGES)
        gray_array = np.array(gray).astype(np.float32)
        edge_array = np.array(edges).astype(np.float32)
        
        # Combine brightness and edges for depth
        depth_map = (gray_array / 255.0) * 0.6 + (edge_array / 255.0) * 0.4
        depth_map = (depth_map - depth_map.min()) / (depth_map.max() - depth_map.min())
        
        # Sample every pixel for maximum detail
        step = 2  # Every 2nd pixel for good detail vs performance balance
        
        for y in range(0, self.height, step):
            for x in range(0, self.width, step):
                color = tuple(img_array[y, x])
                # Include more pixels, only skip completely black
                if sum(color) > 20:
                    # Use depth for initial Z position
                    z = depth_map[y, x] * 50  # 0-50 depth range
                    particle = Particle3D(x, y, z, color, x, y)
                    self.particles.append(particle)
        
        print(f"✨ Created {len(self.particles)} 3D particles")
    
    def update_particles_dissolution(self, frame_index, total_frames):
        """Explosive dissolution phase"""
        dissolution_frames = int(total_frames * 0.4)  # 40% for dissolution
        progress = min(1.0, frame_index / dissolution_frames)
        
        # Easing function for smooth explosion
        ease_progress = 1 - (1 - progress) ** 2  # Ease-out quadratic
        
        for particle in self.particles:
            # Explosive movement with 3D physics
            explosion_factor = ease_progress * 25
            
            particle.x = particle.original_x + particle.vx * explosion_factor
            particle.y = particle.original_y + particle.vy * explosion_factor  
            particle.z = particle.original_z + particle.vz * explosion_factor
            
            # Add gravity and air resistance
            particle.vy += 0.4 * progress  # Gravity
            particle.vx *= 0.97  # Air resistance
            particle.vy *= 0.97
            particle.vz *= 0.95
            
            # Rotation
            particle.rotation += particle.rotation_speed * progress
            
            # Fade and size changes
            particle.opacity = int(255 * (1 - progress * 0.8))
            particle.size = particle.base_size * (1 + progress * 1.5)
    
    def update_particles_floating(self, frame_index, total_frames):
        """Floating in space phase"""
        dissolution_frames = int(total_frames * 0.4)
        floating_frames = int(total_frames * 0.2)  # 20% floating
        
        if frame_index < dissolution_frames + floating_frames:
            progress = (frame_index - dissolution_frames) / floating_frames
            progress = max(0.0, min(1.0, progress))
            
            for particle in self.particles:
                # Gentle floating motion
                particle.x += math.sin(frame_index * 0.1 + particle.original_x * 0.01) * 0.5
                particle.y += math.cos(frame_index * 0.08 + particle.original_y * 0.01) * 0.3
                particle.z += math.sin(frame_index * 0.05 + particle.z * 0.02) * 0.8
                
                # Slow rotation
                particle.rotation += particle.rotation_speed * 0.3
                
                # Keep particles visible but dim
                particle.opacity = int(255 * 0.4)
    
    def update_particles_reconstruction(self, frame_index, total_frames):
        """Reconstruction phase - particles return to exact original positions"""
        dissolution_frames = int(total_frames * 0.4)
        floating_frames = int(total_frames * 0.2)
        reconstruction_start = dissolution_frames + floating_frames
        reconstruction_frames = total_frames - reconstruction_start
        
        if frame_index >= reconstruction_start:
            progress = (frame_index - reconstruction_start) / reconstruction_frames
            progress = max(0.0, min(1.0, progress))
            
            # Smooth easing for reconstruction
            ease_progress = progress ** 2 * (3 - 2 * progress)  # Smooth step
            
            for particle in self.particles:
                # Move back to EXACT original position
                particle.x = particle.x + (particle.original_x - particle.x) * ease_progress * 0.15
                particle.y = particle.y + (particle.original_y - particle.y) * ease_progress * 0.15
                particle.z = particle.z + (particle.original_z - particle.z) * ease_progress * 0.2
                
                # Stop rotation
                particle.rotation += particle.rotation_speed * (1 - progress)
                
                # Restore full opacity and original size
                particle.opacity = int(255 * (0.4 + progress * 0.6))
                particle.size = particle.base_size * (1 + (1 - progress) * 1.5)
    
    def render_frame(self, frame_index, total_frames):
        """Render a single frame with 3D perspective"""
        # Start with dark background for dramatic effect
        canvas = Image.new('RGB', (self.width, self.height), (5, 5, 15))
        draw = ImageDraw.Draw(canvas, 'RGBA')
        
        # Update particles based on animation phase
        dissolution_frames = int(total_frames * 0.4)
        floating_frames = int(total_frames * 0.2)
        
        if frame_index < dissolution_frames:
            self.update_particles_dissolution(frame_index, total_frames)
        elif frame_index < dissolution_frames + floating_frames:
            self.update_particles_floating(frame_index, total_frames)
        else:
            self.update_particles_reconstruction(frame_index, total_frames)
        
        # Sort particles by Z-depth for proper 3D rendering (far to near)
        sorted_particles = sorted(self.particles, key=lambda p: p.z, reverse=True)
        
        # Render particles with 3D perspective
        for particle in sorted_particles:
            if particle.opacity > 1:
                # 3D perspective calculation
                perspective_factor = 1 / (1 + particle.z * 0.01)
                screen_x = int(particle.x * perspective_factor + (1 - perspective_factor) * self.width * 0.5)
                screen_y = int(particle.y * perspective_factor + (1 - perspective_factor) * self.height * 0.5)
                
                # Size based on depth
                size = max(1, int(particle.size * perspective_factor))
                
                # Color with depth-based dimming
                r, g, b = particle.color
                depth_dimming = perspective_factor
                r = int(r * depth_dimming)
                g = int(g * depth_dimming)
                b = int(b * depth_dimming)
                
                alpha = max(0, min(255, int(particle.opacity * perspective_factor)))
                color = (r, g, b, alpha)
                
                # Only draw if on screen
                if -size <= screen_x <= self.width + size and -size <= screen_y <= self.height + size:
                    # Add glow effect for far particles
                    if particle.z > 20:
                        glow_size = size + 2
                        glow_alpha = alpha // 3
                        glow_color = (r, g, b, glow_alpha)
                        draw.ellipse([screen_x - glow_size//2, screen_y - glow_size//2, 
                                    screen_x + glow_size//2, screen_y + glow_size//2], fill=glow_color)
                    
                    # Main particle
                    draw.ellipse([screen_x - size//2, screen_y - size//2, 
                                screen_x + size//2, screen_y + size//2], fill=color)
        
        return canvas

def main():
    if len(sys.argv) != 2:
        print("Usage: python enhanced_dissolution.py <painting_file>")
        print("Available paintings:")
        paintings = [f for f in os.listdir('.') if f.startswith('Painting') and f.endswith('.jpeg')]
        for painting in paintings:
            print(f"  - {painting}")
        sys.exit(1)
    
    IMAGE_PATH = sys.argv[1]
    OUTPUT_GIF = f"enhanced_dissolution_{os.path.splitext(IMAGE_PATH)[0]}.gif"
    
    print(f"🎨 Creating ENHANCED 3D DISSOLUTION for {IMAGE_PATH}...")
    print("💥 Phase 1: Complete explosive dissolution (40%)")
    print("🌌 Phase 2: Particles float in 3D space (20%)")
    print("🔄 Phase 3: Perfect reconstruction (40%)")
    
    if not os.path.exists(IMAGE_PATH):
        print(f"❌ Error: Image file '{IMAGE_PATH}' not found!")
        sys.exit(1)
    
    try:
        print("📸 Loading and processing image...")
        img = Image.open(IMAGE_PATH).convert("RGB")
        
        # Optimize size for particle density
        max_size = 300  # Smaller for more particles
        if max(img.size) > max_size:
            ratio = max_size / max(img.size)
            new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
        
        print(f"🖼️ Image size: {img.size}")
        
        # Create enhanced dissolution
        dissolution = EnhancedDissolution(img)
        
        # More frames for smoother animation
        total_frames = 80  # Longer animation
        print(f"🎬 Generating {total_frames} frames with 3D effects...")
        frames = []
        
        for i in range(total_frames):
            if i % 10 == 0:
                if i < total_frames * 0.4:
                    phase = "💥 Explosive Dissolution"
                elif i < total_frames * 0.6:
                    phase = "🌌 3D Floating"
                else:
                    phase = "🔄 Perfect Reconstruction"
                print(f"✨ Frame {i+1}/{total_frames} - {phase}")
            
            frame = dissolution.render_frame(i, total_frames)
            
            # Add atmospheric effects
            time_factor = i / total_frames
            
            # Color enhancement during reconstruction
            if i > total_frames * 0.6:
                reconstruction_progress = (i - total_frames * 0.6) / (total_frames * 0.4)
                saturation = 0.7 + 0.4 * reconstruction_progress
                enhancer = ImageEnhance.Color(frame)
                frame = enhancer.enhance(saturation)
                
                contrast = 0.8 + 0.3 * reconstruction_progress
                enhancer = ImageEnhance.Contrast(frame)
                frame = enhancer.enhance(contrast)
            
            frames.append(frame)
        
        print(f"🎞️ Exporting enhanced 3D dissolution...")
        
        # Save as high-quality animated GIF
        frames[0].save(
            OUTPUT_GIF,
            save_all=True,
            append_images=frames[1:],
            duration=120,  # 120ms per frame = ~8.3fps
            loop=0,
            optimize=True,
            quality=95
        )
        
        duration = total_frames * 0.12
        file_size = os.path.getsize(OUTPUT_GIF) / (1024 * 1024)
        print(f"🌟 {OUTPUT_GIF} created!")
        print(f"🎯 Effect: 3D DISSOLUTION → FLOATING → PERFECT RECONSTRUCTION")
        print(f"⏱️ Duration: {duration:.1f}s | Size: {file_size:.1f}MB")
        print(f"🎆 Particles: {len(dissolution.particles)} | 3D Depth: Yes")
        print(f"💫 The painting explodes into 3D space and perfectly rebuilds!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
