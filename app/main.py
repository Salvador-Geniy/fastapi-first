from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from routers import users, posts, auth, vote

app = FastAPI(
    title='FastAPI third.',
    description='This is my third fastapi framework project '
                'to have some experience with it.'
)


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(users.user_router)
app.include_router(posts.post_router)
app.include_router(auth.auth_router)
app.include_router(vote.vote_router)


@app.get('/')
def say_hello():
    return {"message": "Hello, world!"}
