import asyncio

async def fetch_data(endpoint: str):
    print(f'{endpoint} fetching started')
    await asyncio.sleep(1.2)
    print(f'{endpoint} fetching ended')
    return f'Data from {endpoint}'

async def main():
    print('Main function run')
    result1 = await fetch_data('API1')
    result2 = await fetch_data('API2')
    print(f'{result1} and {result2}')

if __name__ == '__main__':
   asyncio.run(main())