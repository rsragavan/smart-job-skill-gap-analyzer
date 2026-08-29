import fitz


class ResumeParseError(ValueError):
    """Raised when a PDF cannot provide usable resume text."""


class ResumeParser:
    def extract_text(self, pdf_path: str) -> str:
        try:
            with fitz.open(pdf_path) as document:
                if document.is_encrypted:
                    raise ResumeParseError("Password-protected PDFs are not supported")
                if document.page_count == 0:
                    raise ResumeParseError("The PDF does not contain any pages")

                text = "\n".join(page.get_text("text") for page in document).strip()
        except ResumeParseError:
            raise
        except (fitz.FileDataError, fitz.EmptyFileError, ValueError, OSError) as exc:
            raise ResumeParseError("The PDF is corrupted or could not be parsed") from exc

        if not text:
            raise ResumeParseError(
                "The PDF contains no selectable text; scanned resumes require OCR"
            )

        return text
