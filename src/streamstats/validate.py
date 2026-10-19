import logging
from datetime import datetime

from .errors import EmptyField, IncorrectFormat, IncorrectLevel, MissingKey, OddKey

levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']

logging.basicConfig(level=logging.WARNING, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def validate(obj):
	fields = ['timestamp', 'level', 'source', 'message']
	for k in obj:
		fields.remove(k)
	if fields:
		raise MissingKey('Не хватает следующих ключей:', *fields)
	if len(fields) > 4:
		raise OddKey('Переданы лишние поля', *fields)
	for k,v in obj.items():
		if not v:
			raise EmptyField('Передана пустая строка', k)
	if obj['level'] not in levels:
		raise IncorrectLevel('Дан неправильный уровень лога')
	try:
		datetime.fromisoformat(obj['timestamp'])
	except (ValueError, TypeError) as err:
		raise IncorrectFormat('Введена некорректная строка timestamp') from err
	else:
		match obj['level']:
			case 'WARNING':
				logger.warning(obj['message'])
			case 'ERROR':
				logger.error(obj['message'])
			case 'CRITICAL':
				logger.critical(obj['message'])
			