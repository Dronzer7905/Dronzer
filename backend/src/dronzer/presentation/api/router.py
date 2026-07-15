from fastapi import APIRouter

from dronzer.presentation.api.v1 import chat, embeddings, images, models

# Global v1 router
v1_router = APIRouter(prefix="/v1")

# Mount sub-routers
v1_router.include_router(chat.router)
v1_router.include_router(models.router)
v1_router.include_router(embeddings.router)
v1_router.include_router(images.router)
