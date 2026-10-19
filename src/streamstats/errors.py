class StreamStatsError(Exception):
	pass

class EmptyField(StreamStatsError):
	pass

class IncorrectFormat(StreamStatsError):
	pass

class IncorrectLevel(StreamStatsError):
	pass

class MissingKey(StreamStatsError):
	pass

class OddKey(StreamStatsError):
	pass

class UnsupportedFormat(StreamStatsError):
	pass

class ConfigError(StreamStatsError):
	pass