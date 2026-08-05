from dataclasses import dataclass

import fitz


@dataclass
class PDFParseResult:
    success: bool
    extracted_text: str
    page_count: int
    error: str | None = None


def parse_pdf(
    pdf_path: str,
) -> PDFParseResult:

    try:
        document = fitz.open(pdf_path)

        pages = []

        for page in document:
            pages.append(
                page.get_text()
            )

        document.close()

        text = "\n".join(pages)

        if not text.strip():
            return PDFParseResult(
                success=False,
                extracted_text="",
                page_count=len(pages),
                error="No extractable text found.",
            )

        return PDFParseResult(
            success=True,
            extracted_text="\n".join(pages),
            page_count=len(pages),
        )

    except Exception as e:

        return PDFParseResult(
            success=False,
            extracted_text="",
            page_count=0,
            error=str(e),
        )