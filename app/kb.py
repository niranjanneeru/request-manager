from langchain.text_splitter import CharacterTextSplitter
from PyPDF2 import PdfReader

from app.qdrant import QClient


class KnowledgeBase:
    def add_to_kb(self, pdf_filename, document_id):
        pdf_reader = PdfReader(pdf_filename)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1600,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_text(text)

        QClient().add_vdb(document_id, chunks)
