from pypdf import PdfReader

def extract_text(file_path):
    """Extracts text from PDF or TXT files."""
    if file_path.endswith(".pdf"):
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text and len(page_text.strip()) > 50:
                text += page_text
        return text
    elif file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        raise ValueError("Unsupported file type. Please use PDF or TXT.")