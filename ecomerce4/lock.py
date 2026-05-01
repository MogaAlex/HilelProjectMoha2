import asyncio
from datetime import datetime

lock = asyncio.Lock()

async def worker(delay: float, name: str):
    for i in range(4):
        now = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        print(f'{now} {name} -> step {i}')

        async with lock:
            now = datetime.now().strftime('%H:%M:%S.%f')[:-3]
            print(f'{now} {name} -> step {i} locked')
            await asyncio.sleep(delay)
            print(f'Resources returns to {name}')
        await asyncio.sleep(delay)
    now = datetime.now().strftime('%H:%M:%S.%f')[:-3]
    return f'{now} {name} -> {delay}s '


async def main():
    tasks = [
        worker(delay=1.5, name='Task A'),
        worker(delay=0.7, name='Task B'),
        worker(delay=2.2, name='Task C'),
    ]

    results = await asyncio.gather(*tasks)

    print('All results:', results)


if __name__ == '__main__':
    asyncio.run(main())