import time

class TokenBucket:
    def __init__(self, capacity: int, refill_rate: int):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.last_refill = time.time()

    def refill(self):
        now = time.time()
        self.tokens = min(self.capacity, self.tokens + (now - self.last_refill) * self.refill_rate)
        self.last_refill = now
        
    def consume(self, tokens: int = 1):
        self.refill()
        if self.tokens < tokens:
            return False
        self.tokens -= tokens
        return True
    
def test_token_bucket():
    bucket = TokenBucket(capacity=10, refill_rate=2)
    for _ in range(20):
        print(bucket.consume(2))
        time.sleep(0.5)

if __name__ == "__main__":
    test_token_bucket()