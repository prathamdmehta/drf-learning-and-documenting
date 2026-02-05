from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    # Name of the query parameter used to control page size.
    # Example: ?page_size=5
    page_size_query_param = 'page_size'

    # Name of the query parameter used to select the page number.
    # Default in DRF is "page", here you customize it to "page-num".
    # Example: ?page-num=2
    page_query_param = 'page-num'

    # Maximum number of items allowed per page, even if
    # the client asks for a larger page_size.
    max_page_size = 1

    # Customize the structure of the paginated response.
    # DRF will call this method when returning paginated data.
    def get_paginated_response(self, data):
        return Response({
            # URL to the next page (or None if there is no next page)
            'next': self.get_next_link(),

            # URL to the previous page (or None if there is no previous page)
            'previous': self.get_previous_link(),

            # Total number of objects across all pages
            'count': self.page.paginator.count,

            # Current page size (how many items are in this page)
            'page_size': self.page_size,

            # Actual list of serialized objects for this page
            'results': data
        })