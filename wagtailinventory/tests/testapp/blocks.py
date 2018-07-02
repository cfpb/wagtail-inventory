try:
    from wagtail.core import blocks
except ImportError:  # pragma: no cover; fallback for Wagtail <2.0
    from wagtail.wagtailcore import blocks


class Atom(blocks.StructBlock):
    title = blocks.CharBlock()


class Molecule(blocks.StructBlock):
    title = blocks.CharBlock()
    atoms = blocks.ListBlock(Atom())


class Organism(blocks.StructBlock):
    molecules = blocks.ListBlock(Molecule())
