# -*- coding: utf-8 -*-
from __future__ import absolute_import
from flask import request
from math import ceil

class Pagination(object):
    " Handles Pagination "
    def __init__(self, page, per_page, total_count):
        self.page = page
        self.per_page = per_page
        self.total_count = total_count

    @property
    def pages(self):
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    def iter_pages(self, left_edge=2, left_current=2, right_current=5, right_edge=2):
        last = 0
        for num in xrange(1, self.pages + 1):
            if num <= left_edge or \
               (num > self.page - left_current - 1 and \
                num < self.page + right_current) or \
               num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num

class Paginator(object):
    def __init__(self, app):
        self.app = app
        self.app.config.setdefault('PAGINATION_ITEMS_PER_PAGE', 10)
        self.app.config.setdefault('PAGINATION_PARAM', 'page')        
        self.managers = {}

    def _per_page(self, per_page):
        " number of item to display in each page "
        return per_page or self.app.config['PAGINATION_ITEMS_PER_PAGE']

    def _register_dic(self, f_total, per_page):
        " dic with attributes of an object that's registred for pagination "
        return { 'f_total': f_total,
            'per_page': self._per_page(per_page) }

    def register(self, label, f_total, per_page=None):
        " Register an object for pagination, allowing to use it in any view "
        if not self.managers.has_key(label):
            self.managers[label] = self._register_dic(f_total, per_page)
            manager_attr = 'for_' + label.lower()

    def _manager(self, label):
        " attrs of a registred type "
        for k,v in self.managers.items():
            if k.lower() == label.lower():
                return v
        return None

    def get_manager(self, label):
        " pagination manager object to use in a view "
        manager = self._manager(label)
        return Pagination(self._current_page(), manager['per_page'], manager['f_total']())

    def _current_page(self):
        " gets current page from request "
        return int(request.args.get(self.app.config['PAGINATION_PARAM'], '1'))

    def __getattribute__(self, attr):
        " allow to access any registred type with 'pagination.for_type' "
        if attr.startswith('for_'):
            label = attr.replace('for_', '')         
            return self.get_manager(label)
        else:
            return object.__getattribute__(self, attr)