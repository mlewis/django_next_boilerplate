"""Main Django Ninja API — registers all routers."""

from ninja import NinjaAPI
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.routers.obtain import obtain_pair_router
from ninja_jwt.routers.verify import verify_router

from apps.items.api import router as items_router

api = NinjaAPI(
    title="Hackathon API",
    version="1.0.0",
    description="Django Ninja + Next.js boilerplate API",
    auth=JWTAuth(),
    urls_namespace="api",
)

# JWT auth endpoints:
#   POST /api/auth/pair    — obtain access + refresh tokens
#   POST /api/auth/refresh — refresh access token
#   POST /api/auth/verify  — verify token validity
api.add_router("/auth", obtain_pair_router, auth=None, tags=["auth"])
api.add_router("/auth", verify_router, auth=None, tags=["auth"])

# Domain routers
api.add_router("/items", items_router)
