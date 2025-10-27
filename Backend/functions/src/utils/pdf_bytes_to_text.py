from typing import Optional
import fitz

def pdf_bytes_to_text(pdf_bytes: bytes, max_chars: Optional[int] = None)->str:
    text = []
    try:
        with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
            for page in doc:
                text.append(page.get_text("text"))
            full_text = "\n".join(text)
            if max_chars and len(full_text) > max_chars:
                return full_text[:max_chars]
            return full_text
    except Exception as e:  
        raise RuntimeError(f"Failed to extract text from PDF: {e}")