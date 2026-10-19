from datetime import datetime


class Statistics:
	def __init__(self):
		self.events_amount: int = 0
		self.levels: dict = {x:0 for x in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']}
		self.sources: dict = {}
		self.errors: dict = {}
		self.first_date: str = ''
		self.last_date: str = ''
		self.skipped_lines: int = 0

	def add(self, event: dict):
		self.events_amount += 1
		self.levels[event['level']] += 1
		self.sources[event['source']] = self.sources.get(event['source'], 0) + 1
		if event['level'] in ['ERROR', 'CRITICAL']:
			self.errors[event['source']] = self.errors.get(event['source'], 0) + 1
		if not self.first_date:
			self.first_date = event['timestamp']
		else:
			self.first_date = min(datetime.fromisoformat(str(self.first_date)), datetime.fromisoformat(str(event['timestamp'])))
		if not self.last_date:
			self.last_date = event['timestamp']
		else:
			self.last_date = max(datetime.fromisoformat(str(self.last_date)), datetime.fromisoformat(str(event['timestamp'])))

	def get_five(self):
		return sorted(self.errors.items(), key=lambda x:(-x[1], x[0]))[:5]