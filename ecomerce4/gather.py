import asyncio
from asgiref.sync import sync_to_async
from datetime import datetime
import time

async def worker(delay: float, name: str):
    for i in range(4):
        now = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        print(f'{now} {name} -> step {i}')
        await asyncio.sleep(delay)
        print(f'Resources returns to {name}')
    now = datetime.now().strftime('%H:%M:%S.%f')[:-3]
    return f'{now} {name} -> {delay}s '

@sync_to_async
def sync_worker(delay: float, name: str):
    for i in range(4):
        now = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        print(f'{now} {name} -> step {i}')
        time.sleep(delay)
        print(f'Resources returns to {name}')
    now = datetime.now().strftime('%H:%M:%S.%f')[:-3]
    return f'{now} {name} -> {delay}s '

async def main():
    tasks = [
        worker(delay=1.5, name='Task A'),
        worker(delay=0.7, name='Task B'),
        worker(delay=2.2, name='Task C'),
        sync_worker(delay=3.1, name='Task D'),
    ]
  #  res = sync_worker(delay=3.1, name='Task D')
    results = await asyncio.gather(*tasks)
 #   results.append(res)
    print('All results:', results)


if __name__ == '__main__':
    asyncio.run(main())