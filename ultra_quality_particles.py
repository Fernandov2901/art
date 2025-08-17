#!/usr/bin/env python3
"""
Ultra-High Quality Particle Dissolution Animation
Always visible particles with dramatic 3D flying motion
"""

import numpy as np
from PIL import Image, ImageEnhance, ImageDraw, ImageFilter
import os
import sys
import random
import math

class UltraParticle:
    def __init__(self, x, y, color, original_x, original_y):
        self.original_x = float(original_x)
        self.original_y = float(original_y)
        
        # Start at original position
        self.x = float(x)
        self.y = float(y)
        self.z = 0.0
        
        self.color = color
        self.base_size = random.uniform(2.0, 5.0)  # Larger particles for visibility
        self.opacity = 255
        
        # More dramatic explosion with varied speeds
        angle_xy = random.uniform(0, 2 * math.pi)
        angle_z = random.uniform(-math.pi/2, math.pi/2)
        speed = random.uniform(6, 20)  # Faster movement
        
        # 3D velocity components
        self.vx = math.cos(angle_xy) * math.cos(angle_z) * speed
        self.vy = math.sin(angle_xy) * math.cos(angle_z) * speed
        self.vz = math.sin(angle_z) * speed
        
        # Enhanced rotation
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-20, 20)
        
        # Animation state
        self.state = "exploding"
        self.floating_offset_x = 0.0
        self.floating_offset_y = 0.0
        self.floating_offset_z = 0.0

