from pydantic import BaseModel


class AuthorizationData(BaseModel):
    account_id: int
    message: str
    code: int


class JWTTokens(BaseModel):
    access_token: str
    refresh_token: str