from django.db import migrations

from ..printers import sync_printer_items


def seed(apps, schema_editor):
    # The historical model, not the live one: this migration has to keep
    # working after Item grows or loses columns.
    sync_printer_items(Item=apps.get_model("atlantis_site", "Item"))


def unseed(apps, schema_editor):
    # Only the rows nothing points at. A printer somebody claimed is referenced
    # by an Order, whose item is PROTECTed — dropping it would fail anyway, and
    # marking it deleted is what the forward path does to a retired printer.
    Item = apps.get_model("atlantis_site", "Item")
    Item.objects.filter(kind="printer", orders__isnull=True).delete()
    Item.objects.filter(kind="printer").update(deleted=True)


class Migration(migrations.Migration):

    dependencies = [
        ("atlantis_site", "0063_pearlbracket_printerclaim_savercredit_weekoutcome_and_more"),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
