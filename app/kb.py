import re

from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_core.output_parsers import BaseOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

from app.ai import AIModels
from app.qdrant import QClient

document_property_template = """<s>[INST]

You are an intelligent document analysis assistant.
Your task is to determine the subject and topic of the following uploaded document.
Based on the content provided, you need to infer the overall subject area (e.g., Mathematics, Computer Science, Physics, etc.) and the specific topic (e.g., Red-Black Trees, Quantum Mechanics, Linear Algebra, etc.).

question: {question}

Task:
Subject: Analyze the content of the document and infer its broader subject area.
Topic: Based on the content, identify the specific topic discussed in the document.

Data Provided:
context: {context}

Requirements:
Analyze the content to determine whether the document focuses on theoretical concepts, practical applications, or specific subfields.
Use the terminology, key phrases, and examples in the document to help pinpoint the subject and topic.
Provide a clear and concise subject and topic.

Example Structure:
Subject: [Identify the general subject of the document]
Topic: [Identify the specific topic discussed in the document]

Adhere to Example Structure no other info needed
[/INST]

"""


class KBParser(BaseOutputParser):
    def parse(self, text):
        document_pattern = re.compile(
            r"Subject:\s*(.*?)\nTopic:\s*(.*?)\n", re.DOTALL
        )

        # Search for the sections
        match = document_pattern.search(text)

        if match:
            subject = match.group(1).strip()
            topic = match.group(2).strip()

            return {
                "Subject": subject,
                "Topic": topic
            }
        else:
            return None


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
        prompt = ChatPromptTemplate.from_template(document_property_template)
        model = AIModels().document_properties_model()

        chain = (
                {
                    "context": QClient().fetch_retriever_by_document_id(document_id),
                    "question": RunnablePassthrough()
                }
                | prompt
                | model
                | KBParser()
        )

        output = chain.invoke("Classify subject & topic")

        return output
