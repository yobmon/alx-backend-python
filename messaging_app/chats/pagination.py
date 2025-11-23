## chats/pagination.py
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class MessagePagination(PageNumberPagination):
    page_size = 20  # 20 messages per page
    page_size_query_param = 'page_size'  # optional: allow client override
    max_page_size = 50

    # Customize the response to include total count
    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,  # ✅ This is what the test is checking
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })
