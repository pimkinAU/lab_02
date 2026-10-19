import logging
from datetime import datetime

from .errors import EmptyField, IncorrectFormat, IncorrectLevel, MissingKey, OddKey

levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']

logging.basicConfig(level=logging.WARNING, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def validate(obj):
	if not isinstance(obj, dict):
		raise IncorrectFormat('Строка не является JSON-объектом')
	fields = ['timestamp', 'level', 'source', 'message']
	if set(fields) - set(obj):
		raise MissingKey('Не хватает следующих ключей:', *(set(fields) - set(obj)))
	if set(obj) - set(fields):
		raise OddKey('Переданы лишние поля', *(set(obj) - set(fields)))
	for k,v in obj.items():
		if not isinstance(v, str):
			raise IncorrectFormat('Значение должно быть строкой', k)
	if not obj['source']:
		raise EmptyField('Передана пустая строка', 'source')
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
			