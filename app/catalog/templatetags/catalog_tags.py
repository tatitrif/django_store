import logging
from typing import List

from django import template
from django.core.paginator import Paginator

from ..models import Category

register = template.Library()

logger = logging.getLogger(__name__)


@register.simple_tag
def get_proper_elided_page_range(
    paginator, number, on_each_side=1, on_ends=1
) -> List[int]:
    """
    Returns a list of page numbers for the paginator, with ellipses to indicate
    hidden pages.

    :param paginator: The paginator object.
    :param number: The current page number.
    :param on_each_side: The number of page numbers to display on each side of the
        current page number.
    :param on_ends: The number of page numbers to display at the beginning and end
        of the page range.
    :return: A list of page numbers for the paginator.
    """
    paginator = Paginator(paginator.object_list, paginator.per_page)
    return paginator.get_elided_page_range(
        number=number, on_each_side=on_each_side, on_ends=on_ends
    )


@register.simple_tag
def category_tree():
    category = Category.get_all_categories()
    return category
