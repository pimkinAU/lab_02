import json
import sys
from pathlib import Path

import pytest

from streamstats.__main__ import main
from streamstats.analysis import Statistics
from streamstats.errors import EmptyField, IncorrectFormat, IncorrectLevel, MissingKey
from streamstats.parsers import parse
from streamstats.validate import validate


def test_good_event():
	obj = {'timestamp': '2026-10-07T12:00:00+03:00', 'level': 'INFO', 'source': 'api', 'message': 'Привет'}
	validate(obj)

def test_read_jsonl():
	data = list(parse('tests/data/good.jsonl', 'jsonl'))
	assert len(data) == 2

def test_read_csv():
	data = list(parse('tests/data/log.csv', 'csv'))
	assert data[0]['source'] == 'api'

def test_count_events():
	stats = Statistics()
	obj = {'timestamp': '2026-10-07T12:00:00+03:00', 'level': 'ERROR', 'source': 'api', 'message': 'Привет'}
	stats.add(obj)
	stats.add(obj)
	assert stats.events_amount == 2
	assert stats.levels['ERROR'] == 2

def test_skip_invalid():
	sys.argv = ['streamstats', 'analyze', 'tests/data/with_bad.jsonl', '--format', 'jsonl', '--output', 'tests/data/report.json', '--skip-invalid']
	main()
	with Path('tests/data/report.json').open(encoding='utf-8') as file:
		data = json.load(file)
	assert data['skipped_lines'] == 1

def test_no_message():
	obj = {'timestamp': '2026-10-07T12:00:00+03:00', 'level': 'INFO', 'source': 'api'}
	with pytest.raises(MissingKey):
		validate(obj)

def test_empty_source():
	obj = {'timestamp': '2026-10-07T12:00:00+03:00', 'level': 'INFO', 'source': '', 'message': 'Привет'}
	with pytest.raises(EmptyField):
		validate(obj)

def test_wrong_level():
	obj = {'timestamp': '2026-10-07T12:00:00+03:00', 'level': 'WRONG', 'source': 'api', 'message': 'Привет'}
	with pytest.raises(IncorrectLevel):
		validate(obj)

def test_wrong_timestamp():
	obj = {'timestamp': 'вчера', 'level': 'INFO', 'source': 'api', 'message': 'Привет'}
	with pytest.raises(IncorrectFormat):
		validate(obj)

def test_bad_line_returns_2():
	sys.argv = ['streamstats', 'analyze', 'tests/data/with_bad.jsonl', '--format', 'jsonl', '--output', 'tests/data/report.json']
	assert main() == 2
