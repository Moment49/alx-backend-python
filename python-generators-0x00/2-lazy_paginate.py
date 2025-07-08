#!/usr/bin/env python3
import time
seed = __import__('seed')

def paginate_users(page_size, offset):
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows

# rows = paginate_users(5, 1)
# print(rows)

def lazy_pagination(page_size):
    """Generator to paginate through user data."""

    # Set the start offset of the data returned
    offset = 0
    start_time = time.time()
    while True:
        # Loop to return the paginated data and increment the offset
        rows = paginate_users(page_size, offset)
        # Condition to check if no rows are returned
        if not rows:
            print("All paginated data has been returned")
            break

        offset += 1
        yield rows
    end_time = time.time()
    print(f"pagination time: {round(end_time - start_time, 3)}")


for row in lazy_pagination(500):
    print(row)