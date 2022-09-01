from http import HTTPStatus

import validators
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from starlette.datastructures import URL

from . import crud, models, schemas
from .config import get_settings
from .database import SessionLocal, engine

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def get_admin_info(db_url: models.URL) -> schemas.URLInfo:
    base_url = URL(get_settings().base_url)
    admin_endpoint = app.url_path_for("admin info", secret_key=db_url.secret_key)
    db_url.url = str(base_url.replace(path=db_url.key))
    db_url.admin_url = str(base_url.replace(path=admin_endpoint))
    return db_url


def raise_bad_request(message: str):
    raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=message)


def raise_not_found(request: Request):
    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND, detail=f"URL '{request.url}' does not exist"
    )


@app.get("/")
async def read_root():
    return "Welcome to the URL shortener API :)"


@app.post("/url", response_model=schemas.URLInfo)
async def create_url(url: schemas.URLBase, db: Session = Depends(get_db)):
    if not validators.url(url.target_url):
        raise_bad_request(message="Your URL is invalid")

    db_url = crud.create_db_url(db=db, url=url)
    return get_admin_info(db_url)


@app.get("/{url_key}")
def forward_to_target_url(
    url_key: str, request: Request, db: Session = Depends(get_db)
):
    if not (db_url := crud.get_db_url_by_key(db=db, url_key=url_key)):
        raise_not_found(request=request)

    crud.update_db_clicks(db, db_url)
    return RedirectResponse(db_url.target_url)


@app.get("/admin/{secret_key}", name="admin info", response_model=schemas.URLInfo)
def get_url_info(secret_key: str, request: Request, db: Session = Depends(get_db)):
    if not (db_url := crud.get_db_url_by_secret_key(db, secret_key)):
        raise_not_found(request)

    return get_admin_info(db_url)


@app.delete("/admin/{secret_key}")
def delete_url(secret_key: str, request: Request, db: Session = Depends(get_db)):
    if not (db_url := crud.deactivate_db_url_by_secret_key(db, secret_key)):
        raise_not_found(request)

    return {"detail": f"Shortened URL for '{db_url.target_url}' is deleted"}
