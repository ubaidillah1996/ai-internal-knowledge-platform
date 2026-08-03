# AI Internal Knowledge Platform
# Database Design


# Database Overview

The system uses PostgreSQL as the primary relational database.

PostgreSQL stores structured information:

- Users
- Documents metadata
- Chat history
- User feedback
- System records


The vector database stores AI-related information:

- Document embeddings
- Semantic search vectors


---

# Database Architecture


PostgreSQL

Responsible for:

- Application data
- User management
- Document records
- Chat records


ChromaDB

Responsible for:

- Document embeddings
- Similarity search
- AI retrieval


---

# Entity Relationship Overview


Users

|

| 1:N

|

Documents

|

| 1:N

|

DocumentChunks


Users

|

| 1:N

|

ChatSessions

|

| 1:N

|

ChatMessages


---

# Tables


# 1. Users Table


Purpose:

Store user accounts and access control.


Fields:


id

- Primary Key
- UUID


email

- User email
- Unique


password_hash

- Encrypted password


full_name

- User name


role

Values:

- admin
- employee


created_at

- Account creation timestamp



---

# 2. Documents Table


Purpose:

Store uploaded document information.


Fields:


id

- Primary Key


title

- Document name


file_name

- Original filename


file_type

- PDF
- DOCX
- TXT


category

Examples:

- HR
- IT
- Finance
- Operations


uploaded_by

- User who uploaded document


created_at

- Upload timestamp



---

# 3. DocumentChunks Table


Purpose:

Store processed document sections.


Why:

Large documents cannot be sent directly to AI models.


Documents are split into smaller chunks.


Example:


Original:

HR_POLICY.pdf


After processing:


Chunk 1

"Annual leave policy..."


Chunk 2

"Medical claim policy..."


Fields:


id

- Primary Key


document_id

- Related document


chunk_text

- Extracted text


vector_id

- Reference to ChromaDB vector


created_at

- Timestamp



---

# 4. ChatSessions Table


Purpose:

Store conversation sessions.


Example:


User starts:

"HR Policy Question"


Creates one session.


Fields:


id

- Primary Key


user_id

- Owner


title

- Conversation title


created_at

- Timestamp



---

# 5. ChatMessages Table


Purpose:

Store individual messages.


Example:


User:

"What is annual leave?"


AI:

"Based on HR policy..."


Fields:


id

- Primary Key


session_id

- Related chat session


role

Values:

- user
- assistant


content

- Message text


sources

- Retrieved document references


created_at

- Timestamp



---

# 6. Feedback Table


Purpose:

Collect AI answer quality feedback.


Fields:


id

- Primary Key


message_id

- Related AI response


rating

Values:

- positive
- negative


comment

- User feedback


created_at

- Timestamp



---

# Future Enterprise Tables


## Departments


Purpose:

Separate knowledge access.


Example:


HR department

can access:

HR documents only.



## Permissions


Purpose:

Role based document access.



## AuditLogs


Purpose:

Track:

- Document uploads
- User actions
- AI requests



---

# Design Principles


1. PostgreSQL stores structured data.

2. Vector database stores AI embeddings.

3. Documents are processed before AI retrieval.

4. User access must be controlled.

5. Database design should support future AI Agent expansion.