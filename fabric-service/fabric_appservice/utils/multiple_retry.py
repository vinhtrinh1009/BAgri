import time
MAX_DELAY_TIME = 300

def multiple_retry(func, kwargs, num_retry=2, delay=5):
    error = None
    result = None
    for i in range(num_retry):
        try:
            result = func(**kwargs)
        except Exception as e:
            error = e
            if i != num_retry:
                sleep_time = min(delay*(i+1)*2, MAX_DELAY_TIME)
                time.sleep(sleep_time)
        else:
            return result
    if error:
        raise error
    else:
        raise BaseException()
