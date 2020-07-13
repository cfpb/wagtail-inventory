from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core import blocks as wagtail_blocks
from wagtail.core.fields import StreamField
from wagtail.core.models import Page

from wagtailinventory.tests.testapp import blocks


class NoStreamFieldsPage(Page):
    content = models.TextField()

    content_panels = Page.content_panels + [
        FieldPanel("content"),
    ]


class SingleStreamFieldPage(Page):
    content = StreamField(
        [
            ("atom", blocks.Atom()),
            ("molecule", blocks.Molecule()),
            ("organism", blocks.Organism()),
        ],
        blank=True,
    )

    content_panels = Page.content_panels + [
        StreamFieldPanel("content"),
    ]


class MultipleStreamFieldsPage(Page):
    first = StreamField(
        [
            ("atom", blocks.Atom()),
            ("molecule", blocks.Molecule()),
            ("organism", blocks.Organism()),
        ]
    )
    second = StreamField(
        [
            ("atom", blocks.Atom()),
            ("molecule", blocks.Molecule()),
            ("organism", blocks.Organism()),
        ]
    )

    content_panels = Page.content_panels + [
        StreamFieldPanel("first"),
        StreamFieldPanel("second"),
    ]


class NestedStreamBlockPage(Page):
    content = StreamField(
        [
            (
                "streamblock",
                wagtail_blocks.StreamBlock(
                    [
                        ("text", wagtail_blocks.CharBlock()),
                        ("atom", blocks.Atom()),
                    ]
                ),
            ),
        ]
    )

    content_panels = Page.content_panels + [
        StreamFieldPanel("content"),
    ]
