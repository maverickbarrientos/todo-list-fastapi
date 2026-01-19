from fastapi import Request, Response, Depends
from fastapi_users.authentication import AuthenticationBackend, JWTStrategy, BearerTransport
from fastapi_users import BaseUserManager, FastAPIUsers, IntegerIDMixin
from typing import Optional

from db.base import User, get_user_db

SECRET_KEY = "mySecretKey12345"

class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    verification_token_secret = SECRET_KEY
    reset_password_token_secret = SECRET_KEY
    
    async def on_after_register(self, user: User, request: Optional[Request]):
        print(f"{user.id} has been registered")
    
    async def on_after_login(self, user: User, request: Optional[Request], response: Response):
        print(f"{user.id} logged in")
    
    async def on_after_request_verify(self, user: User, token: str, request: Request):
        print(f"Verification request from {user.id}. Verification token {token}")
        
def get_user_manager(user_db = Depends(get_user_db)):
    yield(UserManager(user_db))
        
bearer = BearerTransport(tokenUrl="/auth/jwt/login")
def get_strategy():
    return JWTStrategy(secret=SECRET_KEY, lifetime_seconds=3600)    

auth_backend = AuthenticationBackend(name="jwt", transport=bearer, get_strategy=get_strategy)
fastapi_users = FastAPIUsers[User, int](get_user_manager, auth_backends=[auth_backend])
current_active_user = fastapi_users.current_user(active=True)