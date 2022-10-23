import requests
import time
import asyncio

start = time.time()
url = "http://127.0.0.1:5000/process"
file_path = 'example_data/example_data.json'
files = {'data': open(file_path, 'rb')}


def background(f):
    def wrapped(*args, **kwargs):
        return asyncio.get_event_loop().run_in_executor(None, f, *args, **kwargs)

    return wrapped


@background
def get_data(url, data):
    print(url)
    res = requests.post(url, files={'data': open(file_path, 'rb')})
    print(res)


for i in range(5):
    get_data(url, files)

end = time.time()

# a Sync way to do it

# for i in range(10):
#     res = requests.post(url, files=files)
#     print(res)

# calculate time needed to process all requests
#print("Time needed: ", end - start)
