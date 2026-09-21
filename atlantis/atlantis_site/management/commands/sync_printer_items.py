"""Bring the hidden printer shop rows back in line with printers.py.

The trees in printers.py are the source of truth for what a printer costs; the
Item rows behind them exist only so that claiming one becomes an ordinary order
fulfillment can post. A data migration seeded them, and this is how they are
brought back into step whenever the trees are edited — a new printer, a moved
price, a retired tier.

Idempotent: run it after any change to printers.py, or on every deploy.
"""

from django.core.management.base import BaseCommand

from ...printers import sync_printer_items


class Command(BaseCommand):
    help = "Create or update the hidden shop Items backing each printer."

    def handle(self, *args, **options):
        counts = sync_printer_items()
        self.stdout.write(self.style.SUCCESS(
            f"Printer items: {counts['created']} created, "
            f"{counts['updated']} updated, {counts['retired']} retired."
        ))
