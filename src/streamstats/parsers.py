import csv
import json
from pathlib import Path

from .errors import ConfigError, UnsupportedFormat


def json_load(p):
	with Path(p).open(encoding='utf-8') as file:
		for line in file:
			try:
				data = json.loads(line) if line.strip() else None
			except json.JSONDecodeError:
				data = line
			yield data

def csv_load(p):
	with Path(p).open(encoding='utf-8', newline='') as file:
		yield from csv.DictReader(file)

def parse(path, format):
	if not Path(path).is_file():
		raise ConfigError(f'Файл не найден: {path}')
	match format:
		case 'jsonl':
			return json_load(path)
		case 'csv':
			return csv_load(path)
		case _:
			raise UnsupportedFormat(f'Неподдерживаемый формат: {format}')





