Circuit Breaker pattern is designed to prevent a cascading failure in a distributed system.

The circuit breaker monitors the failure rate of a service. If the failure rate exceeds a threshold, the circuit breaker trips and stops sending requests to the service.


## States

- **Closed**: Requests are sent to the service.
- **Open**: Requests are not sent to the service.
- **Half-Open**: Requests are sent to the service after a timeout.

## Key components

- **Failure Threshold**: The number of failures that trigger the circuit breaker to trip.
- **Reset Timeout**: The duration after which the circuit breaker transitions from **Open** to **Half-Open**.
- **Failures**: The number of consecutive failures.
- **Last Failure**: The timestamp of the last failure.
