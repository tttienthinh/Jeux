import time, requests

start = time.time()
for i in range(1_000):
    requests.get("http://127.0.0.1:5000")
end = time.time()

print(end-start)

