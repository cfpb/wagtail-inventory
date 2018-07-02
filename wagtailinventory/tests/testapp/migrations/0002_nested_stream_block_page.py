# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion

try:
    from wagtail.core import blocks as core_blocks
    from wagtail.core import fields as core_fields  # pragma: no cover
except ImportError:  # pragma: no cover; fallback for Wagtail <2.0
    from wagtail.wagtailcore import blocks as core_blocks
    from wagtail.wagtailcore import fields as core_fields


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NestedStreamBlockPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('content', core_fields.StreamField([('streamblock', core_blocks.StreamBlock([('text', core_blocks.CharBlock()), ('atom', core_blocks.StructBlock([('title', core_blocks.CharBlock())]))]))])),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
