# -*- coding: utf-8 -*-
import django.db.models.deletion
from django.db import migrations, models

from wagtail import blocks as core_blocks
from wagtail import fields as core_fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0032_add_bulk_delete_page_permission'),
    ]

    operations = [
        migrations.CreateModel(
            name='MultipleStreamFieldsPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('first', core_fields.StreamField([('atom', core_blocks.StructBlock([('title', core_blocks.CharBlock())])), ('molecule', core_blocks.StructBlock([('title', core_blocks.CharBlock()), ('atoms', core_blocks.ListBlock(core_blocks.StructBlock([('title', core_blocks.CharBlock())])))])), ('organism', core_blocks.StructBlock([('molecules', core_blocks.ListBlock(core_blocks.StructBlock([('title', core_blocks.CharBlock()), ('atoms', core_blocks.ListBlock(core_blocks.StructBlock([('title', core_blocks.CharBlock())])))])))]))], use_json_field=True)),
                ('second', core_fields.StreamField([('atom', core_blocks.StructBlock([('title', core_blocks.CharBlock())])), ('molecule', core_blocks.StructBlock([('title', core_blocks.CharBlock()), ('atoms', core_blocks.ListBlock(core_blocks.StructBlock([('title', core_blocks.CharBlock())])))])), ('organism', core_blocks.StructBlock([('molecules', core_blocks.ListBlock(core_blocks.StructBlock([('title', core_blocks.CharBlock()), ('atoms', core_blocks.ListBlock(core_blocks.StructBlock([('title', core_blocks.CharBlock())])))])))]))], use_json_field=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='NoStreamFieldsPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('content', models.TextField()),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='SingleStreamFieldPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('content', core_fields.StreamField([('text', core_blocks.CharBlock()), ('atom', core_blocks.StructBlock([('title', core_blocks.CharBlock())])), ('molecule', core_blocks.StructBlock([('title', core_blocks.CharBlock()), ('atoms', core_blocks.ListBlock(core_blocks.StructBlock([('title', core_blocks.CharBlock())])))])), ('organism', core_blocks.StructBlock([('molecules', core_blocks.ListBlock(core_blocks.StructBlock([('title', core_blocks.CharBlock()), ('atoms', core_blocks.ListBlock(core_blocks.StructBlock([('title', core_blocks.CharBlock())])))])))]))], use_json_field=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
