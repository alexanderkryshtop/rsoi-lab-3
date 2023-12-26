import requests
import time
from threading import Thread
from typing import Dict


class Request:
    def __init__(self, url, http_method, headers, data, timeout):
        self._url = url
        self._http_method = http_method
        self._headers = headers
        self._data = data
        self._timeout = timeout

    def url(self):
        return self._url

    def http_method(self):
        return self._http_method

    def headers(self):
        return self._headers

    def data(self):
        return self._data

    def timeout(self):
        return self._timeout


class Queue:
    _timeout = 10
    _request_queue: Dict[str, Request] = {}
    _background_worker: Thread = None

    @staticmethod
    def push(url: str, http_method, headers={}, data={}, params=None, timeout=10, repeat_num=0):
        resp = requests.Response()
        resp.status_code = 503
        if repeat_num > 0:
            for i in range(repeat_num):
                try:
                    resp = http_method(url, headers=headers, json=data, params=params, timeout=timeout)
                except Exception:
                    pass
                if resp is not None and resp.status_code <= 500:
                    return resp
            resp = requests.Response()
            resp.status_code = 503
            return resp

        Queue._request_queue[url + http_method.__name__] = Request(url=url, http_method=http_method, headers=headers,
                                                                   data=data, timeout=timeout)
        if Queue._background_worker is None:
            Queue._background_worker = Thread(target=Queue._send_requests_in_queue)
            Queue._background_worker.start()

    @staticmethod
    def _send_requests_in_queue():
        while len(Queue._request_queue.keys()) > 0:
            for req_key in Queue._request_queue.keys():
                Thread(target=Queue._send_request, args=(req_key,)).start()
            time.sleep(Queue._timeout)

        Queue._background_worker = None

    @staticmethod
    def _send_request(key: str):
        req = Queue._request_queue.get(key)
        if req is None:
            return

        resp = None
        try:
            resp = req.http_method()(req.url(), headers=req.headers(), json=req.data(), timeout=req.timeout())
        except Exception:
            print(f"error {req.http_method().__name__}:", req.url())
        if resp is not None and resp.status_code <= 500:
            del Queue._request_queue[key]
