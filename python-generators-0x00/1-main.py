from itertools import islice

stream_user = __import__('0-stream_users')

# iterate over the generator function and print only the first 6 rows

for user in islice(stream_user.stream_users(), 6):
    print(user)
