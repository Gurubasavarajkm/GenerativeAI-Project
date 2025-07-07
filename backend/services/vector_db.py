import google.generativeai as genai
from langchain.text_splitter import RecursiveCharacterTextSplitter
import chromadb
import os
from dotenv import load_dotenv

load_dotenv()

# Configure and get Gemini API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Setup ChromaDB client
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("docu_mind_collection")

def add_document_to_db(text: str, doc_id: str):
    if not text.strip():
        print(f"Skipping empty document: {doc_id}")
        return

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = text_splitter.split_text(text)
    
    # Generate embeddings for each chunk
    try:
        result = genai.embed_content(model="models/text-embedding-004",
                                     content=chunks,
                                     task_type="retrieval_document")
    except Exception as e:
        print(f"Error embedding document {doc_id}: {e}")
        return

    # Store in ChromaDB
    collection.add(
        embeddings=result['embedding'],
        documents=chunks,
        metadatas=[{"source": doc_id} for _ in chunks],
        ids=[f"{doc_id}_{i}" for i in range(len(chunks))]
    )
    print(f"Successfully added {len(chunks)} chunks for document {doc_id}")

def query_relevant_chunks(query: str):
    try:
        query_embedding = genai.embed_content(model="models/text-embedding-004",
                                              content=query,
                                              task_type="retrieval_query")['embedding']
    except Exception as e:
        print(f"Error embedding query: {e}")
        return []

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5  # Get top 5 most relevant chunks
    )
    return results['documents'][0]

def generate_answer_from_context(context: list[str], query: str) -> str:
    if not context:
        return "I'm sorry, I couldn't find any relevant information in the uploaded documents to answer your question."

    context_str = "\n---\n".join(context)
    
    prompt = f"""
    You are a helpful AI assistant for the 'DocuMind' application. Your task is to answer user questions based *only* on the context provided from a set of documents.
    Do not use any external knowledge. If the answer is not found in the context, say "I'm sorry, I couldn't find information about that in the documents."

    CONTEXT:
    {context_str}

    QUESTION:
    {query}

    ANSWER:
    """

    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text

def delete_document_from_db(doc_id: str):
    collection.delete(where={"source": doc_id})
    print(f"Deleted document {doc_id} from vector store.")

def get_all_documents():
    # This is an inefficient way for large DBs, but fine for a case study
    all_items = collection.get(include=["metadatas"])
    sources = set(item['source'] for item in all_items['metadatas'])
    return list(sources)