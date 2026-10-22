from collections import defaultdict
from datetime import date
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select
from app.database import get_session
from app.models import Edition
from app.services.scheduler import run_daily_curation, get_current_date

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

MESES_PT = {
    1: "jan", 2: "fev", 3: "mar", 4: "abr", 5: "mai", 6: "jun",
    7: "jul", 8: "ago", 9: "set", 10: "out", 11: "nov", 12: "dez"
}

def format_date_pt(d: date) -> str:
    return f"{d.day:02d} de {MESES_PT.get(d.month, '')}"

@router.get("/")
def home(request: Request, session: Session = Depends(get_session)):
    today = get_current_date()
    edition = session.exec(select(Edition).where(Edition.edition_date == today)).first()

    grouped = defaultdict(list)
    if edition:
        for article in edition.articles:
            grouped[article.category].append(article)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "edition": edition,
        "grouped_articles": grouped,
        "today_formatted": format_date_pt(today)
    })

@router.get("/arquivo")
def archive(request: Request, session: Session = Depends(get_session)):
    editions = session.exec(select(Edition).order_by(Edition.edition_date.desc())).all()
    return templates.TemplateResponse("archive.html", {
        "request": request,
        "editions": editions
    })

@router.get("/edicao/{edition_date}")
def view_edition(edition_date: date, request: Request, session: Session = Depends(get_session)):
    edition = session.exec(select(Edition).where(Edition.edition_date == edition_date)).first()
    if not edition:
        raise HTTPException(status_code=404, detail="Edição não encontrada")

    grouped = defaultdict(list)
    for article in edition.articles:
        grouped[article.category].append(article)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "edition": edition,
        "grouped_articles": grouped,
        "today_formatted": format_date_pt(edition_date)
    })

@router.post("/api/trigger")
def trigger(force: bool = False):
    run_daily_curation(force=force)
    return {"status": "success", "message": "Curadoria executada com sucesso"}

@router.get("/api/health")
def health():
    return {"status": "ok"}
