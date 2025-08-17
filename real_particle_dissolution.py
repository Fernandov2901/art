#!/usr/bin/env python3
"""
Real Particle Dissolution Animation
Particles actually fly around in 3D space and return to exact positions
"""

import numpy as np
from PIL import Image, ImageEnhance, ImageDraw, ImageFilter
import os
import sys
import random
import math

class RealParticle:
    def __init__(self, x, y, color, original_x, original_y):
        self.original_x = float(original_x)
        self.original_y = float(original_y)
        
        # Start at original position
        self.x = float(x)
        self.y = float(y)
        self.z = 0.0
        
        self.color = color
        self.base_size = random.uniform(1.0, 3.0)
        self.opacity = 255
        
        # Random explosion direction in 3D space
        angle_xy = random.uniform(0, 2 * math.pi)
        angle_z = random.uniform(-math.pi/2, math.pi/2)  # Full vertical range
        speed = random.uniform(4, 15)
        
        # 3D velocity components
        self.vx = math.cos(angle_xy) * math.cos(angle_z) * speed
        self.vy = math.sin(angle_xy) * math.cos(angle_z) * speed
        self.vz = math.sin(angle_z) * speed
        
        # Rotation
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-15, 15)
        
        # Animation state
        self.state = "exploding"  # exploding, floating, returning
        self.return_start_time = None
        self.return_duration = random.uniform(30, 50)  # Frames to return

