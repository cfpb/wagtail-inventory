from wagtail.wagtailcore.blocks import StreamValue, StructValue
from wagtail.wagtailcore.fields import StreamField

from wagtailinventory.models import PageBlock


def get_block_name(block):
    return block.__module__ + '.' + block.__class__.__name__


def create_page_block(page, block, value):
    page_block, _ = PageBlock.objects.get_or_create(
        page=page,
        block=get_block_name(block)
    )

    page_blocks = [page_block]

    if isinstance(value, list):
        for subvalue in value:
            page_blocks.extend(create_page_block(
                page,
                block.child_block,
                subvalue
            ))
    elif isinstance(value, StructValue):
        for key, subvalue in value.bound_blocks.items():
            page_blocks.extend(create_page_block(
                page,
                block.child_blocks[key],
                subvalue
            ))
    elif isinstance(value, StreamValue):
        for subvalue in value:
            page_blocks.extend(create_page_block(
                page,
                subvalue.block,
                subvalue.value
            ))

    return page_blocks


def create_page_inventory(page):
    page_blocks = []

    for field in page.specific._meta.fields:
        if not isinstance(field, StreamField):
            continue

        value = getattr(page.specific, field.name)

        for item in value:
            page_blocks.extend(create_page_block(page, item.block, item.value))

    return page_blocks


def get_page_inventory(page=None):
    inventory = PageBlock.objects.all()

    if page:
        inventory = inventory.filter(page=page)

    return inventory


def delete_page_inventory(page=None):
    get_page_inventory(page).delete()


def update_page_inventory(page):
    page_blocks = create_page_inventory(page)

    for page_block in get_page_inventory(page):
        if page_block not in page_blocks:
            page_block.delete()
