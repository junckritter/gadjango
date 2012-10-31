"""
Midllewares
"""

import time

class TimingMiddleware(object):
    """
    """

    def process_request(self, request):
        self.request._start_total_time = time.time()
        return None

    def process_view(self, request, view_func, view_args, view_kwargs):
        self.request._start_view_time = time.time()
        self.request._view_name = view_func.__name__
        return None


    def process_template_response(self, request, response):
        now = time.time()
        stats = [
            {
                'category': 'Django View',
                'label': 'view_time',
                'time': int((now - self.request._start_view_time) * 1000),
                'view': self.request._view_name
            },
            {
                'category': 'Django View',
                'label': 'total_time',
                'time': int((now - self.request._start_total_time) * 1000),
                'view': self.request._view_name
            }
        ]
        response.context_data.update({'ga_stats': stats})
        return response

