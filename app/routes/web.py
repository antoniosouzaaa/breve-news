from collections import defaultdict
from datetime import date
from fastapi import APIRouter, Request, Depends, HTTPException, BackgroundTasks
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select
from app.database import get_session
from app.models import Edition
from app.services.scheduler import run_daily_curation, get_current_date, is_curating

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

MESES_PT = {
    1: "jan", 2: "fev", 3: "mar", 4: "abr", 5: "mai", 6: "jun",
    7: "jul", 8: "ago", 9: "set", 10: "out", 11: "nov", 12: "dez"
}

MESES_PT_EXTENSO = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril", 5: "Maio", 6: "Junho",
    7: "Julho", 8: "Agosto", 9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
}

def format_date_pt(d: date) -> str:
    return f"{d.day:02d} de {MESES_PT.get(d.month, '')}"

def format_date_full_pt(d: date) -> str:
    return f"{d.day:02d} de {MESES_PT_EXTENSO.get(d.month, '')}"

ORDERED_CATEGORIES = ["cultura", "economia", "f1", "design", "geral"]

def sort_grouped_articles(grouped_dict):
    ordered = {}
    for cat in ORDERED_CATEGORIES:
        if cat in grouped_dict and grouped_dict[cat]:
            ordered[cat] = grouped_dict[cat]
    for cat, items in grouped_dict.items():
        if cat not in ordered and items:
            ordered[cat] = items
    return ordered

@router.get("/")
def home(request: Request, session: Session = Depends(get_session)):
    today = get_current_date()
    edition = session.exec(select(Edition).where(Edition.edition_date == today)).first()

    grouped = defaultdict(list)
    articles_list = []
    if edition:
        articles_list = edition.articles
        for article in articles_list:
            grouped[article.category].append(article)

    sorted_grouped = sort_grouped_articles(grouped)
    total_articles = len(articles_list)
    reading_time = max(2, round(total_articles * 0.7)) if total_articles else 3

    return templates.TemplateResponse("index.html", {
        "request": request,
        "edition": edition,
        "grouped_articles": sorted_grouped,
        "total_articles": total_articles,
        "reading_time": reading_time,
        "today_formatted": format_date_pt(today),
        "today_formatted_full": format_date_full_pt(today)
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
    articles_list = edition.articles
    for article in articles_list:
        grouped[article.category].append(article)

    sorted_grouped = sort_grouped_articles(grouped)
    total_articles = len(articles_list)
    reading_time = max(2, round(total_articles * 0.7)) if total_articles else 3

    return templates.TemplateResponse("index.html", {
        "request": request,
        "edition": edition,
        "grouped_articles": sorted_grouped,
        "total_articles": total_articles,
        "reading_time": reading_time,
        "today_formatted": format_date_pt(edition_date),
        "today_formatted_full": format_date_full_pt(edition_date),
        "is_past_edition": True
    })

@router.post("/api/trigger")
def trigger(background_tasks: BackgroundTasks, force: bool = False):
    if is_curating():
        return {"status": "already_running", "message": "Curadoria já está em andamento."}
    background_tasks.add_task(run_daily_curation, force=force)
    return {"status": "started", "message": "Curadoria iniciada com sucesso em segundo plano."}

@router.get("/api/status")
def status():
    return {"is_curating": is_curating()}

@router.get("/api/health")
def health():
    return {"status": "ok"}
