from django.db import migrations, models
from django.db.models import Count, Min


def remove_duplicates(apps, schema_editor):  # pragma: no cover
    PageBlock = apps.get_model('wagtailinventory', 'PageBlock')

    duplicate_pks_to_keep = (
        PageBlock.objects
            .values('page', 'block')
            .annotate(Min('pk'), count=Count('pk'))
            .filter(count__gt=1)
            .values_list('pk__min', flat=True)
    )

    duplicates_to_keep = PageBlock.objects.in_bulk(duplicate_pks_to_keep)

    for duplicate_to_keep in duplicates_to_keep.values():
        duplicates_to_delete = PageBlock.objects.filter(
            page=duplicate_to_keep.page,
            block=duplicate_to_keep.block
        ).exclude(pk=duplicate_to_keep.pk)

        duplicates_to_delete.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailinventory', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(remove_duplicates, migrations.RunPython.noop),
        migrations.AddConstraint(
            model_name='pageblock',
            constraint=models.UniqueConstraint(fields=('page', 'block'), name='unique_page_block'),
        ),
    ]
