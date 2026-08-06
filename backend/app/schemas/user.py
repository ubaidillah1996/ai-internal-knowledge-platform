from pydantic import BaseModel, EmailStr

class UserLogin(BaseModel):

    email: EmailStr
    password: str

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True