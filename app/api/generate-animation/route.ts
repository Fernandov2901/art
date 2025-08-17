import { NextRequest, NextResponse } from 'next/server'
import { writeFile, mkdir } from 'fs/promises'
import { join } from 'path'
import { exec } from 'child_process'
import { promisify } from 'util'

const execAsync = promisify(exec)

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData()
    const file = formData.get('image') as File
    
    if (!file) {
      return NextResponse.json(
        { error: 'No image file provided' },
        { status: 400 }
      )
    }

    // Validate file type
    if (!file.type.startsWith('image/')) {
      return NextResponse.json(
        { error: 'File must be an image' },
        { status: 400 }
      )
    }

    // Validate file size (10MB max)
    if (file.size > 10 * 1024 * 1024) {
      return NextResponse.json(
        { error: 'File size must be less than 10MB' },
        { status: 400 }
      )
    }

    // Create uploads directory if it doesn't exist
    const uploadsDir = join(process.cwd(), 'uploads')
    await mkdir(uploadsDir, { recursive: true })

    // Save uploaded file
    const bytes = await file.arrayBuffer()
    const buffer = Buffer.from(bytes)
    const fileName = `upload_${Date.now()}_${file.name}`
    const filePath = join(uploadsDir, fileName)
    await writeFile(filePath, buffer)

    // Create output directory
    const outputDir = join(process.cwd(), 'public', 'animations')
    await mkdir(outputDir, { recursive: true })

    // Generate unique output filename
    const outputFileName = `animation_${Date.now()}.gif`
    const outputPath = join(outputDir, outputFileName)

    // Run the Python animation script
    const pythonScript = join(process.cwd(), 'perfect_final_painting.py')
    const command = `cd ${process.cwd()} && ./painting_env/bin/python ${pythonScript} ${filePath}`
    
    console.log('Executing command:', command)
    
    const { stdout, stderr } = await execAsync(command)
    
    if (stderr) {
      console.error('Python script stderr:', stderr)
    }
    
    console.log('Python script stdout:', stdout)

    // Check if animation was created
    const animationUrl = `/animations/${outputFileName}`

    return NextResponse.json({
      success: true,
      animationUrl,
      message: 'Animation generated successfully!'
    })

  } catch (error) {
    console.error('Error generating animation:', error)
    return NextResponse.json(
      { error: 'Failed to generate animation' },
      { status: 500 }
    )
  }
}

export async function GET() {
  return NextResponse.json({
    message: 'Particle Animation Generator API',
    status: 'ready'
  })
}
