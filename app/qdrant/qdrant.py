from langchain_community.vectorstores import Qdrant
from langchain_together import TogetherEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.http.models import Filter, FieldCondition, MatchValue

from config import Config

embeddings = TogetherEmbeddings(model="togethercomputer/m2-bert-80M-8k-retrieval")
collection_name = "knowledge_base"


class QClient:
    _instance = None  # Class variable to hold the singleton instance

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(QClient, cls).__new__(cls)
            cls._instance._initialize_client()
        return cls._instance

    def _initialize_client(self):
        self.client = QdrantClient(
            url=Config.QDRANT_API_URL,
            api_key=Config.QDRANT_API_KEY
        )

    def get_client(self):
        return self.client

    def add_vdb(self, document_id, chunks):
        vectorstore = Qdrant.from_texts(
            texts=chunks,
            embedding=embeddings,
            url=Config.QDRANT_API_URL,
            api_key=Config.QDRANT_API_KEY,
            collection_name=collection_name,
            metadatas=[{"document_id": document_id} for _ in chunks]
        )

        retriever = vectorstore.as_retriever()

        return retriever

    def fetch_retriever_by_document_id(self, document_id):
        metadata_filter = Filter(
            must=[
                FieldCondition(
                    key="metadata.document_id",  # Field to filter on
                    match=MatchValue(value=document_id)  # Value of the document_id
                )
            ]
        )

        # Create a Qdrant VectorStore retriever
        vectorstore = Qdrant(
            client=self.get_client(),
            collection_name=collection_name,
            embeddings=embeddings
        )

        # Use the retriever with the filter
        retriever = vectorstore.as_retriever(
            search_type="similarity",  # Use filter search
            filter=metadata_filter  # Apply the filter
        )

        return retriever

    def fetch_retriever(self):
        vectorstore = Qdrant(
            client=self.get_client(),
            collection_name=collection_name,
            embeddings=embeddings
        )

        retriever = vectorstore.as_retriever()

        return retriever
