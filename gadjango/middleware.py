"""
Midllewares
"""
import time

from db_handler import get_db_stats

from django.conf import settings
from django.template.loader import render_to_string


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

    def process_response(self, request, response):
        # append GA at the bottom on the page
        response.content = response.content.replace('</body>', '%s</body>' % str(
            render_to_string('gadjango/timing.html', {'ga_stats': self._get_stats()})
        ))

        return response

    def _get_stats(self):
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

        if getattr(settings, 'GADJANGO_DB_STATS', False):
            # get DB stats only if GADJANGO_DB_STATS is True
            db_stats = get_db_stats()
            if db_stats:
                stats.append({
                    'category': 'Django DB',
                    'label': 'total_time',
                    'time': db_stats['total_time'],
                    'view': self._view_name
                })
                stats.append({
                    'category': 'Django DB',
                    'label': 'query_count',
                    'time': db_stats['query_count'],
                    'view': self._view_name
                })

                if getattr(settings, 'GADJANGO_DB_QUERIES', False):
                    # get DB queries if GADJANGO_DB_QUERIES is True
                    # don't use this on live environment!
                    for item in db_stats['queries']:
                        stats.append({
                            'category': 'Django DB',
                            'label': 'sql',
                            'time': item['time'],
                            'view': item['sql']
                        })

        return stats