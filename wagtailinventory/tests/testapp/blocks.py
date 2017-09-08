from wagtail.wagtailcore import blocks


class Atom(blocks.StructBlock):
    title = blocks.CharBlock()


class Molecule(blocks.StructBlock):
    title = blocks.CharBlock()
    atoms = blocks.ListBlock(Atom())


class Organism(blocks.StructBlock):
    molecules = blocks.ListBlock(Molecule())
