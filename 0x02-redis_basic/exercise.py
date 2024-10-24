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
    The class provides methods to store and retrieve data from Redis.
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
