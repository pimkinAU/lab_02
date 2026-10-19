import csv
import json
from pathlib import Path


def json_load(p):
	with Path(p).open(encoding='utf-8') as file:
		for line in file:
			data = json.loads(line)
			yield data

def csv_load(p):
	with Path(p).open(encoding='utf-8') as file:
		yield from csv.DictReader(file)

def parse(path, format):
	match format:
		case 'jsonl':
			return json_load(path)
		case 'csv':
			return csv_load(path)





