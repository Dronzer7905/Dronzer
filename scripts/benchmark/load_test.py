import asyncio
import time
import aiohttp
import argparse

async def fetch(session, url, payload, headers):
    start = time.monotonic()
    async with session.post(url, json=payload, headers=headers) as response:
        await response.text()
        return response.status, time.monotonic() - start

async def run_benchmark(url: str, requests: int, concurrency: int, api_key: str):
    print(f"Starting benchmark: {requests} requests to {url} with concurrency {concurrency}")
    
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {
        "model": "gpt-4o",
        "messages": [{"role": "user", "content": "Hello, benchmark!"}],
        "stream": False
    }

    async with aiohttp.ClientSession() as session:
        tasks = []
        for _ in range(requests):
            tasks.append(fetch(session, url, payload, headers))
            if len(tasks) >= concurrency:
                results = await asyncio.gather(*tasks)
                tasks = []
                
        if tasks:
            results = await asyncio.gather(*tasks)

    print("Benchmark complete.")
    # Process results (status codes, p50, p99) would go here

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dronzer Load Testing")
    parser.add_argument("--url", default="http://localhost:8000/v1/chat/completions")
    parser.add_argument("--requests", type=int, default=100)
    parser.add_argument("--concurrency", type=int, default=10)
    parser.add_argument("--key", default="sk-test")
    args = parser.parse_args()
    
    asyncio.run(run_benchmark(args.url, args.requests, args.concurrency, args.key))
