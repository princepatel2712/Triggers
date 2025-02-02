# Generated by Django 5.0.6 on 2024-05-21 09:05

import pgtrigger.compiler
import pgtrigger.migrations
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('test_trigger', '0019_appendonlymodel_append_only'),
    ]

    operations = [
        pgtrigger.migrations.RemoveTrigger(
            model_name='appendonlymodel',
            name='append_only',
        ),
        pgtrigger.migrations.AddTrigger(
            model_name='appendonlymodel',
            trigger=pgtrigger.compiler.Trigger(name='append_only_with_calculation', sql=pgtrigger.compiler.UpsertTriggerSql(func="\n            BEGIN\n                -- Perform a calculation or check\n                IF NEW.my_field < 0 THEN\n                    RAISE EXCEPTION 'my_field cannot be negative';\n                END IF;\n\n                -- Protect the row from updates or deletes\n                RAISE EXCEPTION 'Operation not allowed on this table';\n                RETURN NULL;\n            END;\n        ", hash='45fa6c8294f1bb41d1cc3d4a378ca37fea869180', operation='UPDATE OR DELETE', pgid='pgtrigger_append_only_with_calculation_ab17d', table='test_trigger_appendonlymodel', when='BEFORE')),
        ),
    ]
