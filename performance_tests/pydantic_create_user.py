from pydantic import BaseModel, EmailStr

class UserSchema(BaseModel):
    id: str
    email: EmailStr
    last_name: str
    first_name: str
    middle_name: str
    phone_number: str

class CreateUserRequestSchema(BaseModel):
    email: EmailStr
    last_name: str
    first_name: str
    middle_name: str
    phone_number: str

class CreateUserResponseSchema(BaseModel):
    user: UserSchema