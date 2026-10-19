import json
from datetime import datetime
from pathlib import Path


def get_data(stats):
	return {
		'event_amount': stats.events_amount,
		'errors': stats.errors,
		'first_date': datetime.fromisoformat(str(stats.first_date)),
		'last_date': datetime.fromisoformat(str(stats.last_date)),
		'skipped_lines': stats.skipped_lines,
		'top_five': stats.get_five()
	}

def report(stats, path):
	content = json.dumps(get_data(stats), ensure_ascii=False, default=str)
	with Path(path).open(encoding='utf-8', mode='w') as file:
		file.write(content)



