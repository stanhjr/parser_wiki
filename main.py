from db import get_politicians, update_politician, get_politician_count, update_politician_not_data
from query_builder import fetch_one_politician

while True:
    politicians = get_politicians(offset=10)
    for politician in politicians:
        politician_data = fetch_one_politician(politician_id=politician.id)
        if politician_data:
            update_politician(politician=politician_data)
            print("update_politician", politician.id, flush=True)
        else:
            update_politician_not_data(politician_id=politician.id)
        left_politician_count = get_politician_count(is_update=0)
        print(f"All that's left is to parse politicians {left_politician_count}", flush=True)
        if left_politician_count == 0:
            print("Parse completed", flush=True)
            break

