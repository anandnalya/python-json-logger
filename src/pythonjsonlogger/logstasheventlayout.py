from pythonjsonlogger.jsonlogger import JsonFormatter

import socket
from datetime import datetime
from datetime import timezone


class LogstashEventLayout(JsonFormatter):
    _rename_fields = {
        'name': 'logger_name',
        'threadName': 'thread_name',
        'processName': 'process_name',
        'pathname': 'file',
        'funcName': 'method',
        'module': 'class',
        'lineno': 'line_number'
    }

    _static_fields = {
        'source_host': socket.gethostname(),
        '@version': 1
    }

    def __init__(self, *args, **kwargs):
        super(LogstashEventLayout, self).__init__(
            *args,
            static_fields=LogstashEventLayout._static_fields,
            rename_fields=LogstashEventLayout._rename_fields,
            **kwargs
        )

    def add_fields(self, log_record, record, message_dict):
        super(LogstashEventLayout, self).add_fields(log_record, record, message_dict)
        log_record['@timestamp'] = datetime.fromtimestamp(record.created, tz=timezone.utc).strftime(
            '%Y-%m-%dT%H:%M:%S.%fZ')[:-4] + 'Z'
        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname
        if record.exc_info is not None:
            log_record['exception_class'] = f'{record.exc_info[0].__module__}.{record.exc_info[0].__name__}'
            log_record['exception_message'] = getattr(record.exc_info[1], 'message', repr(record.exc_info[1]))
            log_record['stack_trace'] = record.exc_info[2]
            if 'exc_info' in log_record:
                del log_record['exc_info']
