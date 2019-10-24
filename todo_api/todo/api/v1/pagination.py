from rest_framework.pagination import (
    LimitOffsetPagination, PageNumberPagination,
)


class TodoLimitoffSetPagination(LimitOffsetPagination):
    default_limit = 5
    max_limit     = 5


class TodoPageNumberPagination(PageNumberPagination):
    page_size     = 5


