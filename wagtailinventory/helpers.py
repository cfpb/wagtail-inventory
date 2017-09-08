from itertools import chain

from wagtail.wagtailcore.blocks import ListBlock, StructBlock
from wagtail.wagtailcore.fields import StreamField

from wagtailinventory.models import PageBlock


def get_block_name(block):
    return block.__module__ + '.' + block.__class__.__name__


def get_page_blocks(page):
    blocks = []

    for field in page.specific._meta.fields:
        if not isinstance(field, StreamField):
            continue

        for stream_child in getattr(page.specific, field.name):
            blocks.extend(get_field_blocks(stream_child))

    return sorted(set(map(get_block_name, blocks)))


def get_field_blocks(value):
    block = getattr(value, 'block', None)
    blocks = [block] if block else []

    if isinstance(value, list):
        child_blocks = value
    if isinstance(block, StructBlock):
        if hasattr(value, 'bound_blocks'):
            child_blocks = value.bound_blocks.values()
        else:
            child_blocks = [value.value]
    elif isinstance(block, ListBlock):
        child_blocks = value.value
    else:
        child_blocks = []

    blocks.extend(chain(*map(get_field_blocks, child_blocks)))

    return blocks


def get_page_inventory(page=None):
    inventory = PageBlock.objects.all()

    if page:
        inventory = inventory.filter(page=page)

    return inventory


def create_page_inventory(page):
    page_blocks = get_page_blocks(page)

    return [
        PageBlock.objects.get_or_create(page=page, block=block)[0]
        for block in page_blocks
    ]


def delete_page_inventory(page=None):
    get_page_inventory(page).delete()


def update_page_inventory(page):
    page_blocks = create_page_inventory(page)

    for page_block in get_page_inventory(page):
        if page_block not in page_blocks:
            page_block.delete()
