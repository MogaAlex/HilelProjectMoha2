import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import Counter
from datetime import datetime


TARGET_URI = 'https://localhost'
MAX_WORKERS = 20
REQ_PER_SECOND = 300
DURATION = 40
TIMEOUT = 10

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
session = requests.Session()
session.verify = False
session.headers.update({'User-Agent': 'LoadTest/1.0'})

stats_lock = threading.Lock()
stats = Counter()

def send_request():
    try:
        start = time.time()
        response = session.get(TARGET_URI, timeout=TIMEOUT)
        duration = time.time() - start
        with stats_lock:
            if response.status_code == 200:
                stats['200'] += 1
            elif response.status_code == 503:
                stats['503'] += 1
            else:
                stats[f'{response.status_code}'] += 1
        return duration
    except requests.Timeout:
        with stats_lock:
            stats['Timeout'] += 1
    except Exception as e:
        with stats_lock:
            stats['errors'] += 1

def print_stats():
    while True:
        time.sleep(2)
        with stats_lock:
            total = sum(stats.values())
            if total == 0:
                continue
            print (
                f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]'
                f'Requests {total}'
                f'| 200: {stats["200"]} | '
                f'| 503: {stats["503"]} | '
                f'| Timeout: {stats["Timeout"]} | '
                f'| Errors: {stats["errors"]} | '
            )
start_time = time.time()

stats_thread = threading.Thread(target=print_stats, daemon=True)
stats_thread.start()

with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    while time.time() - start_time < DURATION:
        futures = []
        batch_size = min(REQ_PER_SECOND // 5, MAX_WORKERS // 2)
        for _ in range(batch_size):
            futures.append(executor.submit(send_request))

        for future in as_completed(futures, timeout=15):
            future.result()

        elapsed = time.time() - start_time
        excpected_requests = int(REQ_PER_SECOND * elapsed)
        actual_results = sum(stats.values())
        sleep_time = max(0, (actual_results + batch_size)/REQ_PER_SECOND - excpected_requests)
        time.sleep(max(0.01, sleep_time))

print('\n====== Test Finished =========')
total_requests = sum(stats.values())
success_rate = ((stats['200'] / total_requests) * 100) if total_requests > 0 else 0

print(f'Total requests: {total_requests}')
print(f'Success rate: {stats["200"]}%')
print(f'Rejects: {stats["503"]}%')
print(f'Timeouts: {stats["timeout"]}%')
print(f'Errors: {stats["errors"]}%')

if stats["200"] > stats["503"]:
    print('Bad security policy')
else
    print('Good results! Most of the attacking requests was rejected')