# Tools/rate_limiter.py
import asyncio
import time

RATE_LIMIT = 60  # Max requests per minute
CONCURRENT_LIMIT = 12  # Max concurrent requests
RETRY_DELAY = 60  # Default retry delay in seconds for 429 status

class RateLimiter:
    def __init__(self, rate_limit_percentage: float):
        self.rate_limit = int(RATE_LIMIT * rate_limit_percentage)
        self.concurrent_limit = int(CONCURRENT_LIMIT * rate_limit_percentage)
        self.semaphore = asyncio.Semaphore(self.concurrent_limit)
        self.request_times = []

    async def __aenter__(self):
        await self.semaphore.acquire()
        while len(self.request_times) >= self.rate_limit:
            await asyncio.sleep(1)
            now = time.time()
            self.request_times = [t for t in self.request_times if now - t < 60]
        self.request_times.append(time.time())
        return self

    async def __aexit__(self, exc_type, exc, tb):
        self.semaphore.release()
