# Tools/rate_limiter
import asyncio
import aiohttp
import logging
import time
from tqdm.asyncio import tqdm

RATE_LIMIT = 60  # Max requests per minute (max 100)
CONCURRENT_LIMIT = 12  # Max concurrent requests (max 20)
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

async def make_request(session: aiohttp.ClientSession, url: str, rate_limiter: RateLimiter):
    async with rate_limiter:
        while True:
            logging.debug(f"Making request to {url}")
            async with session.get(url) as response:
                if response.status == 429:
                    retry_after = int(response.headers.get('Retry-After', RETRY_DELAY))
                    logging.warning(f"Rate limit exceeded. Retrying after {retry_after} seconds.")
                    await asyncio.sleep(retry_after)
                else:
                    response.raise_for_status()
                    logging.info(f"Successfully received response from {url}")
                    return await response.json()  # Assuming JSON response
