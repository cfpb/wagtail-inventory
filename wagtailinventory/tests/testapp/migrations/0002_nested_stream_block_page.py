# -*- coding: utf-8 -*-
import django.db.models.deletion
from django.db import migrations, models

from wagtail import blocks as core_blocks
from wagtail import fields as core_fields


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NestedStreamBlockPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('content', core_fields.StreamField([('streamblock', core_blocks.StreamBlock([('text', core_blocks.CharBlock()), ('atom', core_blocks.StructBlock([('title', core_blocks.CharBlock())]))]))], use_json_field=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
