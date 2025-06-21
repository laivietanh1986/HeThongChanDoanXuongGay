# List of useful URLs
import requests
from bs4 import BeautifulSoup
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
model_name = "sentence-transformers/all-mpnet-base-v2"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': False}
embeddings = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)
vectorstore = FAISS.load_local("hand_fracture_faiss_index", HuggingFaceEmbeddings(),allow_dangerous_deserialization=True)
docs = vectorstore.similarity_search("How do you treat a broken finger, got Metacarpal fracture ?", k=3)

for i, doc in enumerate(docs):
    print(f"\nDocument {i+1}:")
    print(doc.page_content)

