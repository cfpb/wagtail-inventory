from django.db import models

from wagtail.core.models import Page


class PageBlock(models.Model):
    page = models.ForeignKey(
        Page, related_name="page_blocks", on_delete=models.CASCADE
    )
    block = models.CharField(max_length=255, db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["page", "block"], name="unique_page_block"
            ),
        ]

    def __str__(self):
        return "<{}, {}>".format(self.page, self.block)
