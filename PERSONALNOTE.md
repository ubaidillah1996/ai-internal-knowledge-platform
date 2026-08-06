Architecture Principle
Backend

Responsible for:

API
Authentication
Database operation
Business logic
AI Layer

Responsible for:

Document processing
Embeddings
Retrieval
RAG pipeline
Agent workflow
Frontend

Responsible for:

User interface
User interaction
Dashboard

Development Rule

Never mix:

Frontend logic
with

Backend logic
with

AI processing logic.

Each layer should have clear responsibility.

Future Expansion

The architecture supports:

Multiple AI agents
Department knowledge bases
Advanced workflows
Enterprise integrations

FLOW ARCHITECTURE :

Idea
 ↓
Requirement
 ↓
Architecture
 ↓
Folder Design
 ↓
Database Design
 ↓
API Design
 ↓
Coding

ASSIST.. :

Ubai
 |
 |-- ChatGPT
 |      ├── Architecture
 |      ├── Explain
 |      ├── Debug
 |      └── Review
 |
 |-- VS Code
 |      ├── Write code
 |      ├── Run project
 |      └── Git
 |
 |-- Claude Free (Browser)
        ├── Second opinion
        ├── Review code
        └── Alternative solution

{
  "email": "admin@test.com",
  "password": "hello123"
}

{
 "username":"testuser",
 "email":"test@test.com",
 "password":"123456"
}

eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkB0ZXN0LmNvbSIsImV4cCI6MTc4NTgyOTE5NH0.XxVDU6j62sy0-cDQKxYPjjPS7rgADWQMM8dbCpO2yBQ

.\venv\Scripts\Activate.ps1

psql -U postgres
\c ai_knowledge_db

python -m uvicorn app.main:app --reload

{
  "conversation_id":1,
  "query":"How many annual leave days do employees receive?"
}