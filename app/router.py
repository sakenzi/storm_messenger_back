from fastapi import APIRouter

from app.api.auth.auth_api import router as auth_router
from app.api.search.search_api import router as search_router
from app.api.friends.friend_api import router as friend_router


route = APIRouter()

route.include_router(auth_router, prefix="/auth", tags=["Authentication"])
route.include_router(search_router, prefix="/user_search", tags=["Search Users"])
route.include_router(friend_router, prefix="/friend", tags=["Friends"])
