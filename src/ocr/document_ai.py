import os
import asyncio
from google.api_core.client_options import ClientOptions
from google.cloud import documentai_v1



class DocumentAIOCR:
    """A class to handle Google Document AI OCR operations"""
    
    def __init__(self, parser_nm: str, processor_id: str = "5945bfe7932ca5b7"):
        """
        Initialize Google Document AI Processor
        
        Args:
            parser_nm: Name of the parser
            processor_id: ID of the Document AI processor
        """
        self.api_location = os.getenv("API_LOCATION", "")
        self.project_id = os.getenv("PROJECT_ID", "")
        
        if not self.api_location or not self.project_id:
            raise ValueError("API_LOCATION and PROJECT_ID environment variables must be set")
            
        self.client = self._initialize_client()
        self.processor = self._initialize_processor(processor_id)
    
    def _initialize_client(self) -> documentai_v1.DocumentProcessorServiceClient:
        """Initialize and return Document AI client"""
        client_options = ClientOptions(
            api_endpoint=f"{self.api_location}-documentai.googleapis.com"
        )
        return documentai_v1.DocumentProcessorServiceClient(
            client_options=client_options
        )
    
    def _initialize_processor(self, processor_id: str) -> documentai_v1.Processor:
        """Initialize and return Document AI processor"""
        processor_name = self.client.processor_path(
            self.project_id, 
            self.api_location, 
            processor_id
        )
        request = documentai_v1.GetProcessorRequest(name=processor_name)
        return self.client.get_processor(request=request)
    
    def _read_image(self, img_path: str) -> bytes:
        """Read image file and return bytes content"""
        try:
            with open(img_path, "rb") as image:
                return image.read()
        except IOError as e:
            raise IOError(f"Error reading image file {img_path}: {str(e)}")
    
    def perform_ocr(self, img_path: str) -> documentai_v1.Document:
        """
        Perform OCR for a given image path
        
        Args:
            img_path: Path to the image file
            
        Returns:
            Document object containing OCR results
        """
        img_content = self._read_image(img_path)
        raw_document = documentai_v1.RawDocument(
            content=img_content,
            mime_type="image/png"
        )
        
        try:
            request = documentai_v1.ProcessRequest(
                name=self.processor.name,
                raw_document=raw_document
            )
            result = self.client.process_document(request=request)
            return result.document
        except Exception as e:
            raise RuntimeError(f"OCR processing failed: {str(e)}")
    
    async def perform_ocr_async(self, img_path: str) -> documentai_v1.Document:
        """Asynchronous version of perform_ocr"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.perform_ocr, img_path)
    
    async def process_multiple_images(self, img_paths: list) -> list:
        """
        Process multiple images concurrently
        
        Args:
            img_paths: List of image paths to process
            
        Returns:
            List of Document objects containing OCR results
        """
        tasks = [self.perform_ocr_async(img_path) for img_path in img_paths]
        return await asyncio.gather(*tasks, return_exceptions=True)