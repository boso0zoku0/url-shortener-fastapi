from fastapi import APIRouter, HTTPException, status
from schemas.films import Films
from .crud import FILMS

router = APIRouter(prefix="/films", tags=["Films"])


@router.get("/", response_model=list[Films])
def show_firms():
    return FILMS


@router.get("/{name}", response_model=Films)
def show_film_by_name(name: str):
    film: Films = next((film for film in FILMS if film.name == name), None)
    if film:
        return film
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Film {name!r} not found"
    )


@router.get("/{slug}", response_model=Films)
def show_film_by_slug(slug: str):
    film: Films = next((film for film in FILMS if film.slug == slug), None)
    if film:
        return film
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Film {slug!r} not found"
    )
