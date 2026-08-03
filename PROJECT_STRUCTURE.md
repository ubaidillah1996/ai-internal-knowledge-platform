# AI Internal Knowledge Platform - Project Structure


## Overview

The project follows a modular architecture separating:

- Frontend application
- Backend API
- AI processing layer
- Database layer
- Documentation

ai-internal-knowledge-platform/

│
├── backend/
│
│   ├── app/
│   │
│   │   ├── main.py
│   │   │
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   └── database.py
│   │   │
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── document.py
│   │   │   └── chat.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── user_schema.py
│   │   │   ├── document_schema.py
│   │   │   └── chat_schema.py
│   │   │
│   │   ├── routers/
│   │   │   ├── auth.py
│   │   │   ├── documents.py
│   │   │   └── chat.py
│   │   │
│   │   ├── services/
│   │   │   ├── document_service.py
│   │   │   ├── embedding_service.py
│   │   │   └── rag_service.py
│   │   │
│   │   └── utils/
│   │       └── helpers.py
│   │
│   ├── migrations/
│   │
│   ├── requirements.txt
│   │
│   └── .env
│
│
├── frontend/
│
│   ├── src/
│   │
│   │   ├── components/
│   │   │   ├── Navbar.jsx
│   │   │   ├── ChatBox.jsx
│   │   │   └── DocumentCard.jsx
│   │   │
│   │   ├── pages/
│   │   │   ├── Login.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   └── KnowledgeChat.jsx
│   │   │
│   │   ├── services/
│   │   │   └── api.js
│   │   │
│   │   └── App.jsx
│   │
│   └── package.json
│
│
├── ai/
│
│   ├── ingestion/
│   │   ├── document_loader.py
│   │   ├── text_splitter.py
│   │   └── processor.py
│   │
│   ├── embeddings/
│   │   └── embedding_model.py
│   │
│   ├── retrieval/
│   │   ├── vector_store.py
│   │   └── retriever.py
│   │
│   └── agents/
│       ├── knowledge_agent.py
│       └── workflow_agent.py
│
│
├── documents/
│   └── sample_company_docs/
│
│
├── tests/
│
│
├── docs/
│   ├── architecture.md
│   ├── api_design.md
│   └── database_design.md
│
│
├── PROJECT_CONTEXT.md
├── PROJECT_ROADMAP.md
├── PROJECT_STRUCTURE.md
└── README.md
