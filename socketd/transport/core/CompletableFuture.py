import asyncio
from typing import Generic, TypeVar

T = TypeVar('T')


class CompletableFuture(Generic[T]):

    def __init__(self):
        self._future: asyncio.Future = None

    async def get(self, timeout):
        if not self._future:
            self._future = asyncio.Future()
        await asyncio.wait_for(self._future, timeout)
        return self._future.result()

    def accept(self, result: T, onError):
        self._future.set_result(result)

    def then_async(self, f: asyncio.Future):
        self._future = asyncio.ensure_future(f)

    def set_result(self, t: T):
        self._future.set_result(t)

    def done(self):
        self._future.done()

    def cancel(self):
        self._future.cancel()
