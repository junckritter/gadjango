"""
Midllewares
"""

class TimingMiddleware(object):
    """
    """

    def process_request(self, request):
        return None

    def process_template_response(self, request):
        return request

