import PyPDF2
import docx

def extract_text(file):
    """
    Extract text from PDF or DOCX files
    """
    if file.type == "application/pdf":
        pdf = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
        return text
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = docx.Document(file)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
    else:
        return ""
