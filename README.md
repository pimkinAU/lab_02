# streamstats

Читает события из CSV или JSONL построчно и считает по ним статистику.

## Установка

```bash
pip install -e .
```

## Запуск

```bash
python -m streamstats analyze src/streamstats/data/data.jsonl --format jsonl --output report.json
python -m streamstats analyze src/streamstats/data/data.jsonl src/streamstats/data/data2.jsonl --format jsonl --output report.json --skip-invalid
python -m streamstats analyze src/streamstats/data/data.csv --format csv
```

- `--format` — `csv` или `jsonl`
- `--output` — куда сохранить JSON-отчёт (если не указать, итоги просто печатаются)
- `--skip-invalid` — пропускать ошибочные строки вместо остановки

## Формат события

```text
timestamp: ISO 8601
level: DEBUG | INFO | WARNING | ERROR | CRITICAL
source: непустая строка
message: строка
```

## Что в отчёте

- `event_amount` — сколько всего событий
- `levels` — сколько событий каждого уровня
- `sources` — сколько событий от каждого источника
- `errors` — сколько ERROR/CRITICAL от каждого источника
- `top_five` — топ-5 источников ошибок
- `first_date`, `last_date` — первая и последняя временная метка
- `skipped_lines` — сколько строк пропущено

## Ошибки

Без `--skip-invalid` программа останавливается на первой ошибочной строке, пишет файл и номер строки и выходит с кодом `2`.
С `--skip-invalid` строка пропускается, в лог пишется WARNING.

Все ошибки наследуются от `StreamStatsError` (`errors.py`).

## Проверка

```bash
python -m pytest
ruff check .
```
