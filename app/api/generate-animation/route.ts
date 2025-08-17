import { NextRequest, NextResponse } from 'next/server';
import { writeFile, mkdir } from 'fs/promises';
import path from 'path';

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData();
    const file = formData.get('image') as File;
    
    if (!file) {
      return NextResponse.json({ error: 'No image file provided' }, { status: 400 });
    }

    // Validate file type
    if (!file.type.startsWith('image/')) {
      return NextResponse.json({ error: 'Invalid file type. Please upload an image.' }, { status: 400 });
    }

    // Validate file size (max 10MB)
    if (file.size > 10 * 1024 * 1024) {
      return NextResponse.json({ error: 'File too large. Please upload an image smaller than 10MB.' }, { status: 400 });
    }

    // Create directories if they don't exist
    const uploadsDir = path.join(process.cwd(), 'uploads');
    
    try {
      await mkdir(uploadsDir, { recursive: true });
    } catch (error) {
      console.log('Directories already exist');
    }

    // Save uploaded file
    const bytes = await file.arrayBuffer();
    const buffer = Buffer.from(bytes);
    const fileName = `upload_${Date.now()}_${file.name}`;
    const filePath = path.join(uploadsDir, fileName);
    await writeFile(filePath, buffer);

    // Return success with the uploaded file info
    return NextResponse.json({
      success: true,
      message: 'Image uploaded successfully!',
      fileName: fileName,
      // Return the uploaded image data for client-side processing
      imageData: {
        name: file.name,
        size: file.size,
        type: file.type
      }
    });

  } catch (error) {
    console.error('Error processing request:', error);
    return NextResponse.json(
      { error: 'Failed to process image' },
      { status: 500 }
    );
  }
}

export async function GET() {
  return NextResponse.json({
    message: 'Particle Animation Generator API',
    status: 'ready'
  })
}
