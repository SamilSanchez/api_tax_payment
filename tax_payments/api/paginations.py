from rest_framework.pagination import PageNumberPagination


class SmallResultSetPagination(PageNumberPagination):
    """
    Paginacion personalizada
    """

    page_size = 5
    page_query_param = "page"
