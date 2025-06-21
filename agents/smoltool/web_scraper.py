# List of useful URLs
import requests
from bs4 import BeautifulSoup
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter

URLS = [
    "https://orthoinfo.aaos.org/en/diseases--conditions/hand-fractures",
    "https://www.factdr.com/health-conditions/hand-fracture",
    "https://en.wikipedia.org/wiki/Broken_finger",
    "https://en.wikipedia.org/wiki/Scaphoid_fracture",
    "https://www.orthonet.on.ca/2025/03/hand-fractures-types-treatments-and-what-to-expect",
    "https://www.spirehand.com.sg/types-of-hand-fractures-what-you-need-to-know",
    "https://radiopaedia.org/articles/metacarpal-fracture-2",
    "https://radiopaedia.org/articles/fractures-of-the-thumb?lang=us",
    "https://radiopaedia.org/articles/phalanx-fracture",
    "https://radiopaedia.org/articles/avulsion-injury-1"
    "https://pressbooks.bccampus.ca/pathophysiology/chapter/bone-fractures",
    "https://tagvault.org/blog/types-of-fractures-2/",
    "https://southshoreorthopedics.com/common-types-of-bone-fractures",
    "https://www.ncbi.nlm.nih.gov/books/NBK513279/#:~:text=Pathophysiology-,A%20greenstick%20fracture%20is%20a%20partial%20thickness%20fracture%20where%20only,radius%2C%20humerus%2C%20and%20clavicle."
    "https://my.clevelandclinic.org/health/diseases/22956-transverse-fracture",
    "https://my.clevelandclinic.org/health/diseases/22241-spiral-fracture",
    "https://my.clevelandclinic.org/health/diseases/17812-greenstick-fractures",
    "https://my.clevelandclinic.org/health/diseases/15841-stress-fractures",
    "https://my.clevelandclinic.org/health/diseases/21950-compression-fractures",
    "https://my.clevelandclinic.org/health/diseases/22185-oblique-fracture",
    "https://amicuslegalgroup.com/faqs/what-is-an-impacted-fracture-and-how-is-it-treated/"
    "https://my.clevelandclinic.org/health/diseases/22234-segmental-fracture",
    "https://my.clevelandclinic.org/health/diseases/22252-comminuted-fracture",
    "https://my.clevelandclinic.org/health/diseases/21802-avulsion-fracture"
]

def get_page_text(url):
    print(f"Scraping: {url}")
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, "html.parser")

    # Extract all visible text
    paragraphs = soup.find_all("p")
    text = "\n".join([p.get_text().strip() for p in paragraphs])
    return text

# Step 1: Collect and combine content
documents = []
for url in URLS:
    text = get_page_text(url)
    documents.append({"source": url, "content": text})


# Step 2: Split into chunks
# Split documents into smaller chunks for better retrieval
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,  # Characters per chunk
    chunk_overlap=100,  # Overlap between chunks to maintain context
    add_start_index=True,
    strip_whitespace=True,
    separators=["\n\n", "\n", ".", " ", ""],  # Priority order for splitting
)
all_texts = []
for doc in documents:
    splits = text_splitter.split_text(doc["content"])
    for split in splits:
        all_texts.append({
            "text": split,
            "metadata": {"source": doc["source"]}
        })



texts = [x["text"] for x in all_texts]
metadatas = [x["metadata"] for x in all_texts]

model_name = "sentence-transformers/all-mpnet-base-v2"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': False}
embeddings = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)

vectorstore = FAISS.from_texts(texts, embedding=embeddings, metadatas=metadatas)

# Save index to disk (optional)
vectorstore.save_local("hand_fracture_faiss_index")

print("✅ Data scraped and indexed for RAG.")