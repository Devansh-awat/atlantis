"""The pending counts the admin rail wears next to each desk.

A reviewer arriving at /root asks one question first — which queue needs me? —
and answering it used to mean opening all five pages. The badges put the answer
in the sidebar, so the rail is the triage.

Counted per link rather than all at once on purpose: the navbar only renders
the desks a reviewer has permission for, so a T1-only reviewer never pays for
the T3 count.
"""

from django import template
from django.utils.html import format_html

from ..models import Order
from ..views.admin.queue import QUEUES

register = template.Library()

# Past this the exact number stops being information a reviewer acts on, and a
# four-digit badge would push the rail's links around.
BADGE_MAX = 99


def pending_count(key):
    """How many things are waiting on one desk.

    The review desks answer with their own queue — the same set `next` walks —
    so a badge can never disagree with the page it links to.
    """
    if key == "fulfillment":
        return Order.objects.filter(status=Order.OrderStatus.PENDING).count()
    return QUEUES[key].pending().count()


@register.simple_tag
def nav_badge(key):
    """The rail's badge for one desk — nothing at all when it's empty.

    An empty queue is the state that needs no attention, and a rail of zeroes
    is five things to read past on the way to the one that isn't.
    """
    count = pending_count(key)
    if not count:
        return ""
    return format_html(
        '<span class="nav-badge" title="{} pending">{}</span>',
        count,
        count if count <= BADGE_MAX else f"{BADGE_MAX}+",
    )
