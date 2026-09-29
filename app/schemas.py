from datetime import date

from pydantic import BaseModel, EmailStr, Field

from app.models import Status


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)


class UserOut(BaseModel):
    id: int
    email: EmailStr

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ApplicationCreate(BaseModel):
    company: str = Field(min_length=1, max_length=120)
    role: str = Field(min_length=1, max_length=120)
    status: Status = Status.applied
    source: str = Field(default="other", max_length=50)
    applied_on: date | None = None
    notes: str | None = None


class ApplicationUpdate(BaseModel):
    company: str | None = Field(default=None, min_length=1, max_length=120)
    role: str | None = Field(default=None, min_length=1, max_length=120)
    status: Status | None = None
    source: str | None = Field(default=None, max_length=50)
    applied_on: date | None = None
    notes: str | None = None


class ApplicationOut(BaseModel):
    id: int
    company: str
    role: str
    status: Status
    source: str
    applied_on: date
    notes: str | None

    model_config = {"from_attributes": True}
