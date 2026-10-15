import PyPDF2
import re


def extract_text_from_pdf(pdf_file):

    text = ""

    reader = PyPDF2.PdfReader(pdf_file)

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    # Remove unwanted website/footer text
    text = re.sub(
        r'www\.enhancv\.com.*',
        '',
        text,
        flags=re.IGNORECASE
    )

    # Fix common PDF extraction spacing
    replacements = {
        "DjangoFlask": "Django Flask",
        "FlaskREST": "Flask REST",
        "RESTAPIs": "REST APIs",
        "MySQLSQLite": "MySQL SQLite",
        "ExcelPowerBI": "Excel Power BI",
        "PowerBITableau": "Power BI Tableau",
        "TableauPandas": "Tableau Pandas",
        "GitGitHub": "Git GitHub",
        "GenerativeAI": "Generative AI",
        "PromptEngineering": "Prompt Engineering",
        "HTML 5": "HTML5",
        "CSS 3": "CSS3",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    # Remove spaces between single characters
    text = re.sub(
        r'(?<!\w)([A-Za-z])\s+(?=[A-Za-z](?!\w))',
        r'\1',
        text
    )

    # Fix multiple spaces
    text = re.sub(r'[ \t]+', ' ', text)

    # Remove excessive blank lines
    text = re.sub(r'\n\s*\n+', '\n\n', text)

    return text.strip()