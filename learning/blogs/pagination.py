from rest_framework.pagination import PageNumberPagination

class BlogPagination(PageNumberPagination):
    page_size = 5  # Number of blogs per page
    page_size_query_param = 'page'
    max_page_size = 100