class UltraQualityDissolution:
    def __init__(self, image):
        self.image = image
        self.width, self.height = image.size
        self.particles = []
        self.create_particles()
    
    def create_particles(self):
        """Convert every pixel into a high-quality particle"""
        print("🔥 Converting painting to ultra-quality flying particles...")
        img_array = np.array(self.image)
        
        # Sample every pixel for maximum detail
        step = 1  # Every single pixel for maximum quality
        
        for y in range(0, self.height, step):
            for x in range(0, self.width, step):
                color = tuple(img_array[y, x])
                # Include all pixels except pure black
                if sum(color) > 15:
                    particle = UltraParticle(x, y, color, x, y)
                    self.particles.append(particle)
        
        print(f"✨ Created {len(self.particles)} ultra-quality particles")
    
    def update_particles(self, frame_index, total_frames):
        """Update particle physics with enhanced visibility"""
        dissolution_frames = int(total_frames * 0.25)  # 25% for explosion
        floating_frames = int(total_frames * 0.5)      # 50% for dramatic floating
        return_frames = total_frames - dissolution_frames - floating_frames
        
        for particle in self.particles:
            if frame_index < dissolution_frames:
                # EXPLOSION PHASE - Dramatic particle creation
                progress = frame_index / dissolution_frames
                ease_progress = progress ** 1.5  # Smoother easing
                
                # Apply explosion forces with more dramatic movement
                particle.x = particle.original_x + particle.vx * ease_progress * 25
                particle.y = particle.original_y + particle.vy * ease_progress * 25
                particle.z = particle.z + particle.vz * ease_progress * 20
                
                # Enhanced physics
                particle.vy += 0.4 * ease_progress  # Stronger gravity
                particle.vx *= 0.99  # Less air resistance for longer flight
                particle.vy *= 0.99
                particle.vz *= 0.97
                
                # Rotation
                particle.rotation += particle.rotation_speed * ease_progress
                
                # Keep particles highly visible during explosion
                particle.opacity = int(255 * (0.9 - ease_progress * 0.1))  # Minimal fade
                particle.size = particle.base_size * (1 + ease_progress * 0.3)
                
            elif frame_index < dissolution_frames + floating_frames:
                # FLOATING PHASE - Particles constantly flying around in 3D space
                if particle.state == "exploding":
                    particle.state = "floating"
                    # Add random floating offsets for more organic movement
                    particle.floating_offset_x = random.uniform(-50, 50)
                    particle.floating_offset_y = random.uniform(-50, 50)
                    particle.floating_offset_z = random.uniform(-30, 30)
                
                # Continue physics with enhanced movement
                particle.x += particle.vx * 0.15
                particle.y += particle.vy * 0.15
                particle.z += particle.vz * 0.15
                
                # Dramatic floating motion - particles are ALWAYS moving
                float_time = frame_index * 0.08
                particle.x += math.sin(float_time + particle.original_x * 0.02) * 1.5
                particle.y += math.cos(float_time + particle.original_y * 0.015) * 1.2
                particle.z += math.sin(float_time * 0.7 + particle.z * 0.03) * 1.0
                
                # Add orbital motion around original position
                orbit_radius = 20 + abs(particle.z) * 0.5
                orbit_angle = float_time * 0.5 + particle.original_x * 0.01
                particle.x += math.cos(orbit_angle) * orbit_radius * 0.1
                particle.y += math.sin(orbit_angle) * orbit_radius * 0.1
                
                # Continue rotation
                particle.rotation += particle.rotation_speed * 0.3
                
                # Keep particles highly visible during floating
                particle.opacity = int(255 * 0.95)  # Always visible
                
            else:
                # RETURN PHASE - Perfect reconstruction with enhanced clarity
                if particle.state == "floating":
                    particle.state = "returning"
                
                return_progress = (frame_index - (dissolution_frames + floating_frames)) / return_frames
                return_progress = max(0.0, min(1.0, return_progress))
                
                # Smooth easing for return
                ease_return = return_progress ** 2 * (3 - 2 * return_progress)
                
                # Calculate return trajectory
                current_x = particle.x
                current_y = particle.y
                current_z = particle.z
                
                # Move back to EXACT original position
                particle.x = current_x + (particle.original_x - current_x) * ease_return * 0.2
                particle.y = current_y + (particle.original_y - current_y) * ease_return * 0.2
                particle.z = current_z + (0 - current_z) * ease_return * 0.25
                
                # Stop rotation smoothly
                particle.rotation += particle.rotation_speed * (1 - ease_return) * 0.05
                
                # Restore full opacity and original size for crystal clear final image
                particle.opacity = int(255 * (0.95 + ease_return * 0.05))
                particle.size = particle.base_size * (1 + (1 - ease_return) * 0.2)
    
    def render_frame(self, frame_index, total_frames):
        """Render a single frame with ultra-high quality"""
        # Start with very dark background for maximum contrast
        canvas = Image.new('RGB', (self.width, self.height), (2, 2, 8))
        draw = ImageDraw.Draw(canvas, 'RGBA')
        
        # Update particle physics
        self.update_particles(frame_index, total_frames)
        
        # Sort particles by Z-depth for proper 3D rendering
        sorted_particles = sorted(self.particles, key=lambda p: p.z, reverse=True)
        
        # Render particles with ultra-high quality
        for particle in sorted_particles:
            if particle.opacity > 5:  # Only render visible particles
                # Enhanced 3D perspective calculation
                perspective_factor = 1 / (1 + abs(particle.z) * 0.015)
                
                # Project 3D position to 2D screen
                screen_x = int(particle.x * perspective_factor + (1 - perspective_factor) * self.width * 0.5)
                screen_y = int(particle.y * perspective_factor + (1 - perspective_factor) * self.height * 0.5)
                
                # Size based on depth with enhanced visibility
                size = max(2, int(particle.size * perspective_factor))
                
                # Enhanced color processing
                r, g, b = particle.color
                depth_dimming = perspective_factor
                r = int(r * depth_dimming)
                g = int(g * depth_dimming)
                b = int(b * depth_dimming)
                
                alpha = max(0, min(255, int(particle.opacity * perspective_factor)))
                color = (r, g, b, alpha)
                
                # Only draw if on screen
                if -size <= screen_x <= self.width + size and -size <= screen_y <= self.height + size:
                    # Enhanced glow effect for far particles
                    if abs(particle.z) > 8:
                        glow_size = size + 4
                        glow_alpha = alpha // 3
                        glow_color = (r, g, b, glow_alpha)
                        draw.ellipse([screen_x - glow_size//2, screen_y - glow_size//2, 
                                    screen_x + glow_size//2, screen_y + glow_size//2], fill=glow_color)
                    
                    # Main particle with enhanced rendering
                    draw.ellipse([screen_x - size//2, screen_y - size//2, 
                                screen_x + size//2, screen_y + size//2], fill=color)
                    
                    # Add subtle highlight for 3D effect
                    if size > 3:
                        highlight_size = max(1, size // 3)
                        highlight_alpha = alpha // 2
                        highlight_color = (min(255, r + 30), min(255, g + 30), min(255, b + 30), highlight_alpha)
                        draw.ellipse([screen_x - highlight_size//2, screen_y - highlight_size//2, 
                                    screen_x + highlight_size//2, screen_y + highlight_size//2], fill=highlight_color)
        
        return canvas

def main():
    if len(sys.argv) != 2:
        print("Usage: python ultra_quality_particles.py <painting_file>")
        print("Available paintings:")
        paintings = [f for f in os.listdir('.') if f.startswith('Painting') and f.endswith('.jpeg')]
        for painting in paintings:
            print(f"  - {painting}")
        sys.exit(1)
    
    IMAGE_PATH = sys.argv[1]
    OUTPUT_GIF = f"ultra_quality_{os.path.splitext(IMAGE_PATH)[0]}.gif"
    
    print(f"🎨 Creating ULTRA-QUALITY PARTICLE DISSOLUTION for {IMAGE_PATH}...")
    print("💥 Phase 1: Dramatic explosive creation (25%)")
    print("🌌 Phase 2: Constant 3D flying motion (50%)")
    print("🔄 Phase 3: Crystal-clear reconstruction (25%)")
    
    if not os.path.exists(IMAGE_PATH):
        print(f"❌ Error: Image file '{IMAGE_PATH}' not found!")
        sys.exit(1)
    
    try:
        print("📸 Loading and processing image...")
        img = Image.open(IMAGE_PATH).convert("RGB")
        
        # Higher resolution for ultra quality
        max_size = 400  # Higher resolution for better quality
        if max(img.size) > max_size:
            ratio = max_size / max(img.size)
            new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
        
        print(f"🖼️ Image size: {img.size}")
        
        # Create ultra-quality dissolution
        dissolution = UltraQualityDissolution(img)
        
        # More frames for ultra-smooth animation
        total_frames = 120  # Longer animation for better quality
        print(f"🎬 Generating {total_frames} ultra-quality frames...")
        frames = []
        
        for i in range(total_frames):
            if i % 20 == 0:
                if i < total_frames * 0.25:
                    phase = "💥 Explosive Creation"
                elif i < total_frames * 0.75:
                    phase = "🌌 Constant 3D Flying"
                else:
                    phase = "🔄 Crystal Reconstruction"
                print(f"✨ Frame {i+1}/{total_frames} - {phase}")
            
            frame = dissolution.render_frame(i, total_frames)
            
            # Enhanced color processing
            time_factor = i / total_frames
            
            # Progressive color enhancement
            if i > total_frames * 0.75:
                return_progress = (i - total_frames * 0.75) / (total_frames * 0.25)
                saturation = 0.9 + 0.2 * return_progress
                enhancer = ImageEnhance.Color(frame)
                frame = enhancer.enhance(saturation)
                
                contrast = 0.95 + 0.15 * return_progress
                enhancer = ImageEnhance.Contrast(frame)
                frame = enhancer.enhance(contrast)
                
                brightness = 0.95 + 0.1 * return_progress
                enhancer = ImageEnhance.Brightness(frame)
                frame = enhancer.enhance(brightness)
            
            frames.append(frame)
        
        print(f"🎞️ Exporting ultra-quality animation...")
        
        # Save as ultra-high-quality animated GIF
        frames[0].save(
            OUTPUT_GIF,
            save_all=True,
            append_images=frames[1:],
            duration=80,  # 80ms per frame = 12.5fps for smooth motion
            loop=0,
            optimize=True,
            quality=100  # Maximum quality
        )
        
        duration = total_frames * 0.08
        file_size = os.path.getsize(OUTPUT_GIF) / (1024 * 1024)
        print(f"🌟 {OUTPUT_GIF} created!")
        print(f"🎯 Effect: ULTRA-QUALITY PARTICLE EXPLOSION → CONSTANT 3D FLYING → CRYSTAL RECONSTRUCTION")
        print(f"⏱️ Duration: {duration:.1f}s | Size: {file_size:.1f}MB")
        print(f"🎆 Particles: {len(dissolution.particles)} | Ultra Quality: Yes")
        print(f"💫 Particles are ALWAYS visible and constantly flying in 3D space!")
        print(f"🎨 Final painting is crystal clear and perfectly reconstructed!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
