# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0032_add_bulk_delete_page_permission'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageBlock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('block', models.CharField(db_index=True, max_length=255)),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='page_blocks', to='wagtailcore.Page')),
            ],
        ),
    ]
