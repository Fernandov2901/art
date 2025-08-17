#!/usr/bin/env python3
"""
Simple Painting Animation Script
Creates beautiful particle animations from paintings using PIL for GIF output
"""

import numpy as np
from PIL import Image, ImageEnhance, ImageDraw
import os
import sys
import random

class ParticleSystem:
    def __init__(self, width, height, max_particles=1000):
        self.width = width
        self.height = height
        self.max_particles = max_particles
        self.particles = []
        
    def add_particle(self, x, y, color, depth_val, frame_index):
        z_distance = depth_val * 100
        velocity_x = random.uniform(-2, 2) * (1 + depth_val)
        velocity_y = random.uniform(-3, -1) * (1 + depth_val * 2)
        velocity_z = random.uniform(0.5, 2) * depth_val
        
        particle = {
            'x': x, 'y': y, 'z': z_distance,
            'vx': velocity_x, 'vy': velocity_y, 'vz': velocity_z,
            'color': color,
            'size': random.uniform(2, 6) * (1 + depth_val),
            'life': random.uniform(30, 60),  # Shorter life for GIF
            'birth_frame': frame_index,
            'opacity': 255,
            'rotation': random.uniform(0, 360),
            'rotation_speed': random.uniform(-5, 5)
        }
        
        if len(self.particles) < self.max_particles:
            self.particles.append(particle)
    
    def update_particles(self, frame_index):
        updated_particles = []
        for particle in self.particles:
            age = frame_index - particle['birth_frame']
            if age < particle['life']:
                particle['x'] += particle['vx']
                particle['y'] += particle['vy']
                particle['z'] += particle['vz']
                particle['vy'] += 0.1
                particle['vx'] *= 0.995
                particle['vy'] *= 0.995
                particle['vz'] *= 0.99
                particle['rotation'] += particle['rotation_speed']
                life_ratio = age / particle['life']
                particle['opacity'] = int(255 * (1 - life_ratio))
                scale_factor = 1 + (particle['z'] / 200)
                particle['current_size'] = particle['size'] * scale_factor
                updated_particles.append(particle)
        self.particles = updated_particles
    
    def render_particles(self, image):
        img_array = np.array(image)
        draw_img = Image.fromarray(img_array)
        draw = ImageDraw.Draw(draw_img, 'RGBA')
        sorted_particles = sorted(self.particles, key=lambda p: p['z'], reverse=True)
        
        for particle in sorted_particles:
            if 0 <= particle['x'] < self.width and 0 <= particle['y'] < self.height:
                r, g, b = particle['color']
                alpha = max(0, min(255, particle['opacity']))
                color = (r, g, b, alpha)
                size = max(1, int(particle['current_size']))
                x, y = int(particle['x']), int(particle['y'])
                
                if particle['z'] > 50:
                    blur_size = max(1, int(particle['z'] / 30))
                    for i in range(blur_size):
                        offset = i - blur_size // 2
                        alpha_reduced = alpha // (blur_size + 1)
                        blur_color = (r, g, b, alpha_reduced)
                        draw.ellipse([x + offset - size//2, y + offset - size//2,
                                    x + offset + size//2, y + offset + size//2], fill=blur_color)
                else:
                    draw.ellipse([x - size//2, y - size//2, x + size//2, y + size//2], fill=color)
        return draw_img

def create_simple_depth_map(image):
    """Create a simple depth map based on brightness and edge detection"""
    img_array = np.array(image.convert('L'))  # Convert to grayscale
    
    # Simple edge detection
    from PIL import ImageFilter
    edges = image.filter(ImageFilter.FIND_EDGES)
    edge_array = np.array(edges.convert('L'))
    
    # Combine brightness and edges for depth estimation
    depth_map = (img_array.astype(np.float32) / 255.0) * 0.7 + (edge_array.astype(np.float32) / 255.0) * 0.3
    
    # Normalize to 0-1 range
    depth_map = (depth_map - depth_map.min()) / (depth_map.max() - depth_map.min())
    
    return depth_map

class ArtisticStyleProcessor:
    def __init__(self, width=1024, height=1024):
        self.particle_system = ParticleSystem(width, height)
    
    def particle_powder_style(self, image, depth_map, frame_index, total_frames):
        img_array = np.array(image).astype(np.float32)
        h, w, c = img_array.shape
        time_factor = frame_index / total_frames
        enhanced_img = img_array.copy()
        
        particle_spawn_rate = max(1, int(20 * (1 + np.sin(time_factor * 4 * np.pi))))
        
        for _ in range(particle_spawn_rate):
            x = random.randint(0, w-1)
            y = random.randint(0, h-1)
            depth_val = depth_map[y, x]
            
            if random.random() < depth_val * 0.8:
                pixel_color = tuple(img_array[y, x].astype(int))
                r, g, b = pixel_color
                r = max(0, min(255, r + random.randint(-20, 20)))
                g = max(0, min(255, g + random.randint(-20, 20)))
                b = max(0, min(255, b + random.randint(-20, 20)))
                self.particle_system.add_particle(x, y, (r, g, b), depth_val, frame_index)
        
        self.particle_system.update_particles(frame_index)
        
        extraction_intensity = 0.3 + 0.2 * np.sin(time_factor * 2 * np.pi)
        for y in range(h):
            for x in range(w):
                depth_val = depth_map[y, x]
                if depth_val > 0.6:
                    fade_factor = 1 - (depth_val * extraction_intensity * 0.4)
                    enhanced_img[y, x] *= fade_factor
                    gray_val = np.mean(enhanced_img[y, x])
                    blend_factor = depth_val * 0.2
                    enhanced_img[y, x] = enhanced_img[y, x] * (1 - blend_factor) + gray_val * blend_factor
        
        wave_strength = 2
        for y in range(h):
            wave_offset = int(wave_strength * np.sin(time_factor * 2 * np.pi + y * 0.01))
            if wave_offset != 0:
                enhanced_img[y] = np.roll(enhanced_img[y], wave_offset, axis=0)
        
        canvas_img = Image.fromarray(np.clip(enhanced_img, 0, 255).astype(np.uint8))
        final_img = self.particle_system.render_particles(canvas_img)
        return final_img

def main():
    if len(sys.argv) != 2:
        print("Usage: python animate_painting_simple.py <painting_file>")
        print("Available paintings:")
        paintings = [f for f in os.listdir('.') if f.startswith('Painting') and f.endswith('.jpeg')]
        for painting in paintings:
            print(f"  - {painting}")
        sys.exit(1)
    
    IMAGE_PATH = sys.argv[1]
    OUTPUT_GIF = f"painting_animation_{os.path.splitext(IMAGE_PATH)[0]}.gif"
    
    print(f"🎨 Creating PARTICLE POWDER animation for {IMAGE_PATH}...")
    
    if not os.path.exists(IMAGE_PATH):
        print(f"❌ Error: Image file '{IMAGE_PATH}' not found!")
        sys.exit(1)
    
    try:
        print("📸 Processing image...")
        img = Image.open(IMAGE_PATH).convert("RGB")
        
        # Resize for processing
        if max(img.size) > 800:
            img.thumbnail((800, 800), Image.Resampling.LANCZOS)
        
        print("🕳️ Creating depth map...")
        depth_map = create_simple_depth_map(img)
        
        h, w = img.size[1], img.size[0]
        processor = ArtisticStyleProcessor(w, h)
        
        # Generate 60 frames (3 seconds at 20fps for GIF)
        num_frames = 60
        print(f"🎬 Generating {num_frames} frames...")
        frames = []
        
        for i in range(num_frames):
            if i % 10 == 0:
                particle_count = len(processor.particle_system.particles)
                print(f"✨ Frame {i+1}/{num_frames} - Particles: {particle_count}")
            
            artistic_frame = processor.particle_powder_style(img, depth_map, i, num_frames)
            
            # Enhance colors
            time_factor = i / num_frames
            saturation = 1.0 + 0.3 * np.sin(time_factor * 2 * np.pi)
            enhancer = ImageEnhance.Color(artistic_frame)
            artistic_frame = enhancer.enhance(saturation)
            
            contrast = 1.0 + 0.2 * np.cos(time_factor * 1.5 * np.pi)
            enhancer = ImageEnhance.Contrast(artistic_frame)
            artistic_frame = enhancer.enhance(contrast)
            
            frames.append(artistic_frame)
        
        print(f"🎞️ Exporting animated GIF...")
        
        # Save as animated GIF
        frames[0].save(
            OUTPUT_GIF,
            save_all=True,
            append_images=frames[1:],
            duration=100,  # 100ms per frame = 10fps
            loop=0,
            optimize=True
        )
        
        duration = num_frames * 0.1  # 10fps
        file_size = os.path.getsize(OUTPUT_GIF) / (1024 * 1024)  # MB
        print(f"🌟 {OUTPUT_GIF} created!")
        print(f"🎯 Style: PARTICLE POWDER | Duration: {duration:.1f}s | Size: {file_size:.1f}MB")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
