from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import posts, auth, users, comments

app = FastAPI(title="chyrp-rebuild")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth")
app.include_router(posts.router, prefix="/posts")
app.include_router(users.router, prefix="/users")
app.include_router(comments.router, prefix="/comments")
