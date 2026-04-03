#!/usr/bin/env python3
"""Check scheduled cron jobs."""
import asyncio
import json
import websockets

WS_URL = "ws://10.93.26.140:42002/ws/chat?access_key=my_secret_api_key"


async def main():
    async with websockets.connect(WS_URL) as ws:
        print("✓ Connected to WebSocket")
        
        # Ask to list scheduled jobs
        msg = {"content": "List scheduled jobs."}
        await ws.send(json.dumps(msg))
        print("✓ Sent request")
        
        # Wait for responses
        for i in range(5):
            try:
                resp = await asyncio.wait_for(ws.recv(), timeout=60)
                content_preview = resp[:300] if len(resp) > 300 else resp
                print(f"✓ Response {i+1}: {content_preview}...")
            except asyncio.TimeoutError:
                print(f"⏱ Timeout waiting for response {i+1}")
                break


if __name__ == "__main__":
    asyncio.run(main())
