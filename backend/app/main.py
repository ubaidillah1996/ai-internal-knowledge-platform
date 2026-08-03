from fastapi import FastAPI


app = FastAPI(
    title="AI Internal Knowledge Platform API",
    version="0.1.0"
)


@app.get("/")
def root():
    return {
        "message": "AI Knowledge Platform API Running"
    }