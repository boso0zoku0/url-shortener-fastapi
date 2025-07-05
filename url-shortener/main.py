from dns.e164 import query
from fastapi import FastAPI, Request

app = FastAPI(title="URL Shortener")


@app.get("/")
def qqw(request: Request, name: str):
    data = request.url.replace(path="/docs", query="")
    return {"Hello": str(name), "data": data}
