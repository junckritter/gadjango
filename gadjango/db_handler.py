"""
Database handlers for gadjango.
"""
from datetime import datetime

from django.db import connections
from django.db.backends.util import CursorWrapper, CursorDebugWrapper


def execute(self, sql, params=()):
    start = datetime.now()
    try:
        return self.cursor.execute(sql, params)
    finally:
        self.db.queries.append({
            'sql': sql,
            'time': _ms(datetime.now() - start),
        })


def executemany(self, sql, param_list):
    start = datetime.now()
    try:
        return self.cursor.executemany(sql, param_list)
    finally:
        self.db.queries.append({
            'sql': '%s times: %s' % (len(param_list), sql),
            'time': _ms(datetime.now() - start),
        })


setattr(CursorWrapper, 'execute', execute)
setattr(CursorWrapper, 'executemany', execute)

setattr(CursorDebugWrapper, 'execute', execute)
setattr(CursorDebugWrapper, 'executemany', execute)


def get_db_stats():
    """
    Get queries from all connections.
    """
    total_time = 0.0
    queries = []
    for c in connections.all():
        for q in c.queries:
            queries.append({
                'time': int(float('%.3f' % q['time'])),
                'sql': '%s: %s' % (c.alias, q['sql'][:64].replace('\n', ' ').replace("'", "\\'"))
            })
            total_time += q['time']

    return {
        'queries': queries,
        'total_time': int(float('%.3f' % total_time)),
        'query_count': len(queries)
    }


def _ms(time_delta):
    return int((time_delta.days * 24 * 60 * 60 + time_delta.seconds) * 1000 + time_delta.microseconds / 1000.0)
