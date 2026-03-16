from pydantic import BaseModel,EmailStr,Field

class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(
        min_length=5,
        max_length=10
    )

class UserUpdate(BaseModel):
    email: EmailStr | None = None
    username : str | None = Field(
        default=None,
        min_length=5,
        max_length=10
    )

class UserOut(BaseModel):
    id:int
    email:EmailStr
    username:str

    class Config:
        from_attribute = True