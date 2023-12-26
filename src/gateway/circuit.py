import requests
import time
from threading import Thread


class Breaker:
    _threshold = 5
    _delay = 10
    _failures = {}
    _service_info = {}
    _worker: Thread = None

    @staticmethod
    def send_request(url: str, http_method, headers: dict, data: dict, params=None, timeout=5):
        response = requests.Response()
        response.status_code = 503
        if http_method is None:
            return response

        host_url = url[url.find('://') + 3:]
        host_url = host_url[:host_url.find('/')]

        state = Breaker._service_info.get(host_url)
        if state == "unavailable":
            print(f"Service {host_url} is unavailable")
            return response

        for i in range(Breaker._threshold + 1):
            try:
                response = http_method(url, headers=headers, json=data, params=params, timeout=timeout)
            except Exception:
                pass

            if response is not None and response.status_code < 500:
                return response

            fail = Breaker._failures.get(host_url)
            if fail is None:
                Breaker._failures[host_url] = 1
            else:
                Breaker._failures[host_url] += 1

        fail = Breaker._failures.get(host_url)
        if fail is not None and fail > Breaker._threshold:
            Breaker._failures[host_url] = 0
            Breaker._service_info[host_url] = "unavailable"
            if Breaker._worker is None:
                Breaker._worker = Thread(target=Breaker._wait_until_available)
                Breaker._worker.start()
            print(f"CustomCircuitBreaker: num of fails for {host_url} is overflow")
            return response

        return response

    @staticmethod
    def _wait_until_available():
        is_end = False
        while not is_end:
            time.sleep(Breaker._delay)
            is_end = True
            for host_url in Breaker._service_info.keys():
                if Breaker._service_info[host_url] == "unavailable":
                    is_end = False
                    Thread(target=Breaker._health_check, args=(host_url,)).start()
        Breaker._worker = None

    @staticmethod
    def _health_check(host_url):
        resp = None
        url = 'http://' + host_url + '/manage/health'
        try:
            resp = requests.get(url, timeout=5)
        except Exception:
            print("error health:", url)
        if resp is not None and resp.status_code == 200:
            Breaker._service_info[host_url] = "available"