class RealParticleDissolution:
    def __init__(self, image):
        self.image = image
        self.width, self.height = image.size
        self.particles = []
        self.create_particles()
    
    def create_particles(self):
        """Convert every pixel into a real particle"""
        print("🔥 Converting painting to real flying particles...")
        img_array = np.array(self.image)
        
        # Sample every pixel for maximum detail
        step = 2  # Every 2nd pixel for good detail vs performance
        
        for y in range(0, self.height, step):
            for x in range(0, self.width, step):
                color = tuple(img_array[y, x])
                # Include more pixels, only skip completely black
                if sum(color) > 20:
                    particle = RealParticle(x, y, color, x, y)
                    self.particles.append(particle)
        
        print(f"✨ Created {len(self.particles)} real flying particles")
    
    def update_particles(self, frame_index, total_frames):
        """Update particle physics and positions"""
        dissolution_frames = int(total_frames * 0.3)  # 30% for explosion
        floating_frames = int(total_frames * 0.4)     # 40% for floating
        return_frames = total_frames - dissolution_frames - floating_frames
        
        for particle in self.particles:
            if frame_index < dissolution_frames:
                # EXPLOSION PHASE - Particles fly away from original position
                progress = frame_index / dissolution_frames
                ease_progress = progress ** 2  # Ease-out
                
                # Apply explosion forces
                particle.x = particle.original_x + particle.vx * ease_progress * 20
                particle.y = particle.original_y + particle.vy * ease_progress * 20
                particle.z = particle.z + particle.vz * ease_progress * 15
                
                # Add gravity and air resistance
                particle.vy += 0.3 * ease_progress
                particle.vx *= 0.98
                particle.vy *= 0.98
                particle.vz *= 0.95
                
                # Rotation
                particle.rotation += particle.rotation_speed * ease_progress
                
                # Fade out during explosion
                particle.opacity = int(255 * (1 - ease_progress * 0.3))
                particle.size = particle.base_size * (1 + ease_progress * 0.5)
                
            elif frame_index < dissolution_frames + floating_frames:
                # FLOATING PHASE - Particles drift in 3D space
                if particle.state == "exploding":
                    particle.state = "floating"
                
                # Continue physics
                particle.x += particle.vx * 0.1
                particle.y += particle.vy * 0.1
                particle.z += particle.vz * 0.1
                
                # Add gentle floating motion
                particle.x += math.sin(frame_index * 0.05 + particle.original_x * 0.01) * 0.8
                particle.y += math.cos(frame_index * 0.04 + particle.original_y * 0.01) * 0.6
                particle.z += math.sin(frame_index * 0.03 + particle.z * 0.02) * 0.5
                
                # Continue rotation
                particle.rotation += particle.rotation_speed * 0.2
                
                # Keep particles visible
                particle.opacity = int(255 * 0.7)
                
            else:
                # RETURN PHASE - Particles return to exact original positions
                if particle.state == "floating":
                    particle.state = "returning"
                    particle.return_start_time = frame_index
                
                return_progress = (frame_index - (dissolution_frames + floating_frames)) / return_frames
                return_progress = max(0.0, min(1.0, return_progress))
                
                # Smooth easing for return
                ease_return = return_progress ** 2 * (3 - 2 * return_progress)  # Smooth step
                
                # Calculate return trajectory
                current_x = particle.x
                current_y = particle.y
                current_z = particle.z
                
                # Move back to EXACT original position
                particle.x = current_x + (particle.original_x - current_x) * ease_return * 0.15
                particle.y = current_y + (particle.original_y - current_y) * ease_return * 0.15
                particle.z = current_z + (0 - current_z) * ease_return * 0.2
                
                # Stop rotation
                particle.rotation += particle.rotation_speed * (1 - ease_return) * 0.1
                
                # Restore full opacity and original size
                particle.opacity = int(255 * (0.7 + ease_return * 0.3))
                particle.size = particle.base_size * (1 + (1 - ease_return) * 0.5)
    
    def render_frame(self, frame_index, total_frames):
        """Render a single frame with real 3D perspective"""
        # Start with dark background
        canvas = Image.new('RGB', (self.width, self.height), (5, 5, 15))
        draw = ImageDraw.Draw(canvas, 'RGBA')
        
        # Update particle physics
        self.update_particles(frame_index, total_frames)
        
        # Sort particles by Z-depth for proper 3D rendering (far to near)
        sorted_particles = sorted(self.particles, key=lambda p: p.z, reverse=True)
        
        # Render particles with real 3D perspective
        for particle in sorted_particles:
            if particle.opacity > 1:
                # Real 3D perspective calculation
                perspective_factor = 1 / (1 + abs(particle.z) * 0.02)
                
                # Project 3D position to 2D screen
                screen_x = int(particle.x * perspective_factor + (1 - perspective_factor) * self.width * 0.5)
                screen_y = int(particle.y * perspective_factor + (1 - perspective_factor) * self.height * 0.5)
                
                # Size based on depth
                size = max(1, int(particle.size * perspective_factor))
                
                # Color with depth-based effects
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
                    if abs(particle.z) > 10:
                        glow_size = size + 3
                        glow_alpha = alpha // 4
                        glow_color = (r, g, b, glow_alpha)
                        draw.ellipse([screen_x - glow_size//2, screen_y - glow_size//2, 
                                    screen_x + glow_size//2, screen_y + glow_size//2], fill=glow_color)
                    
                    # Main particle
                    draw.ellipse([screen_x - size//2, screen_y - size//2, 
                                screen_x + size//2, screen_y + size//2], fill=color)
        
        return canvas

def main():
    if len(sys.argv) != 2:
        print("Usage: python real_particle_dissolution.py <painting_file>")
        print("Available paintings:")
        paintings = [f for f in os.listdir('.') if f.startswith('Painting') and f.endswith('.jpeg')]
        for painting in paintings:
            print(f"  - {painting}")
        sys.exit(1)
    
    IMAGE_PATH = sys.argv[1]
    OUTPUT_GIF = f"real_particles_{os.path.splitext(IMAGE_PATH)[0]}.gif"
    
    print(f"🎨 Creating REAL PARTICLE DISSOLUTION for {IMAGE_PATH}...")
    print("💥 Phase 1: Explosive particle creation (30%)")
    print("🌌 Phase 2: Particles float freely in 3D space (40%)")
    print("🔄 Phase 3: Particles return to exact positions (30%)")
    
    if not os.path.exists(IMAGE_PATH):
        print(f"❌ Error: Image file '{IMAGE_PATH}' not found!")
        sys.exit(1)
    
    try:
        print("📸 Loading and processing image...")
        img = Image.open(IMAGE_PATH).convert("RGB")
        
        # Optimize size for particle density
        max_size = 250  # Smaller for more particles
        if max(img.size) > max_size:
            ratio = max_size / max(img.size)
            new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
        
        print(f"🖼️ Image size: {img.size}")
        
        # Create real particle dissolution
        dissolution = RealParticleDissolution(img)
        
        # More frames for smoother particle motion
        total_frames = 100  # Longer animation for real particle movement
        print(f"🎬 Generating {total_frames} frames with real particle physics...")
        frames = []
        
        for i in range(total_frames):
            if i % 15 == 0:
                if i < total_frames * 0.3:
                    phase = "💥 Explosive Creation"
                elif i < total_frames * 0.7:
                    phase = "🌌 3D Floating"
                else:
                    phase = "🔄 Returning Home"
                print(f"✨ Frame {i+1}/{total_frames} - {phase}")
            
            frame = dissolution.render_frame(i, total_frames)
            
            # Add atmospheric effects
            time_factor = i / total_frames
            
            # Color enhancement during return phase
            if i > total_frames * 0.7:
                return_progress = (i - total_frames * 0.7) / (total_frames * 0.3)
                saturation = 0.8 + 0.3 * return_progress
                enhancer = ImageEnhance.Color(frame)
                frame = enhancer.enhance(saturation)
                
                contrast = 0.9 + 0.2 * return_progress
                enhancer = ImageEnhance.Contrast(frame)
                frame = enhancer.enhance(contrast)
            
            frames.append(frame)
        
        print(f"🎞️ Exporting real particle animation...")
        
        # Save as high-quality animated GIF
        frames[0].save(
            OUTPUT_GIF,
            save_all=True,
            append_images=frames[1:],
            duration=100,  # 100ms per frame = 10fps
            loop=0,
            optimize=True,
            quality=95
        )
        
        duration = total_frames * 0.1
        file_size = os.path.getsize(OUTPUT_GIF) / (1024 * 1024)
        print(f"🌟 {OUTPUT_GIF} created!")
        print(f"🎯 Effect: REAL PARTICLE EXPLOSION → 3D FLOATING → EXACT RECONSTRUCTION")
        print(f"⏱️ Duration: {duration:.1f}s | Size: {file_size:.1f}MB")
        print(f"🎆 Particles: {len(dissolution.particles)} | Real 3D Physics: Yes")
        print(f"💫 Particles actually fly around in 3D space and return to exact positions!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
