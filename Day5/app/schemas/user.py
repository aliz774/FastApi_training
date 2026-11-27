from pydantic import BaseModel, ConfigDict, EmailStr, Field

# pip install fastapi uvicorn "email-validator" "pwdlib[argon2]"

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: str


class UserUpdate(BaseModel):
    full_name: str | None = None


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    full_name: str
    role: str