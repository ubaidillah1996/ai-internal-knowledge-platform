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

@router.delete("/{document_id}")
def delete_document(

    document_id: int,

    db: Session = Depends(get_db),

    current_user: User = Depends(get_current_user)

):


    document = (

        db.query(Document)

        .filter(

            Document.id == document_id

        )

        .first()

    )


    if not document:

        raise HTTPException(

            status_code=404,

            detail="Document not found"

        )


    if document.uploaded_by != current_user.id:

        raise HTTPException(

            status_code=403,

            detail="Not allowed"

        )


    # get chunk ids

    chunk_ids = [

        chunk.id

        for chunk in document.chunks

    ]


    # delete chroma vectors

    if chunk_ids:

        delete_embedding(

            chunk_ids

        )


    # delete file

    if os.path.exists(

        document.file_path

    ):

        os.remove(

            document.file_path

        )

    chunk_ids = [
        chunk.id
        for chunk in document.chunks
    ]


    if chunk_ids:

        delete_embedding(
            chunk_ids
        )

    if os.path.exists(document.file_path):

        os.remove(
            document.file_path
        )

    # delete database

    db.delete(

        document

    )


    db.commit()


    return {

        "message":

        "Document deleted successfully",

        "deleted_chunks":

        len(chunk_ids)

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

    try:

        # 1. delete old embeddings

        old_chunk_ids = [

            chunk.id

            for chunk in document.chunks

        ]

        print(
            "OLD CHUNK IDS:",
            old_chunk_ids
        )

    
        if old_chunk_ids:

            delete_embedding(
                old_chunk_ids
            )

        # 2. delete old chunks

        for chunk in document.chunks:

            db.delete(chunk)


        db.commit()

        # 3. save new file

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

        # 4. update document information

        document.filename = file.filename

        document.file_path = file_path

        document.title = file.filename

        db.commit()
        db.refresh(document)

        # 5. extract text from new PDF

        doc = fitz.open(
            document.file_path
        )


        text = ""


        for page in doc:

            text += page.get_text()

        if not text.strip():

            raise HTTPException(

                status_code=400,

                detail="PDF contains no readable text"

            )

        document.content = text


        db.commit()
        db.refresh(document)

        # 6. create new chunks

        chunks = create_chunks(text)

        for index, chunk in enumerate(chunks):

            document_chunk = DocumentChunk(

                document_id=document.id,

                content=chunk,

                chunk_index=index

            )


            db.add(document_chunk)


        db.commit()

        

        db.refresh(document)

        # 7. recreate embeddings

        for chunk in document.chunks:

            print(
                "CHUNK TYPE:",
                type(chunk),
                "CONTENT TYPE:",
                type(chunk.content)
            )
            


            try:

                embedding = create_embedding(chunk.content)


                store_embedding(

                    chunk_id=document_chunk.id,

                    embedding=embedding,

                    text=chunk.content,

                    metadata={

                        "document_id": document.id,

                        "filename": document.filename,

                        "chunk_index": chunk.chunk_index

                    }

                )


            except Exception as e:

                print("EMBEDDING ERROR:", e)

                raise HTTPException(
                    status_code=500,
                    detail=str(e)
                )

            db.commit()

        return {
            "message": "Document updated successfully",
            "document_id": document.id,
            "chunks": len(document.chunks)
        }


    except Exception as e:

        db.rollback()

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

    pass
    

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



    chunks = create_chunks(text)


    for index, chunk in enumerate(chunks):

        document_chunk = DocumentChunk(

            document_id=new_document.id,

            content=chunk,

            chunk_index=index

        )


        db.add(document_chunk)

        db.commit()

        db.refresh(document_chunk)


        try:

            embedding = create_embedding(chunk)


            store_embedding(

                chunk_id=document_chunk.id,

                embedding=embedding,

                text=chunk,

                metadata={

                    "document_id": new_document.id,

                    "filename": file.filename,

                    "chunk_index": index

                }

            )


        except Exception:

            raise HTTPException(

                status_code=500,

                detail="Failed to create document embedding"

            )

    return new_document

