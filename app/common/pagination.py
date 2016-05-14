from flask import render_template, flash, redirect, url_for, request
from google.appengine.ext import ndb
from math import ceil
import logging

PER_PAGE = 10

class Pagination(object):

    def __init__(self, page, query, per_page=PER_PAGE ):
        self._page      = page
        self._per_page  = per_page
        self._queryArgs = dict(offset=(page-1)*per_page, limit=per_page)
        self._query     = query
        self._qit       = query.iter(offset=(page-1)*per_page, limit=per_page)
        self._pages     = query.count_async()

    def __repr__(self):
        return '<Pagination - page: %s, next_page: %s, prev_page: %s, pages: %s>' %( str(self.page), str(self.next_page), str(self.prev_page), str(self.pages))

    @property
    def pages(self):
        total_count = self._pages.get_result()
        return int(ceil(total_count / float(self._per_page)))

    @property
    def has_prev(self):
        return self._page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    @property
    def prev_page(self):
        return self.page - 1 if self.has_prev else -1

    @property
    def next_page(self):
        return self.page + 1 if self.has_next else -1

    def __nonzero__(self):
        return self.has_prev or self.has_next

    def get_posts_async(self):
        return self._query.fetch_async(**self._queryArgs)

    @ndb.tasklet
    def items(self):
        results = []
        while (yield self._qit.has_next_async()):
          entity = self._qit.next() # this will always be articles in our case
          results.append(entity)
        raise ndb.Return(results)

    @property
    def page(self):
        return self._page

    def iter_pages(self, left_edge=2, left_current=2, right_current=5, right_edge=2):
        last = 0
        for num in xrange(1, self.pages + 1):
          if num <= left_edge or (num > self.page - left_current - 1 and num < self.page + right_current) or num > self.pages - right_edge:
            if last + 1 != num:
              yield None
            yield num
            last = num
