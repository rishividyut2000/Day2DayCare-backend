from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = "size"
    max_page_size = 200

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ("items", data),
            ("page", self.page.number),
            ("size", self.get_page_size(self.request)),
            ("total", self.page.paginator.count),
        ]))
