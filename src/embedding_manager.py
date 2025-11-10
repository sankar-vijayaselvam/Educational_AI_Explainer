from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=200)
print("Initialized Recursive Character Text Splitter...")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
print("Initialized Huggingface Embedding model...")

def embedding_creator(pdf_text_data):


    # Split the text into no of Chunks
    pdf_text_chunks = splitter.split_text(pdf_text_data)
    print(f"Split PDF text into {len(pdf_text_chunks)} chunks.")

    # Embeddings will be created using the text chunks and stored it in vector db
    chroma_db = Chroma.from_texts(
    texts=pdf_text_chunks,
    embedding=embeddings,
    persist_directory="./vectorstore" # Store the vector index locally
    )
    print("The Embeddings will be Created and Store in Chroma dB")

    # Initilize the db retriever
    pdf_retriever = chroma_db.as_retriever(search_kwargs={"k": 2}) # Retrieve top 2 chunks
    print("ChromaDB vector store created and ready. Initialize the db retriever")

    return pdf_retriever



