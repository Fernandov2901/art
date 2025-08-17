#!/usr/bin/env python3
"""
Ultra-HD Particle Animation
Tiny particles, maximum count, high definition quality
"""

import numpy as np
from PIL import Image, ImageEnhance, ImageDraw, ImageFilter
import os
import sys
import random
import math

class UltraHDParticle:
    def __init__(self, x, y, color, original_x, original_y):
        self.original_x = float(original_x)
        self.original_y = float(original_y)
        
        # Start at original position
        self.x = float(x)
        self.y = float(y)
        self.z = 0.0
        
        self.color = color
        self.base_size = random.uniform(0.8, 2.5)  # Much smaller particles for HD quality
        self.opacity = 255  # Always full opacity
        
        # Dramatic explosion with varied speeds
        angle_xy = random.uniform(0, 2 * math.pi)
        angle_z = random.uniform(-math.pi/2, math.pi/2)
        speed = random.uniform(10, 30)  # Faster movement for smaller particles
        
        # 3D velocity components
        self.vx = math.cos(angle_xy) * math.cos(angle_z) * speed
        self.vy = math.sin(angle_xy) * math.cos(angle_z) * speed
        self.vz = math.sin(angle_z) * speed
        
        # Enhanced rotation
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-30, 30)
        
        # Animation state
        self.state = "exploding"
        self.floating_offset_x = 0.0
        self.floating_offset_y = 0.0
        self.floating_offset_z = 0.0

