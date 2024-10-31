from dataclasses import dataclass
from enum import Enum
from typing import Callable, Any
import datetime
import threading

class CircuitBreakerState(Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"

class CircuitBreakerError(Exception):
    pass


@dataclass
class CircuitBreaker:
    failure_threshold: int
    reset_timeout: float

    def __init__(
        self,
        failure_threshold: int,
        reset_timeout: float,
        failures: int = 0,
        state = CircuitBreakerState.CLOSED,
        last_failure: datetime.datetime = None,
    ):
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.failures = failures
        self.state = state
        self.last_failure = last_failure
        self.lock = threading.Lock()

    def handle_request(self, func: Callable, *args, **kwargs) -> Any:
        with self.lock:
            if self.state == CircuitBreakerState.OPEN:
                if datetime.datetime.now() - self.last_failure >= self.reset_timeout:
                    self.state = CircuitBreakerState.HALF_OPEN
                else:
                    raise CircuitBreakerError("Circuit breaker is open")
            try:
                result = func(*args, **kwargs)
                if self.state == CircuitBreakerState.HALF_OPEN:
                    self.state = CircuitBreakerState.CLOSED
                    self.failures = 0
                return result
            except Exception as e:
                self._handle_failure()
                raise CircuitBreakerError(f"Circuit breaker failed with {e}")

    def _handle_failure(self):
        self.failures += 1
        self.last_failure_time = datetime.datetime.now()
        if self.failures >= self.failure_threshold:
            self.state = CircuitBreakerState.OPEN
        

# def test_circuit_breaker():
#     breaker = CircuitBreaker(failure_threshold=3, reset_timeout=5)