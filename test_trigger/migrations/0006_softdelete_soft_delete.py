# Generated by Django 4.2.11 on 2024-05-21 05:52

from django.db import migrations
import pgtrigger.compiler
import pgtrigger.migrations


class Migration(migrations.Migration):

    dependencies = [
        ('test_trigger', '0005_softdelete_delete_timestampmodel'),
    ]

    operations = [
        pgtrigger.migrations.AddTrigger(
            model_name='softdelete',
            trigger=pgtrigger.compiler.Trigger(name='soft_delete', sql=pgtrigger.compiler.UpsertTriggerSql(func='UPDATE "test_trigger_softdelete" SET is_active = False WHERE "id" = OLD."id"; RETURN NULL;', hash='90e15a798b29805e7fd60d2cdeb70f343008e6f6', operation='DELETE', pgid='pgtrigger_soft_delete_2f6e6', table='test_trigger_softdelete', when='BEFORE')),
        ),
    ]
