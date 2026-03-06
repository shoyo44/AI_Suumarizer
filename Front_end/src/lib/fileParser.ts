import mammoth from 'mammoth';

export interface ParseResult {
  text: string;
  fileName: string;
  fileType: string;
  pageCount?: number;
}

/**
 * Extract text from PDF file using a simpler approach
 * Note: This is a basic implementation. For better PDF parsing, consider server-side processing
 */
async function extractTextFromPDF(file: File): Promise<ParseResult> {
  try {
    // Dynamic import of PDF.js to avoid build issues
    const pdfjsLib = await import('pdfjs-dist');
    
    // Use worker from public directory
    pdfjsLib.GlobalWorkerOptions.workerSrc = '/pdf.worker.min.mjs';
    console.log('PDF.js worker configured: /pdf.worker.min.mjs');
    
    const arrayBuffer = await file.arrayBuffer();
    const loadingTask = pdfjsLib.getDocument({ data: arrayBuffer });
    const pdf = await loadingTask.promise;
    
    let fullText = '';
    
    for (let i = 1; i <= pdf.numPages; i++) {
      const page = await pdf.getPage(i);
      const textContent = await page.getTextContent();
      const pageText = textContent.items
        .map((item: any) => {
          if ('str' in item) {
            return item.str;
          }
          return '';
        })
        .join(' ');
      fullText += pageText + '\n\n';
    }
    
    if (!fullText.trim()) {
      throw new Error('No text found in PDF. The PDF might be image-based or empty.');
    }
    
    return {
      text: fullText.trim(),
      fileName: file.name,
      fileType: 'PDF',
      pageCount: pdf.numPages,
    };
  } catch (error: any) {
    console.error('PDF parsing error:', error);
    throw new Error(`Failed to parse PDF: ${error.message || 'Unknown error'}. Try converting to TXT first.`);
  }
}

/**
 * Extract text from DOCX file
 */
async function extractTextFromDOCX(file: File): Promise<ParseResult> {
  try {
    const arrayBuffer = await file.arrayBuffer();
    const result = await mammoth.extractRawText({ arrayBuffer });
    
    if (!result.value.trim()) {
      throw new Error('No text found in DOCX file.');
    }
    
    return {
      text: result.value.trim(),
      fileName: file.name,
      fileType: 'DOCX',
    };
  } catch (error: any) {
    console.error('DOCX parsing error:', error);
    throw new Error(`Failed to parse DOCX: ${error.message || 'Unknown error'}`);
  }
}

/**
 * Extract text from TXT file
 */
async function extractTextFromTXT(file: File): Promise<ParseResult> {
  try {
    const text = await file.text();
    
    if (!text.trim()) {
      throw new Error('The text file is empty.');
    }
    
    return {
      text: text.trim(),
      fileName: file.name,
      fileType: 'TXT',
    };
  } catch (error: any) {
    console.error('TXT parsing error:', error);
    throw new Error(`Failed to parse TXT: ${error.message || 'Unknown error'}`);
  }
}

/**
 * Main function to parse uploaded file
 */
export async function parseFile(file: File): Promise<ParseResult> {
  const fileType = file.type;
  const fileName = file.name.toLowerCase();
  
  console.log('📄 Parsing file:', fileName, 'Type:', fileType, 'Size:', file.size);
  
  try {
    // PDF files
    if (fileType === 'application/pdf' || fileName.endsWith('.pdf')) {
      console.log('🔍 Detected PDF file, extracting text...');
      return await extractTextFromPDF(file);
    }
    
    // DOCX files
    if (
      fileType === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' ||
      fileName.endsWith('.docx')
    ) {
      console.log('🔍 Detected DOCX file, extracting text...');
      return await extractTextFromDOCX(file);
    }
    
    // TXT files
    if (fileType === 'text/plain' || fileName.endsWith('.txt')) {
      console.log('🔍 Detected TXT file, reading text...');
      return await extractTextFromTXT(file);
    }
    
    throw new Error('Unsupported file type. Please upload PDF, DOCX, or TXT files.');
  } catch (error: any) {
    console.error('❌ File parsing error:', error);
    throw error;
  }
}

/**
 * Validate file before parsing
 */
export function validateFile(file: File): { valid: boolean; error?: string } {
  const maxSize = 10 * 1024 * 1024; // 10MB
  const allowedTypes = [
    'application/pdf',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'text/plain',
  ];
  const allowedExtensions = ['.pdf', '.docx', '.txt'];
  
  console.log('✅ Validating file:', file.name, 'Size:', (file.size / 1024 / 1024).toFixed(2) + 'MB', 'Type:', file.type);
  
  // Check file size
  if (file.size > maxSize) {
    return {
      valid: false,
      error: `File size (${(file.size / 1024 / 1024).toFixed(2)}MB) exceeds 10MB limit`,
    };
  }
  
  // Check file type
  const fileName = file.name.toLowerCase();
  const hasValidType = allowedTypes.includes(file.type);
  const hasValidExtension = allowedExtensions.some(ext => fileName.endsWith(ext));
  
  if (!hasValidType && !hasValidExtension) {
    return {
      valid: false,
      error: `Invalid file type "${file.type}". Please upload PDF, DOCX, or TXT files.`,
    };
  }
  
  console.log('✅ File validation passed');
  return { valid: true };
}
