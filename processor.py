import fitz  # PyMuPDF
from rapidocr_onnxruntime import RapidOCR

# Lazy-load OCR engine once for faster performance
_ocr_engine = None


def get_ocr():
    global _ocr_engine
    if _ocr_engine is None:
        _ocr_engine = RapidOCR()
    return _ocr_engine


def extract_pages_from_pdf(file_bytes: bytes, filename: str = "document.pdf") -> list[dict]:
    """Extracts page-by-page text from both typed and scanned/image-based PDFs."""
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    pages_data = []

    for page_num, page in enumerate(doc, start=1):
        text = page.get_text("text").strip()

        # Fallback to OCR if the page has minimal extractable text (scanned/photo page)
        if len(text) < 40:
            pix = page.get_pixmap(dpi=150)
            img_bytes = pix.tobytes("png")
            result, _ = get_ocr()(img_bytes)
            if result:
                text = "\n".join([line[1] for line in result]).strip()

        if text:
            pages_data.append({
                "source": filename,
                "page": page_num,
                "text": text
            })

    doc.close()
    return pages_data


def process_multiple_pdfs(files_list: list, topic_keyword: str = "") -> str:
    """
    Combines multiple Streamlit UploadedFiles (or (name, bytes) tuples).
    If topic_keyword is provided, filters pages matching that topic across all PDFs.
    """
    all_pages = []

    for f in files_list:
        if hasattr(f, "getvalue"):
            name, raw_bytes = f.name, f.getvalue()
        else:
            name, raw_bytes = f[0], f[1]
        all_pages.extend(extract_pages_from_pdf(raw_bytes, name))

    if not all_pages:
        return ""

    # Smart topic page search (handles combined or mismatched unit PDFs)
    if topic_keyword and topic_keyword.strip():
        keywords = [k.strip().lower() for k in topic_keyword.split(",") if k.strip()]
        matched = [
            p for p in all_pages
            if any(k in p["text"].lower() for k in keywords)
        ]
        # Use matched pages if found; otherwise fall back to all pages
        selected_pages = matched if matched else all_pages
    else:
        selected_pages = all_pages

    combined = []
    for p in selected_pages:
        combined.append(f"--- [{p['source']} | Page {p['page']}] ---\n{p['text']}")

    return "\n\n".join(combined)