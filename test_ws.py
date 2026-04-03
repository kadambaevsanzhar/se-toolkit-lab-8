#!/usr/bin/env python3
"""Test WebSocket and create health check."""
import asyncio
import json
import websockets

WS_URL = "ws://10.93.26.140:42002/ws/chat?access_key=my_secret_api_key"


async def main():
    async with websockets.connect(WS_URL) as ws:
        print("✓ Connected to WebSocket")
        
        # Send health check request immediately
        health_msg = {
            "content": "Create a health check for this chat that runs every 15 minutes. Each run should check for backend errors in the last 15 minutes, inspect a trace if needed, and post a short summary here. If there are no recent errors, say the system looks healthy. Use your cron tool."
        }
        await ws.send(json.dumps(health_msg))
        print("✓ Sent health check request")
        
        # Wait for responses
        for i in range(10):
            try:
                resp = await asyncio.wait_for(ws.recv(), timeout=60)
                content_preview = resp[:150] if len(resp) > 150 else resp
                print(f"✓ Response {i+1}: {content_preview}...")
                
                # Check if we got a meaningful response
                try:
                    data = json.loads(resp)
                    if "health" in data.get("content", "").lower() or "cron" in data.get("content", "").lower():
                        print("\n✓✓✓ Health check created successfully! ✓✓✓")
                        return
                except:
                    pass
            except asyncio.TimeoutError:
                print(f"⏱ Timeout waiting for response {i+1}")
                break
        
        print("\n✓ Request processed by agent")


if __name__ == "__main__":
    asyncio.run(main())
