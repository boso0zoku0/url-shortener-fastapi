from typing import Annotated


from fastapi import FastAPI, Request, status, HTTPException, Depends, Query
from fastapi.responses import RedirectResponse
from pydantic import HttpUrl

from schemas.short_url import ShortUrl
from schemas.films import *

app = FastAPI(title="URL Shortener")

SHORT_URLS = [
    ShortUrl(target_url="http://google.com", slug="google"),
    ShortUrl(target_url="http://yandex.ru", slug="yandex"),
]

FILMS = [
    Films(
        id=1,
        name="Криминальное чтиво",
        description="Нелинейная криминальная драма",
        year_release=1994,
    ),
    Films(
        id=2,
        name="Интерстеллар",
        description="Космическая одиссея о спасении человечества",
        year_release=2014,
    ),
    Films(
        id=3,
        name="Матрица",
        description="Реальность иллюзия виртуального мира",
        year_release=1999,
    ),
]


def prefetch_url(slug: str):
    url: ShortUrl = next((url for url in SHORT_URLS if url.slug == slug), None)
    if url:
        return RedirectResponse(url=url.target_url)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"URL {slug!r} not found"
    )


@app.get("/")
def root(request: Request):
    data = request.url.replace(path="/docs", query="")
    return {"Hello": "Y", data: data}


@app.get("/r/{slug}/")
def redirect(url: Annotated[ShortUrl, Depends(prefetch_url)]):
    return url


@app.get("/short-urls/")
def urls():
    return SHORT_URLS


@app.get("/short-url/{slug}")
def show_url(slug: str):
    url: ShortUrl = next((url for url in SHORT_URLS if url.slug == slug), None)
    if url:
        return url
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"URL {slug!r} not found"
    )


@app.get("/firms/", response_model=list[Films])
def show_firms():
    return FILMS


@app.get("/film/{idx}", response_model=Films)
def show_film_by_id(idx: int):
    film: Films = next((film for film in FILMS if film.id == idx), None)
    if film:
        return film
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Film {id!r} not found"
    )


@app.get("/film/{name}", response_model=Films)
def show_film_by_name(name: str):
    film: Films = next((film for film in FILMS if film.name == name), None)
    if film:
        return film
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Film {name!r} not found"
    )
