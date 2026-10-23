from datetime import datetime, date
from zoneinfo import ZoneInfo
from sqlmodel import Session, select
from app.database import engine
from app.models import Edition, Article
from app.services.rss_fetcher import fetch_category_items
from app.services.ai_summarizer import summarize_category_news
from app.services.mailer import send_morning_alert
from app.config import settings

CATEGORIES = ["cultura", "economia", "f1", "design", "geral"]

IS_CURATING = False

def is_curating() -> bool:
    global IS_CURATING
    return IS_CURATING

def get_current_date() -> date:
    try:
        return datetime.now(ZoneInfo(settings.TIMEZONE)).date()
    except Exception:
        return date.today()

def run_daily_curation(force: bool = False):
    global IS_CURATING
    if IS_CURATING:
        print("Curadoria já está em andamento. Aguarde a finalização.")
        return

    IS_CURATING = True
    try:
        today = get_current_date()
        print(f"Iniciando curadoria diária para: {today}")

        with Session(engine) as session:
            existing = session.exec(select(Edition).where(Edition.edition_date == today)).first()
            if existing and not force:
                print(f"Edição de hoje ({today}) já foi processada.")
                return

            edition = existing or Edition(edition_date=today)
            session.add(edition)
            session.commit()
            session.refresh(edition)

            if force and existing:
                # Limpa artigos anteriores para reprocessar
                for old_art in list(edition.articles):
                    session.delete(old_art)
                session.commit()

            for cat in CATEGORIES:
                raw_items = fetch_category_items(cat)
                if not raw_items:
                    continue
                curated_list = summarize_category_news(cat, raw_items)
                for item in curated_list:
                    article = Article(
                        edition_id=edition.id,
                        category=cat,
                        title=item["title"],
                        summary=item["summary"],
                        source_name=item["source_name"],
                        source_url=item["source_url"]
                    )
                    session.add(article)

            edition.email_sent = True
            session.add(edition)
            session.commit()

        send_morning_alert(today.strftime("%d/%m/%Y"))
        print(f"Curadoria diária concluída com sucesso para {today}.")
    except Exception as e:
        print(f"Erro inesperado durante a curadoria diária: {e}")
    finally:
        IS_CURATING = False
