
from dotenv import load_dotenv
from smolagents import tool
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS




# @tool
# def get_medical_document(query: str) -> str:
#     """Queries and retrieves medical documents, articles, and research papers.

#     Args:
#         query: the information about the medical symbol .

#     Returns:
#         str: Retrieved documents or articles in text format.
#     """
#     print(f"Querying documents with: {query}")
#     # Here you would implement the logic to query and retrieve documents
#     model_name = "sentence-transformers/all-mpnet-base-v2"
#     model_kwargs = {'device': 'cpu'}
#     encode_kwargs = {'normalize_embeddings': False}
#     embeddings = HuggingFaceEmbeddings(
#         model_name=model_name,
#         model_kwargs=model_kwargs,
#         encode_kwargs=encode_kwargs
# )
#     vectorstore = FAISS.load_local("hand_fracture_faiss_index", embeddings())
#     docs = vectorstore.similarity_search(query=query, k=3)
#     result = "";
#     for i, doc in enumerate(docs):
#         result += f"\nDocument {doc.metadata["source"]}:\n{doc.page_content}\n"


#     return result if result else "No relevant documents found for the query."
from smolagents import Tool

class RetrieverTool(Tool):
    name = "retriever"
    description =  "Queries and retrieves medical documents, articles, and output the research papers.Retrieved documents or articles in text format."
    inputs = {
        "query": {
            "type": "string",
            "description": "query: the information about the medical symbol.",
        }
    }
    output_type = "string"

    def __init__(self,  **kwargs):
        super().__init__(**kwargs)
        load_dotenv()
        # Initialize the retriever with our processed documents
        model_name = "sentence-transformers/all-mpnet-base-v2"
        model_kwargs = {'device': 'cpu'}
        encode_kwargs = {'normalize_embeddings': False}
        embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs=model_kwargs,
            encode_kwargs=encode_kwargs
        )
        self.vectorstore = FAISS.load_local("hand_fracture_faiss_index", embeddings,allow_dangerous_deserialization=True)

    def forward(self, query: str) -> str:
        """Execute the retrieval based on the provided query."""
        assert isinstance(query, str), "Your search query must be a string"

        # Retrieve relevant documents
        docs = self.vectorstore.similarity_search(query=query, k=3)
        result = "";
        for i, doc in enumerate(docs):
            result += f"\nDocument {doc.metadata["source"]}:\n{doc.page_content}\n"


        return result if result else "No relevant documents found for the query."

# Initialize our retriever tool with the processed documents
retriever_tool = RetrieverTool()