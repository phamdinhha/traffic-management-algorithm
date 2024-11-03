from collections import deque
import time
from threading import Lock
from dataclasses import dataclass
from typing import Dict

@dataclass
class RequestLog:
    timestamp: deque[float]
    total_requests: int = 0
    
class SlidingWindowRateLimiter:
    def __init__(self, window_size: float, max_requests: int):
        self.max_requests = max_requests
        self.window_size = window_size
        self.requests: Dict[str, RequestLog] = {} # client_id -> RequestLog
        self.lock = Lock()
        
    def is_allowed(self, client_id: str) -> bool:
        with self.lock:
            now = time.time()
            if client_id not in self.requests:
                self.requests[client_id] = RequestLog(
                    timestamp=deque([now]),
                    total_requests=0
                )
            request_log = self.requests[client_id]
            while request_log.timestamp and request_log.timestamp[0] <= now - self.window_size:
                request_log.timestamp.popleft()
                request_log.total_requests -= 1
            if request_log.total_requests >= self.max_requests:
                return False
            request_log.timestamp.append(now)
            request_log.total_requests += 1
            return True
        
    def get_requests_count(self, client_id: str) -> int:
        with self.lock:
            return self.requests[client_id].total_requests if client_id in self.requests else 0
        
    def get_time_to_reset(self, client_id: str) -> float:
        with self.lock:
            if client_id not in self.requests or not self.requests[client_id].timestamp:
                return 0
            oldest_request = self.requests[client_id].timestamp[0]
            return max(0, self.window_size - (time.time() - oldest_request))
        
    def get_rate_limit_info(self, client_id: str):
        with self.lock:
            now = time.time()
            if client_id not in self.requests:
                return {
                    "remaining_requests": self.max_requests,
                    "current_requests": 0,
                    "reset_time": now + self.window_size,
                    "window_size": self.window_size
                }
            request_log = self.requests[client_id]
            while (request_log.timestamp and request_log.timestamp[0] <= now - self.window_size):
                request_log.timestamp.popleft()
                request_log.total_requests -= 1
            return {
                "remaining": max(0, self.max_requests - request_log.total_requests),
                "current_requests": request_log.total_requests,
                "reset_time": (request_log.timestamp[0] + self.window_size) if request_log.timestamp else now + self.window_size,
                "window_size": self.window_size
            }
  
    