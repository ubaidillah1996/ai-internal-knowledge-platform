# AI Internal Knowledge Platform
# API Design


# API Overview

The backend provides REST API endpoints using FastAPI.

The API handles:

- User authentication
- Document management
- AI knowledge retrieval
- Chat interaction
- Analytics


---

# Base URL

Development:

http://localhost:8000/api


---

# Authentication API


## Register User


Endpoint:

POST /auth/register


Purpose:

Create a new user account.


Request:


{
    "full_name": "Ali Ahmad",
    "email": "ali@email.com",
    "password": "password123"
}


Response:


{
    "message": "User created successfully"
}


---

## Login User


Endpoint:

POST /auth/login


Purpose:

Authenticate user and generate JWT token.


Request:


{
    "email": "ali@email.com",
    "password": "password123"
}


Response:


{
    "access_token": "jwt_token",
    "token_type": "bearer"
}


---

# Document Management API


## Upload Document


Endpoint:

POST /documents/upload


Purpose:

Upload company document.


Supported:

- PDF
- DOCX
- TXT


Flow:


Upload File

↓

Extract Text

↓

Split Text

↓

Generate Embedding

↓

Store Vector


Response:


{
    "message": "Document processed successfully"
}



---

## Get Documents


Endpoint:

GET /documents


Purpose:

Display available documents.


Response:


[
 {
    "id":1,
    "title":"HR Policy",
    "category":"HR"
 }
]


---

## Delete Document


Endpoint:

DELETE /documents/{document_id}


Purpose:

Remove document from knowledge base.



---

# AI Knowledge API


## Ask Question


Endpoint:

POST /chat/query


Purpose:

Ask AI questions based on company knowledge.


Request:


{
 "question":
 "What is the annual leave policy?"
}



Backend Flow:


User Question

↓

Convert question into embedding

↓

Search ChromaDB

↓

Retrieve relevant chunks

↓

Send context to LLM

↓

Generate answer



Response:


{
 "answer":
 "Employees receive 18 days annual leave.",

 "sources":[
    "HR_POLICY.pdf page 10"
 ]
}



---

# Chat History API


## Get Chat History


Endpoint:

GET /chat/history


Purpose:

Retrieve previous conversations.



---

# Feedback API


## Submit Feedback


Endpoint:

POST /feedback


Purpose:

Rate AI answer quality.


Request:


{
 "message_id":10,
 "rating":"positive"
}



---

# Admin API


## Dashboard Statistics


Endpoint:

GET /admin/statistics


Return:


- Total documents
- Total users
- Total questions
- Popular topics



---

# Future Agent API


## Agent Task


Endpoint:

POST /agent/task


Purpose:

Execute complex AI workflows.


Example:


User:

"Prepare employee onboarding guide"


Agent:


1. Search HR policy

2. Search IT setup guide

3. Search training document

4. Generate final report



---

# Security Requirements


All protected endpoints require:

JWT Authentication


Admin operations require:

Role validation


---

# API Design Principles


1. Clear endpoint naming

2. Separate business logic from routes

3. Validate all inputs

4. Return meaningful errors

5. Prepare for AI Agent expansion