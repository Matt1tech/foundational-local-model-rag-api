from .base import BaseLoader
from .txt_loader import TxtLoader
from .pdf_loader import PdfLoader
from .docx_loader import DocxLoader

__all__ = [
    "BaseLoader",
    "TxtLoader",
    "PdfLoader",
    "DocxLoader",
]