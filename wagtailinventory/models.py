from django.db import models

from wagtail.models import Page


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

    wagtail_reference_index_ignore = True

    def __str__(self):
        return f"<{self.page}, {self.block}>"
