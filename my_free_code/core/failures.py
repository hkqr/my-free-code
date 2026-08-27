from dataclasses import dataclass

@dataclass(frozen=True)
class ExecutionFailure(Exception):
    message: str
    kind: str = "upstream"
    status: int | None = None
    retryable: bool = True
    committed: bool = False

    def __str__(self):
        return self.message

RETRYABLE_STATUS = {408, 409, 425, 429, 500, 502, 503, 504}

def classify_status(status: int, message: str) -> ExecutionFailure:
    return ExecutionFailure(
        message=message,
        kind="upstream",
        status=status,
        retryable=status in RETRYABLE_STATUS,
    )
