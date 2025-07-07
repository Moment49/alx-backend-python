#!/usr/bin/env python3

from itertools import islice
stream_module_users = __import__('0-stream_users')

# iterate over the generator function and print only the first 6 rows

for user in islice(stream_module_users.stream_users(), 2):
    print(user)