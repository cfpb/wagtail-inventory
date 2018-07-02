# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

try:
    from wagtail.core import blocks as core_blocks
    from wagtail.core import fields as core_fields  # pragma: no cover
except ImportError:  # pragma: no cover; fallback for Wagtail <2.0
    from wagtail.wagtailcore import blocks as core_blocks
    from wagtail.wagtailcore import fields as core_fields


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0002_nested_stream_block_page'),
    ]

    operations = [
        migrations.AlterField(
            model_name='singlestreamfieldpage',
            name='content',
            field=core_fields.StreamField([('atom', core_blocks.StructBlock([('title', core_blocks.CharBlock())])), ('molecule', core_blocks.StructBlock([('title', core_blocks.CharBlock()), ('atoms', core_blocks.ListBlock(core_blocks.StructBlock([('title', core_blocks.CharBlock())])))])), ('organism', core_blocks.StructBlock([('molecules', core_blocks.ListBlock(core_blocks.StructBlock([('title', core_blocks.CharBlock()), ('atoms', core_blocks.ListBlock(core_blocks.StructBlock([('title', core_blocks.CharBlock())])))])))]))], blank=True),
        ),
    ]
