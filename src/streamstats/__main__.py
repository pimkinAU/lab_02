import argparse
import logging
import sys

from .analysis import Statistics
from .errors import StreamStatsError
from .parsers import parse
from .report import report
from .validate import validate

logger = logging.getLogger(__name__)


def main():
	try:
		parser = argparse.ArgumentParser(prog='streamstats', description='Статистика по логам из CSV и JSONL')
		subparser = parser.add_subparsers(dest='command', required=True)
		analyze_parser = subparser.add_parser('analyze', help='Посчитать статистику по файлам')
		analyze_parser.add_argument('input', nargs='+', help='Входные файлы')
		analyze_parser.add_argument('--format', help='Csv или jsonl')
		analyze_parser.add_argument('--output', help='Путь к JSON-отчёту')
		analyze_parser.add_argument('--skip-invalid', action='store_true', dest='skip', help='Пропускать ошибочные строки')

		stats = Statistics()

		args = parser.parse_args()
		for input in args.input:
			start = 2 if args.format == 'csv' else 1
			for number, event in enumerate(parse(input, args.format), start=start):
				if event is None:
					continue
				try:
					validate(event)
				except StreamStatsError as err:
					if not args.skip:
						raise StreamStatsError(f'{input}, строка {number}: {err}') from err
					logger.warning('%s, строка %s пропущена: %s', input, number, err)
					stats.skipped_lines += 1
					continue
				stats.add(event)
		print('Топ 5 источников ошибок ERROR/CRITICAL:', stats.get_five())
		print('Первая временная метка',stats.first_date)
		print('Последняя временная метка', stats.last_date)
		print('Skipped lines', stats.skipped_lines)
		if args.output:
			report(stats, args.output)
	except StreamStatsError as err:
		print('Получена ошибка -', err)
		return 2

if __name__ == '__main__':
	sys.exit(main())
