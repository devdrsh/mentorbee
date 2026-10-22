import os
import asyncio
import urllib.request
import logging

logger = logging.getLogger("mentorbee.keep_alive")

async def start_keep_alive():
    """
    Background worker that pings the application's /api/health endpoint
    every 9-10 minutes to prevent cloud hosting platforms (like Render.com free tier)
    from spinning down due to 15 minutes of inactivity.
    """
    # Render automatically sets RENDER_EXTERNAL_URL (e.g. https://mentorbee.onrender.com)
    external_url = os.getenv("RENDER_EXTERNAL_URL") or os.getenv("APP_URL") or os.getenv("KEEP_ALIVE_URL")
    
    if not external_url:
        logger.info("[Keep-Alive] No external URL configured (RENDER_EXTERNAL_URL / APP_URL). Skipping self-pinging loop.")
        return

    # Clean URL format
    external_url = external_url.rstrip("/")
    health_endpoint = f"{external_url}/api/health"
    
    # Ping every 9 minutes (540 seconds) to safely beat Render's 15-minute inactivity timeout
    interval_seconds = int(os.getenv("KEEP_ALIVE_INTERVAL_SECONDS", "540"))
    
    logger.info(f"[Keep-Alive] Initialized self-ping service for: {health_endpoint} every {interval_seconds}s")
    
    # Wait 60 seconds before first ping to allow app to finish boot
    await asyncio.sleep(60)

    while True:
        try:
            # Run non-blocking HTTP GET via standard library urllib
            req = urllib.request.Request(
                health_endpoint,
                headers={"User-Agent": "MentorBee-KeepAlive-Heartbeat/1.0"}
            )
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, lambda: urllib.request.urlopen(req, timeout=15))
            logger.info(f"[Keep-Alive] Heartbeat ping successful to {health_endpoint}")
        except Exception as e:
            logger.warning(f"[Keep-Alive] Heartbeat ping failed: {e}")
        
        await asyncio.sleep(interval_seconds)
