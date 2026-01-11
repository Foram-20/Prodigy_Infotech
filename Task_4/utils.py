import time

def measure_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        response = func(*args, **kwargs)
        end = time.time()
        print(f"⏱️ Time Taken: {end - start:.4f} seconds")
        return response
    return wrapper
