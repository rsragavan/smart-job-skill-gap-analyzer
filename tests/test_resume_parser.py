from app.resume.resume_parser import ResumeParser

parser = ResumeParser()

text = parser.extract_text("uploads/ragavan_resume.pdf")

print(text)