import os
from typing import List

import fitz
import markdown
import requests
import resend
from markdown_pdf import MarkdownPdf, Section

output_dir = "output"
os.makedirs(output_dir, exist_ok=True)


def generate_pdf(name: str, markdown: str) -> None:
    """
    Generates a PDF from the given markdown content.

    Args:
        name (str): pdf file name.
        markdown (str): The markdown content for the pdf.

    Returns:
        None
    """
    pdf = MarkdownPdf()
    pdf.add_section(Section(markdown))
    try:
        pdf.save(f"{output_dir}/{name}.pdf")
    except IOError as e:
        print(f"Failed to save PDF report: {e}")


def write(filename: str, markdown: str, append=False) -> None:
    mode = "a" if append else "w"
    with open(f"{output_dir}/{filename}", mode) as f:
        f.write(markdown)


def extract_text_from_pdf(file: str) -> str:
    doc = fitz.open(file)
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def download(link: str, filename: str) -> None:
    r = requests.get(link)
    with open(f"{output_dir}/{filename}", "wb") as f:
        f.write(r.content)


def filename(file: str) -> str:
    return ".".join(os.path.basename(file).split(".")[0:-1])


def output_content(topic, format, content):
    if format == "md":
        write(f"{topic}.md", content)
    elif format == "pdf":
        generate_pdf(topic, content)
    else:
        print(f"Invalid format({format}). Please choose either 'md' or 'pdf'.")


def send_mail(topic: str, receivers: List[str], content: str):
    html = markdown.markdown(content)
    resend.api_key = os.getenv("RESEND_API_KEY")
    email_from = os.getenv("EMAIL_FROM")
    resend.Emails.send(
        {
            "from": email_from,
            "to": receivers,
            "subject": topic,
            "html": html,
        }
    )
