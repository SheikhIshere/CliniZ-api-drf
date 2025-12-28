"""
BASE/base_pagination.py
"""

from rest_framework import pagination

class BasePagination(pagination.PageNumberPagination):
    page_size = 50  # Number of items per page
    page_size_query_param = 'page_size'
    max_page_size = 100