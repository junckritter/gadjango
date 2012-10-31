"""
Midllewares
"""
import time

from db_handler import get_db_stats


class TimingMiddleware(object):
    """
    """

    def process_request(self, request):
        self._start_total_time = time.time()
        return None

    def process_view(self, request, view_func, view_args, view_kwargs):
        self._start_view_time = time.time()
        self._view_name = view_func.__name__
        return None

    def process_template_response(self, request, response):
        now = time.time()
        stats = [
            {
                'category': 'Django View',
                'label': 'view_time',
                'time': int((now - self._start_view_time) * 1000),
                'view': self._view_name
            },
            {
                'category': 'Django View',
                'label': 'total_time',
                'time': int((now - self._start_total_time) * 1000),
                'view': self._view_name
            }
        ]

        db_stats = get_db_stats()
        if db_stats:
            for item in db_stats:
                stats.append({
                    'category': 'Django DB',
                    'label': 'sql',
                    'time': item['time'],
                    'view': item['sql']
                })

        response.context_data.update({'ga_stats': stats})
        return response
