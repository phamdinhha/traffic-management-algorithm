##Core Concepts:

Imagine a bucket that holds tokens
Tokens flow into the bucket at a constant rate (fill_rate)
The bucket has a maximum capacity
Each request consumes one or more tokens
If there are enough tokens, the request is allowed
If not enough tokens, the request is rejected


##Key Components:

capacity: Maximum number of tokens (bucket size)
fill_rate: How fast tokens are added (tokens per second)
tokens: Current number of available tokens
last_update: When we last added tokens


##The Algorithm Flow:
a. When a request arrives:

Calculate time passed since last update
Add new tokens based on time passed × fill_rate
Cap tokens at maximum capacity
Try to consume tokens for the request

b. Token consumption:

If enough tokens available: subtract tokens and allow request
If not enough tokens: reject request


##Benefits:

Allows for "burst" traffic up to bucket capacity
Smooths out traffic over time
Simple to implement and understand
Memory efficient (only stores a few variables)


##Common Use Cases:

API rate limiting
Network traffic shaping
Resource consumption control
DDoS protection