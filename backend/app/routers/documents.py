from email.mime import text

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.core.database import get_db
from app.core.auth import get_current_user

from app.models.document import Document
from app.models.user import User

from app.schemas.document import (
    DocumentResponse,
    DocumentDetailResponse,
    DocumentListResponse
)

import os

from fastapi import UploadFile, File
import fitz

from app.services.chunking import create_chunks

from app.models.document_chunk import DocumentChunk

from app.services.embedding import create_embedding
from app.services.vector_store import (
    store_embedding,
    delete_embedding
)
from app.core.logger import logger

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

@router.get(
    "/",
    response_model=list[DocumentDetailResponse]
)
def get_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    documents = (
        db.query(Document)
        .filter(
            Document.uploaded_by == current_user.id
        )
        .all()
    )


    return [

        {
            "id": document.id,

            "title": document.title,

            "filename": document.filename,

            "uploaded_by": document.uploaded_by,

            "total_chunks": len(document.chunks),

            "status": "indexed",

            "created_at": document.created_at,

            "updated_at": document.updated_at
        }

        for document in documents

    ]

@router.get("/{document_id}")
def get_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    document = (
        db.query(Document)
        .filter(
            Document.id == document_id,
            Document.uploaded_by == current_user.id
        )
        .first()
    )


    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )


    return {
        "id": document.id,
        "title": document.title,
        "filename": document.filename,
        "uploaded_by": document.uploaded_by,
        "created_at": document.created_at,
        "total_chunks": len(document.chunks),
        "status": "indexed",
        "updated_at": document.updated_at
    }


@router.put("/{document_id}")
def update_document(
    document_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    document = (
        db.query(Document)
        .filter(
            Document.id == document_id,
            Document.uploaded_by == current_user.id
        )
        .first()
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    try:

        # 1. Delete old embeddings

        old_chunk_ids = [
            chunk.id
            for chunk in document.chunks
        ]

        logger.info(
            f"OLD CHUNK IDS: {old_chunk_ids}"
        )

        if old_chunk_ids:
            delete_embedding(old_chunk_ids)


        # 2. Delete old chunks

        for chunk in document.chunks:
            db.delete(chunk)

        db.commit()


        # 3. Save new PDF

        upload_folder = "uploads"

        os.makedirs(
            upload_folder,
            exist_ok=True
        )

        file_path = f"{upload_folder}/{file.filename}"

        with open(file_path, "wb") as buffer:
            buffer.write(
                file.file.read()
            )


        # 4. Extract text

        doc = fitz.open(file_path)

        text = ""

        for page in doc:
            text += page.get_text()

        doc.close()

        if not text.strip():
            raise HTTPException(
                status_code=400,
                detail="PDF contains no readable text"
            )


        logger.info(
            f"Extracted text length: {len(text)}"
        )


        # 5. Update document information

        document.filename = file.filename

        document.file_path = file_path

        document.title = file.filename

        document.content = text

        db.commit()

        db.refresh(document)


        # 6. Create new chunks

        chunks = create_chunks(text)

        logger.info(
            f"Number of chunks created: {len(chunks)}"
        )


        document_chunks = []


        for index, chunk in enumerate(chunks):

            logger.info(
                f"Chunk {index}: {len(chunk)} characters"
            )

            document_chunk = DocumentChunk(

                document_id=document.id,

                content=chunk,

                chunk_index=index

            )

            db.add(document_chunk)

            document_chunks.append(
                document_chunk
            )


        db.commit()


        # Refresh each newly created chunk
        for document_chunk in document_chunks:

            db.refresh(document_chunk)


        # 7. Create new embeddings

        stored_chunk_ids = []


        for document_chunk in document_chunks:

            logger.info(
                f"Creating embedding for chunk {document_chunk.id}"
            )

            try:

                embedding = create_embedding(
                    document_chunk.content
                )


                store_embedding(

                    chunk_id=document_chunk.id,

                    embedding=embedding,

                    text=document_chunk.content,

                    metadata={

                        "document_id": document.id,

                        "filename": document.filename,

                        "chunk_index": document_chunk.chunk_index

                    }

                )


                stored_chunk_ids.append(
                    document_chunk.id
                )


            except Exception as e:

                logger.error(
                    f"EMBEDDING ERROR: {e}"
                )

                raise HTTPException(
                    status_code=500,
                    detail="Failed to create document embedding"
                )


        logger.info(
            f"Stored embeddings: {len(stored_chunk_ids)}"
        )


        return {

            "message": "Document updated successfully",

            "document_id": document.id,

            "filename": document.filename,

            "chunks": len(document_chunks)

        }


    except HTTPException:
        db.rollback()
        raise


    except Exception as e:

        db.rollback()

        logger.error(
            f"Document update failed: {e}"
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.delete("/{document_id}")
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    document = (
        db.query(Document)
        .filter(
            Document.id == document_id,
            Document.uploaded_by == current_user.id
        )
        .first()
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    chunk_ids = [
        chunk.id
        for chunk in document.chunks
    ]

    logger.info(
        f"Document {document_id} chunk IDs: {chunk_ids}"
    )
    

@router.post("/upload")
def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    existing_document = db.query(Document).filter(
        Document.filename == file.filename,
        Document.uploaded_by == current_user.id
    ).first()

    if existing_document:
        raise HTTPException(
            status_code=400,
            detail="This document has already been uploaded"
        )   

    upload_folder = "uploads"

    os.makedirs(
        upload_folder,
        exist_ok=True
    )


    file_path = f"{upload_folder}/{file.filename}"


    with open(file_path, "wb") as buffer:

        buffer.write(
            file.file.read()
        )


    try:

        doc = fitz.open(file_path)


        text = ""


        for page in doc:

            text += page.get_text()

        if not text.strip():

            raise HTTPException(

                status_code=400,

                detail="PDF contains no readable text"

            )

    except Exception:

        raise HTTPException(

            status_code=400,

            detail="Unable to read PDF file"

        )


    new_document = Document(

        title=file.filename,

        filename=file.filename,

        file_path=file_path,

        content=text,

        uploaded_by=current_user.id
    )


    db.add(new_document)

    db.commit()

    db.refresh(new_document)



    # Create chunks

    chunks = create_chunks(text)


    # Create database chunks

    document_chunks = []


    for index, chunk in enumerate(chunks):

        document_chunk = DocumentChunk(

            document_id=new_document.id,

            content=chunk,

            chunk_index=index

        )

        db.add(document_chunk)

        document_chunks.append(document_chunk)


    # Commit all chunks once

    db.commit()


    # Refresh chunks to get their database IDs

    for document_chunk in document_chunks:

        db.refresh(document_chunk)


    # Create embeddings

    for document_chunk in document_chunks:

        try:

            embedding = create_embedding(
                document_chunk.content
            )


            store_embedding(

                chunk_id=document_chunk.id,

                embedding=embedding,

                text=document_chunk.content,

                metadata={

                    "document_id": new_document.id,

                    "filename": file.filename,

                    "chunk_index": document_chunk.chunk_index

                }

            )

        except Exception as e:

            logger.error(
                f"Embedding failed: {e}"
            )


            # Delete database chunks

            for document_chunk in document_chunks:

                db.delete(document_chunk)


            # Delete document

            db.delete(new_document)


            db.commit()


            raise HTTPException(

                status_code=500,

                detail="Failed to create document embedding"

            )




