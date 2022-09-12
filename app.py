import models
from database import SessionLocal, engine
from fastapi import Depends, FastAPI, Form, Request, status, Path, HTTPException
from scrapper import get_news
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates
import json
from typing import Optional, List
from pydantic import BaseModel

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

app = FastAPI()


class News(BaseModel):
    id: int
    title: str
    day: str
    checked: bool
    classification: Optional[str] = None

    class Config:
        orm_mode = True


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

# API
@app.get("/news", response_model=List[News], status_code=status.HTTP_200_OK)
def get_all_news(db: Session = Depends(get_db)):
    news = db.query(models.News).all()
    return news





@app.get("/get-by-day", response_model=List[News], status_code=status.HTTP_200_OK)
def get_one_day(
    day: str, classification: Optional[str] = None, db: Session = Depends(get_db)
):
    news_list = db.query(models.News).filter(models.News.day == day).all()
    return news_list


@app.post("/add", response_model=News, status_code=status.HTTP_201_CREATED)
def add_news(news: News, db: Session = Depends(get_db)):
    news = models.News(
        title=news.title,
        day=news.day,
        checked=news.checked,
        classification=news.classification,
    )

    db.add(news)
    db.commit()
    return news

# templates
@app.get("/data")
async def data(request: Request, db: Session = Depends(get_db)):
    news_list = db.query(models.News).all()
    return templates.TemplateResponse(
        "data.html", {"request": request, "news_list": news_list}
    )
    
@app.put("/update/{article_id}", response_model=News, status_code=status.HTTP_202_ACCEPTED)
def update(article_id: int, db: Session = Depends(get_db)):
    article = db.query(models.News).filter(models.News.id == article_id).first()
    article.checked = not article.checked
    db.commit()
    # db.refresh(article)
    url = app.url_path_for("data")
    return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)


@app.delete("/delete/{article_id}", response_model=News)
def delete(article_id: int, db: Session = Depends(get_db)):
    article = db.query(models.News).filter(models.News.id == article_id).first()
    db.delete(article)
    db.commit()

    url = app.url_path_for("data")
    return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)
