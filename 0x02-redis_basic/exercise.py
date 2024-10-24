#!/usr/bin/env python3
"""
This module defines a Cache class that interacts with a Redis database.
The Cache class stores data with randomly generated keys.
"""

import redis
from typing import Union
import uuid


class Cache:
    """
    Cache class for storing data in Redis.
    The class provides methods to store, retrieve, and convert data from Redis
    """

    def __init__(self) -> None:
        """
        Initialize the Redis client and flush the database.

        The Redis client is stored as a private instance variable `_redis`.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the data in Redis with a randomly generated key.

        Args:
            data (Union[str, bytes, int, float]): The data to store in Redis.

        Returns:
            str: The generated random key associated with the stored data.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(
        self, key: str, fn: Optional[Callable] = None
    ) -> Union[str, bytes, int, float, None]:
        """
        Retrieve data from Redis by key and optionally apply a conversion fun

        Args:
            key (str): The key to retrieve the data for.
            fn (Callable, optional): A function to apply to the retrieved
                Defaults to None.

        Returns:
            Union[str, bytes, int, float, None]: The retrieved data
        """
        value = self._redis.get(key)
        if value is None:
            return None
        if fn:
            return fn(value)
        return value

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieve a string value from Redis.

        Args:
            key (str): The key to retrieve the data for.

        Returns:
            Optional[str]: The decoded string value from Redis or None.
        """
        return self.get(key, lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieve an integer value from Redis.

        Args:
            key (str): The key to retrieve the data for.

        Returns:
            Optional[int]: The integer value from Redis or None.
        """
        return self.get(key, lambda d: int(d))