class UltraHDDissolution:
    def __init__(self, image):
        self.image = image
        self.width, self.height = image.size
        self.particles = []
        self.create_particles()
    
    def create_particles(self):
        """Convert every pixel into tiny HD particles"""
        print("🔥 Converting painting to ultra-HD tiny particles...")
        img_array = np.array(self.image)
        
        # Sample every pixel for maximum detail
        step = 1  # Every single pixel for maximum particle count
        
        for y in range(0, self.height, step):
            for x in range(0, self.width, step):
                color = tuple(img_array[y, x])
                # Include all pixels except pure black for maximum particle count
                if sum(color) > 10:  # Lower threshold for more particles
                    particle = UltraHDParticle(x, y, color, x, y)
                    self.particles.append(particle)
        
        print(f"✨ Created {len(self.particles)} ultra-HD tiny particles")
    
    def update_particles(self, frame_index, total_frames):
        """Update particle physics with HD precision"""
        dissolution_frames = int(total_frames * 0.2)  # 20% for explosion
        floating_frames = int(total_frames * 0.6)     # 60% for dramatic floating
        return_frames = total_frames - dissolution_frames - floating_frames
        
        for particle in self.particles:
            if frame_index < dissolution_frames:
                # EXPLOSION PHASE - Particles fly away with HD precision
                progress = frame_index / dissolution_frames
                ease_progress = progress ** 1.5
                
                # Apply explosion forces with precise movement
                particle.x = particle.original_x + particle.vx * ease_progress * 35
                particle.y = particle.original_y + particle.vy * ease_progress * 35
                particle.z = particle.z + particle.vz * ease_progress * 30
                
                # Enhanced physics for small particles
                particle.vy += 0.6 * ease_progress  # Stronger gravity for small particles
                particle.vx *= 0.998  # Less air resistance for longer flight
                particle.vy *= 0.998
                particle.vz *= 0.99
                
                # Rotation
                particle.rotation += particle.rotation_speed * ease_progress
                
                # CRITICAL: Particles NEVER fade - always full opacity
                particle.opacity = 255  # Always visible!
                particle.size = particle.base_size * (1 + ease_progress * 0.15)
                
            elif frame_index < dissolution_frames + floating_frames:
                # FLOATING PHASE - Particles constantly flying around in 3D space
                if particle.state == "exploding":
                    particle.state = "floating"
                    # Add random floating offsets for more organic movement
                    particle.floating_offset_x = random.uniform(-80, 80)
                    particle.floating_offset_y = random.uniform(-80, 80)
                    particle.floating_offset_z = random.uniform(-50, 50)
                
                # Continue physics with enhanced movement
                particle.x += particle.vx * 0.25
                particle.y += particle.vy * 0.25
                particle.z += particle.vz * 0.25
                
                # Dramatic floating motion - particles are ALWAYS moving and visible
                float_time = frame_index * 0.12
                particle.x += math.sin(float_time + particle.original_x * 0.03) * 2.5
                particle.y += math.cos(float_time + particle.original_y * 0.025) * 2.2
                particle.z += math.sin(float_time * 0.9 + particle.z * 0.05) * 2.0
                
                # Add orbital motion around original position
                orbit_radius = 30 + abs(particle.z) * 0.8
                orbit_angle = float_time * 0.7 + particle.original_x * 0.02
                particle.x += math.cos(orbit_angle) * orbit_radius * 0.2
                particle.y += math.sin(orbit_angle) * orbit_radius * 0.2
                
                # Continue rotation
                particle.rotation += particle.rotation_speed * 0.5
                
                # CRITICAL: Particles stay at full opacity during floating
                particle.opacity = 255  # Always visible!
                
            else:
                # RETURN PHASE - Perfect reconstruction with HD clarity
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
                
                # Move back to EXACT original position with HD precision
                particle.x = current_x + (particle.original_x - current_x) * ease_return * 0.3
                particle.y = current_y + (particle.original_y - current_y) * ease_return * 0.3
                particle.z = current_z + (0 - current_z) * ease_return * 0.35
                
                # Stop rotation smoothly
                particle.rotation += particle.rotation_speed * (1 - ease_return) * 0.05
                
                # CRITICAL: Particles become even more visible during return
                particle.opacity = 255  # Maximum visibility for final painting
                particle.size = particle.base_size * (1 + (1 - ease_return) * 0.05)
    
    def render_frame(self, frame_index, total_frames):
        """Render a single frame with ultra-HD quality"""
        # Start with very dark background for maximum contrast
        canvas = Image.new('RGB', (self.width, self.height), (0, 0, 2))
        draw = ImageDraw.Draw(canvas, 'RGBA')
        
        # Update particle physics
        self.update_particles(frame_index, total_frames)
        
        # Sort particles by Z-depth for proper 3D rendering
        sorted_particles = sorted(self.particles, key=lambda p: p.z, reverse=True)
        
        # Render particles with ultra-HD quality
        for particle in sorted_particles:
            # CRITICAL: Only render if particle is visible (which they always are)
            if particle.opacity > 1:
                # Enhanced 3D perspective calculation for HD
                perspective_factor = 1 / (1 + abs(particle.z) * 0.01)
                
                # Project 3D position to 2D screen with precision
                screen_x = int(particle.x * perspective_factor + (1 - perspective_factor) * self.width * 0.5)
                screen_y = int(particle.y * perspective_factor + (1 - perspective_factor) * self.height * 0.5)
                
                # Size based on depth with HD precision
                size = max(1, int(particle.size * perspective_factor))  # Minimum size 1 for HD detail
                
                # Enhanced color processing - NO dimming for maximum visibility
                r, g, b = particle.color
                # Remove depth dimming - particles are always bright
                r = int(r)
                g = int(g)
                b = int(b)
                
                # CRITICAL: Full opacity always
                alpha = 255
                color = (r, g, b, alpha)
                
                # Only draw if on screen
                if -size <= screen_x <= self.width + size and -size <= screen_y <= self.height + size:
                    # Enhanced glow effect for far particles
                    if abs(particle.z) > 5:
                        glow_size = size + 3
                        glow_alpha = 80  # Subtle glow for HD quality
                        glow_color = (r, g, b, glow_alpha)
                        draw.ellipse([screen_x - glow_size//2, screen_y - glow_size//2, 
                                    screen_x + glow_size//2, screen_y + glow_size//2], fill=glow_color)
                    
                    # Main particle with HD precision
                    draw.ellipse([screen_x - size//2, screen_y - size//2, 
                                screen_x + size//2, screen_y + size//2], fill=color)
                    
                    # Add subtle highlight for 3D effect and HD quality
                    if size > 2:
                        highlight_size = max(1, size // 3)
                        highlight_alpha = 120
                        highlight_color = (min(255, r + 25), min(255, g + 25), min(255, b + 25), highlight_alpha)
                        draw.ellipse([screen_x - highlight_size//2, screen_y - highlight_size//2, 
                                    screen_x + highlight_size//2, screen_y + highlight_size//2], fill=highlight_color)
        
        return canvas

def main():
    if len(sys.argv) != 2:
        print("Usage: python ultra_hd_particles.py <painting_file>")
        print("Available paintings:")
        paintings = [f for f in os.listdir('.') if f.startswith('Painting') and f.endswith('.jpeg')]
        for painting in paintings:
            print(f"  - {painting}")
        sys.exit(1)
    
    IMAGE_PATH = sys.argv[1]
    OUTPUT_GIF = f"ultra_hd_{os.path.splitext(IMAGE_PATH)[0]}.gif"
    
    print(f"🎨 Creating ULTRA-HD PARTICLE DISSOLUTION for {IMAGE_PATH}...")
    print("💥 Phase 1: Explosive creation with TINY HD particles (20%)")
    print("🌌 Phase 2: Constant 3D flying with MAXIMUM particles (60%)")
    print("🔄 Phase 3: Ultra-HD painting reconstruction (20%)")
    
    if not os.path.exists(IMAGE_PATH):
        print(f"❌ Error: Image file '{IMAGE_PATH}' not found!")
        sys.exit(1)
    
    try:
        print("📸 Loading and processing image...")
        img = Image.open(IMAGE_PATH).convert("RGB")
        
        # Ultra-high resolution for maximum HD quality
        max_size = 500  # Higher resolution for ultra-HD quality
        if max(img.size) > max_size:
            ratio = max_size / max(img.size)
            new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
        
        print(f"🖼️ Image size: {img.size}")
        
        # Create ultra-HD dissolution
        dissolution = UltraHDDissolution(img)
        
        # More frames for ultra-smooth HD animation
        total_frames = 120  # More frames for HD quality
        print(f"🎬 Generating {total_frames} ultra-HD frames...")
        frames = []
        
        for i in range(total_frames):
            if i % 20 == 0:
                if i < total_frames * 0.2:
                    phase = "💥 Explosive Creation"
                elif i < total_frames * 0.8:
                    phase = "🌌 Constant 3D Flying"
                else:
                    phase = "🔄 Ultra-HD Reconstruction"
                print(f"✨ Frame {i+1}/{total_frames} - {phase}")
            
            frame = dissolution.render_frame(i, total_frames)
            
            # Enhanced color processing for HD final painting
            if i > total_frames * 0.8:
                return_progress = (i - total_frames * 0.8) / (total_frames * 0.2)
                saturation = 0.98 + 0.18 * return_progress
                enhancer = ImageEnhance.Color(frame)
                frame = enhancer.enhance(saturation)
                
                contrast = 0.99 + 0.15 * return_progress
                enhancer = ImageEnhance.Contrast(frame)
                frame = enhancer.enhance(contrast)
                
                brightness = 0.99 + 0.15 * return_progress
                enhancer = ImageEnhance.Brightness(frame)
                frame = enhancer.enhance(brightness)
                
                # Sharpness enhancement for HD quality
                sharpness = 0.95 + 0.2 * return_progress
                enhancer = ImageEnhance.Sharpness(frame)
                frame = enhancer.enhance(sharpness)
            
            frames.append(frame)
        
        print(f"🎞️ Exporting ultra-HD animation...")
        
        # Save as ultra-high-quality animated GIF
        frames[0].save(
            OUTPUT_GIF,
            save_all=True,
            append_images=frames[1:],
            duration=75,  # 75ms per frame = ~13.3fps for smooth HD motion
            loop=0,
            optimize=True,
            quality=100  # Maximum quality
        )
        
        duration = total_frames * 0.075
        file_size = os.path.getsize(OUTPUT_GIF) / (1024 * 1024)
        print(f"🌟 {OUTPUT_GIF} created!")
        print(f"🎯 Effect: ULTRA-HD TINY PARTICLE EXPLOSION → MAXIMUM 3D FLYING → HD RECONSTRUCTION")
        print(f"⏱️ Duration: {duration:.1f}s | Size: {file_size:.1f}MB")
        print(f"🎆 Particles: {len(dissolution.particles)} | Ultra-HD Quality: Yes")
        print(f"💫 TINY particles with MAXIMUM count - always visible and constantly flying!")
        print(f"🎨 Final painting is ULTRA-HD and perfectly reconstructed!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
