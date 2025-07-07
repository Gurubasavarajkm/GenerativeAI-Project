🤖 Document Chat Bot

An intelligent chatbot application that uses a Retrieval-Augmented Generation (RAG) pipeline with the Google Gemini API to answer questions based on the content of user-uploaded documents.

✨ Core Concept

This project demonstrates a powerful AI pattern called Retrieval-Augmented Generation (RAG). Instead of a generic chatbot that knows about everything on the internet, this bot's knowledge is strictly limited to the documents it has been given.
Here's the workflow:
Retrieval (R): When you ask a question, the system first searches through all the uploaded documents to find the most relevant snippets of text.
Augmentation (A): It then takes these relevant snippets and "augments" a prompt for the AI, essentially telling it: "Using only this information I found, please answer the user's question."
Generation (G): The Google Gemini model receives this detailed prompt and generates a concise, accurate answer based only on the provided context.
This approach eliminates "hallucinations" (made-up answers) and ensures that all responses are grounded in the source material, making it perfect for enterprise or personal knowledge base applications.

🚀 Features

Secure User Authentication: JWT-based authentication system with two distinct user roles.
Dual User Roles:
Admin: Can upload new documents (PDF, DOCX, XLSX, PPTX) and delete existing ones.
Normal User: Can only interact with the chatbot to ask questions.
Document Management: A dedicated admin dashboard for managing the knowledge base.
Intelligent Chat Interface: A clean, real-time chat UI for users to ask natural language questions.
Context-Aware Responses: The bot will clearly state if it cannot find an answer within the provided documents, preventing misinformation.
Powered by Google Gemini: Utilizes the gemini-pro model for generation and text-embedding-004 for creating semantic vector embeddings.
Fast and Modern Tech Stack: Built with FastAPI (Python) on the backend and React (Vite) on the frontend for a high-performance, responsive experience.

🛠️ Technology Stack

Backend: Python 3.11+, FastAPI, Uvicorn
Frontend: React 18+, Vite, Material-UI (MUI)
AI Service: Google Gemini API (gemini-pro, text-embedding-004)
Vector Database: ChromaDB (for efficient similarity search)
Document Parsing: pypdf, python-docx, openpyxl, python-pptx
Authentication: PyJWT (JSON Web Tokens)

📸 Screenshots

(You should replace these with your own screenshots)
Login Page	Admin Dashboard	Chat Interface
![alt text](path/to/your/login-screenshot.png)
![alt text](path/to/your/admin-screenshot.png)
![alt text](path/to/your/chat-screenshot.png)

⚙️ Setup and Installation

Follow these steps to get the project running on your local machine.

Prerequisites

Python 3.11+
Node.js v18+ and npm
Git
