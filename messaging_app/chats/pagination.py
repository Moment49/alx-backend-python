from rest_framework import pagination

class CustomMessagePagination(pagination.PageNumberPagination):
    """This is a custom pagination to be used by the MessageViewSet class"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 50
    page_query_param = 'p'