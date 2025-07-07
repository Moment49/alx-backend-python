#!/usr/bin/env python3

import sys
processing = __import__('1-batch_processing')

##### print processed users in a batch of 50
try:
    for row in processing.stream_users_in_batches(50):
        print(row)
        
    for row in processing.batch_processing(50):
        print(row)
except BrokenPipeError:
    sys.stderr.close()