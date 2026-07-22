import asyncio
import logging
from contextlib import suppress

from app.db.database import SessionLocal
from app.services.job_sync_service import JobSyncService

logger = logging.getLogger(__name__)
SYNC_INTERVAL_SECONDS = 24 * 60 * 60


def sync_jobs_in_worker() -> dict:
    db = SessionLocal()
    try:
        return JobSyncService(db).sync_all_jobs()
    finally:
        db.close()


class DailyJobScheduler:
    def __init__(self, interval_seconds: int = SYNC_INTERVAL_SECONDS):
        self.interval_seconds = interval_seconds
        self._stop_event = asyncio.Event()
        self._run_lock = asyncio.Lock()
        self._task: asyncio.Task | None = None

    async def start(self):
        if self._task is None or self._task.done():
            self._stop_event.clear()
            self._task = asyncio.create_task(self._run(), name="daily-job-scheduler")
            logger.info("Daily job scheduler started; interval=%s seconds", self.interval_seconds)

    async def stop(self):
        if self._task is None:
            return
        self._stop_event.set()
        self._task.cancel()
        with suppress(asyncio.CancelledError):
            await self._task
        self._task = None
        logger.info("Daily job scheduler stopped")

    async def run_once(self) -> dict:
        async with self._run_lock:
            return await asyncio.to_thread(sync_jobs_in_worker)

    async def _run(self):
        while not self._stop_event.is_set():
            try:
                await asyncio.wait_for(self._stop_event.wait(), timeout=self.interval_seconds)
                continue
            except asyncio.TimeoutError:
                pass

            try:
                await self.run_once()
            except asyncio.CancelledError:
                raise
            except Exception:
                logger.exception("Scheduled job synchronization failed; scheduler will continue")
