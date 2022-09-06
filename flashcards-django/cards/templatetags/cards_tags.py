from django import template

from cards.models import BOXES, Card

register = template.Library()


@register.inclusion_tag("cards/box_links.html")
def boxes_as_links():
    return {
        "boxes": [
            {"number": box_num, "card_count": Card.objects.filter(box=box_num).count()}
            for box_num in BOXES
        ]
    }
