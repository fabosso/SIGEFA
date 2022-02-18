from urllib.parse import urlparse
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


def clean_scheme_url(url):
   if url:
      parse_result = urlparse(url)
      url_path = f"{parse_result.path}?{parse_result.query}"
      return url_path
   return None


class CustomPagination(PageNumberPagination):
   page_size = 5

   def get_paginated_response(self, data):
      next_link = clean_scheme_url(self.get_next_link())
      previous_link = clean_scheme_url(self.get_previous_link())
      return Response({
         'links': {
            'next': next_link,
            'previous': previous_link,
            'current': self.request.query_params.get('page', None)
         },
         'page_links': self.get_pages_context(),
         'count': self.page.paginator.count,
         'results': data
      })
   
   def get_pages_context(self):
      page_links = dict()
      pages_list = list()
      page_context = self.get_html_context()
      pages = page_context['page_links']

      for page in pages:
         p = {
            'url': clean_scheme_url(page.url),
            'number': page.number,
            'is_break': page.is_break,
            'is_active': page.is_active,
         }
         pages_list.append(p)
      page_links['page_links'] = pages_list

      return page_links


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
   #  page_size_query_param = 'page_size'
   #  max_page_size = 1000
