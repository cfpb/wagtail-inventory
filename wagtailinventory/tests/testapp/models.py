from django.db import models
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailcore import blocks as wagtail_blocks
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import Page

from wagtailinventory.tests.testapp import blocks


class NoStreamFieldsPage(Page):
    content = models.TextField()

    content_panels = [
        FieldPanel('content'),
    ]


class SingleStreamFieldPage(Page):
    content = StreamField([
        ('text', wagtail_blocks.CharBlock()),
        ('atom', blocks.Atom()),
        ('molecule', blocks.Molecule()),
        ('organism', blocks.Organism()),
    ])

    content_panels = [
        FieldPanel('content'),
    ]


class MultipleStreamFieldsPage(Page):
    first = StreamField([
        ('atom', blocks.Atom()),
        ('molecule', blocks.Molecule()),
        ('organism', blocks.Organism()),
    ])
    second = StreamField([
        ('atom', blocks.Atom()),
        ('molecule', blocks.Molecule()),
        ('organism', blocks.Organism()),
    ])

    content_panels = [
        FieldPanel('first'),
        FieldPanel('second'),
    ]
