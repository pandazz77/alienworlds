import time

class TimerError(Exception):

	def __init__(self, message):
		self.message = message
		super().__init__(self.message)


class Timer:
	def __init__(self):
		self._started = False
		self._start_time = None

	def start(self):
		if not self._started:
			self._started = True
			self._start_time = time.perf_counter()
			return self._start_time
		else:
			pass
			#raise TimerError("Timer is already running!")

	def get_time(self):
		if self._started:
			return time.perf_counter() - self._start_time
		else:
			pass
			#raise TimerError("Timer is not started!")

	def status(self):
		return self._started

	def stop(self):
		if self._started:
			ellapsed = time.perf_counter() - self._start_time
			self._start_time = None
			self._started = False
			return ellapsed
		else:
			pass
			#raise TimerError("Timer is not started!")