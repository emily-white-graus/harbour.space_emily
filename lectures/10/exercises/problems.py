"""Lecture 10 practice problems: threading, multiprocessing, and async/await.

Implement each function below so tests pass.
Rules:
- Do not change function names/signatures.
- Use only the Python standard library.
"""

from __future__ import annotations

import asyncio
import time
import threading
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


def simulated_long_fetch(value: object) -> object:
    """Helper function: Simulate a slow blocking fetch and return the same input value."""
    time.sleep(0.1)
    return value


async def async_simulated_long_fetch(value: object) -> object:
    """Helper function: Simulate a slow async fetch and return the same input value."""
    await asyncio.sleep(0.1)
    return value


def locked_counter_total(num_threads: int, increments_per_thread: int) -> int:
    """Mission 1: thread-safe counter increment with `threading.Lock`.

    Required functions/classes:
        - `threading.Thread`
        - `threading.Lock`
        - `Thread.start()` and `Thread.join()`

    Expected result:
        num_threads * increments_per_thread
    """
    counter = 0
    lock = threading.Lock()

    def worker() -> None:
        nonlocal counter
        for _ in range(increments_per_thread):
            with lock:
                counter += 1

    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=worker)
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    return counter


def threaded_square_map(values: list[int]) -> list[int]:
    """Mission 2: compute squares using one thread per element.

    Required functions/classes:
        - `threading.Thread`
        - `Thread.start()` and `Thread.join()`

    Notes:
        - Keep output index order the same as input order.

    Example:
        [2, -3, 4] -> [4, 9, 16]
    """
    results = [0] * len(values)

    def worker(index: int, value: int) -> None:
        results[index] = value * value

    threads = [
        threading.Thread(target=worker, args=(index, value))
        for index, value in enumerate(values)
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    return results


def threadpool_sleep_map(delays: list[float], max_workers: int = 4) -> list[float]:
    """Mission 3: simulate blocking I/O with `ThreadPoolExecutor`.

    Requirements:
        - Use `ThreadPoolExecutor(max_workers=max_workers)`.
        - In each task, call `simulated_long_fetch(delay)` and return its result.
        - Preserve input order in returned list (for example via `executor.map`).
        - Raise `ValueError` if `max_workers < 1`.
    """
    if max_workers < 1:
        raise ValueError("max_workers must be at least 1")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        return list(executor.map(simulated_long_fetch, delays))


def processpool_square_map(values: list[int], max_workers: int = 2) -> list[int]:
    """Mission 4: compute squares with `ProcessPoolExecutor`.

    Requirements:
        - Use a process pool (`ProcessPoolExecutor`).
        - Use process-pool mapping (`executor.map` or equivalent).
        - Return squared values in the same order as input.
        - Raise `ValueError` if `max_workers < 1`.
    """
    if max_workers < 1:
        raise ValueError("max_workers must be at least 1")

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        return list(executor.map(_square, values))


async def async_tag_fetch(labels: list[str], delay: float = 0.01) -> list[str]:
    """Mission 5: run async tasks concurrently with `asyncio.gather`.

    Required functions:
        - `async_simulated_long_fetch`
        - `asyncio.gather`

    Behavior:
        - For each label, first fetch it with `async_simulated_long_fetch`.
        - Then return `f"done:{label}"`.
        - Preserve output order by label position.
        - `delay` is kept for API compatibility; you do not need to use it.
    """
    async def fetch_one(label: str) -> str:
        fetched = await async_simulated_long_fetch(label)
        return f"done:{fetched}"

    return await asyncio.gather(*(fetch_one(label) for label in labels))


async def async_blocking_double(values: list[int]) -> list[int]:
    """Mission 6: bridge blocking work into async flow.

    Required functions:
        - `simulated_long_fetch`
        - `asyncio.to_thread`
        - `asyncio.gather`

    Return:
        - For each input value, run `simulated_long_fetch` via `to_thread`.
        - After fetch completes, double the value.
        - Return doubled values in input order.

        Example: [1, 2, 3] -> [2, 4, 6]
    """
    async def double_one(value: int) -> int:
        fetched = await asyncio.to_thread(simulated_long_fetch, value)
        return fetched * 2

    return await asyncio.gather(*(double_one(value) for value in values))


def _square(value: int) -> int:
    return value * value
