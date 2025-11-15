from fastapi import FastAPI

from routers import activities, auth, comments, feed, followers, likes, stats

app = FastAPI(title="Striv API - Application de sport connectee", root_path="/proxy/5000")

# Inclusion des routers
app.include_router(auth.router)
app.include_router(activities.router)
app.include_router(likes.router)
app.include_router(comments.router)
app.include_router(followers.router)
app.include_router(stats.router)
app.include_router(feed.router)


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000)
