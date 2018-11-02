""" Utility functions for concurrency."""

import functools
import threading 
import time

def serialized(func):
	""" Decorator to provide mutual exclusion for method using _lock attribute."""
	@functools.wraps(func)
	def serialized_method(self, *args, **kwargs):
		lock = getattr(self, '_lock')
		with lock:
			return func(self, *args, **kwargs)
	return serialized_method


class Singleton(type):
	""" A threadsafe singleton meta-class"""
	_singleton_lock = threading.RLock()
	_instances = {}

	def __call__(cls, *args, **kwargs):
		with Singleton._singleton_lock:
			if cls not in cls._instances:
				cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
			return cls._instances[cls]
		