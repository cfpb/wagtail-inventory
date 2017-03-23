from __future__ import absolute_import, unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from wagtail.wagtailcore.models import Page


@python_2_unicode_compatible
class PageBlock(models.Model):
    page = models.ForeignKey(Page, related_name='page_blocks')
    block = models.CharField(max_length=255, db_index=True)

    def __str__(self):
        return '<{}, {}>'.format(self.page, self.block)
