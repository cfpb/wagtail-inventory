from django.db import models
from wagtail.wagtailadmin.edit_handlers import FieldPanel

try:
    from wagtail.core import blocks as wagtail_blocks
    from wagtail.core.fields import StreamField
    from wagtail.core.models import Page
except ImportError:  # pragma: no cover; fallback for Wagtail <2.0 
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


class NestedStreamBlockPage(Page):
    content = StreamField([
        ('streamblock', wagtail_blocks.StreamBlock([
            ('text', wagtail_blocks.CharBlock()),
            ('atom', blocks.Atom()),
        ])),
    ])

    content_panels = [
        FieldPanel('content'),
    ]
