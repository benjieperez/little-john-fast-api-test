from pydantic import BaseModel, EmailStr
from tortoise import fields
from tortoise.models import Model

# User ORM Model
class UsersModel(Model):
    id = fields.IntField(primary_key=True, auto_increment=True)
    name = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255, unique=True)
    picture_url = fields.CharField(max_length=512)
    class Meta:
        table = "users"

# Pydantic model for validating incoming user data
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    picture_url: str
    token: str

# Pydantic model for mocking Google OAuth response
class GoogleOAuthResponse(BaseModel):
    name: str
    email: str
    picture_url: str
    token: str  # This can be the token or OAuth response data