from rest_framework.response import Response
from rest_framework import pagination


class CustomPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'next_page_url': self.get_next_link(),
            'prev_page_url': self.get_previous_link(),
            'per_page': self.page_size,
            'current_page': self.page.number,
            'last_page': self.page.paginator.num_pages,
            'from': self.page.start_index(),
            'to': self.page.end_index(),
            'total': self.page.paginator.count,
            'data': data
        })
