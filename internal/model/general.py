from pydantic import BaseModel


class AuthorizationData(BaseModel):
    account_id: int
    two_fa_status: bool
    role: str
    message: str
    status_code: int


class JWTTokens(BaseModel):
    access_token: str
    refresh_token: str