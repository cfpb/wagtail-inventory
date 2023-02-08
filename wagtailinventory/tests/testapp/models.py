from django.db import models

from wagtail import blocks as wagtail_blocks
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page

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
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("content"),
    ]


class MultipleStreamFieldsPage(Page):
    first = StreamField(
        [
            ("atom", blocks.Atom()),
            ("molecule", blocks.Molecule()),
            ("organism", blocks.Organism()),
        ],
        use_json_field=True,
    )
    second = StreamField(
        [
            ("atom", blocks.Atom()),
            ("molecule", blocks.Molecule()),
            ("organism", blocks.Organism()),
        ],
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("first"),
        FieldPanel("second"),
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
        ],
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("content"),
    ]
