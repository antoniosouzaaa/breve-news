from contextlib import asynccontextmanager
from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from app.database import init_db
from app.routes.web import router
from app.services.scheduler import run_daily_curation
from app.config import settings

scheduler = BackgroundScheduler(timezone=settings.TIMEZONE)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicializa banco de dados SQLite
    init_db()
    # Agenda o job diário matinal para as 06:30 BRT
    scheduler.add_job(
        run_daily_curation,
        trigger=CronTrigger(hour=6, minute=30, timezone=settings.TIMEZONE),
        id="morning_curation_job",
        replace_existing=True
    )
    scheduler.start()
    yield
    scheduler.shutdown()

app = FastAPI(title="BREVE. Morning Briefing", lifespan=lifespan)
app.include_router(router)
