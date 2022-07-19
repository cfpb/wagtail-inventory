from wagtail import VERSION as WAGTAIL_VERSION


if WAGTAIL_VERSION >= (3, 0):
    from wagtail import blocks
else:
    from wagtail.core import blocks


class Atom(blocks.StructBlock):
    title = blocks.CharBlock()


class Molecule(blocks.StructBlock):
    title = blocks.CharBlock()
    atoms = blocks.ListBlock(Atom())


class Organism(blocks.StructBlock):
    molecules = blocks.ListBlock(Molecule())
