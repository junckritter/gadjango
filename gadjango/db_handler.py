"""
Database handlers for gadjango.
"""
from time import time

from django.db import connections
from django.db.backends.util import CursorWrapper, CursorDebugWrapper


def execute(self, sql, params=()):
    start = time()
    try:
        return self.cursor.execute(sql, params)
    finally:
        stop = time()
        duration = stop - start
        sql = self.db.ops.last_executed_query(self.cursor, sql, params)
        self.db.queries.append({
            'sql': sql,
            'time': int(float("%.6f" % duration) * 1000000),
        })


def executemany(self, sql, param_list):
    start = time()
    try:
        return self.cursor.executemany(sql, param_list)
    finally:
        stop = time()
        duration = stop - start
        self.db.queries.append({
            'sql': '%s times: %s' % (len(param_list), sql),
            'time': int(float("%.6f" % duration) * 1000000),
        })


setattr(CursorWrapper, 'execute', execute)
setattr(CursorWrapper, 'executemany', execute)

setattr(CursorDebugWrapper, 'execute', execute)
setattr(CursorDebugWrapper, 'executemany', execute)


def get_db_stats():
    """
    Get queries from all connections.
    """
    all_queries = []
    for c in connections.all():
        for q in c.queries:
            all_queries.append({
                'time': q['time'],
                'sql': '%s:%s' % (c.alias, q['sql'])
            })

    return all_queries
