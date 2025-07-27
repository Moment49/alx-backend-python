from rest_framework import pagination
from rest_framework.response import Response 

class CustomMessagePagination(pagination.PageNumberPagination):
    """This is a custom pagination to be used by the MessageViewSet class"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 50
    page_query_param = 'p'

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        })