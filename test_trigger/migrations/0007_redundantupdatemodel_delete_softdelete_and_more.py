# Generated by Django 4.2.11 on 2024-05-21 05:56

from django.db import migrations, models
import pgtrigger.compiler
import pgtrigger.migrations


class Migration(migrations.Migration):

    dependencies = [
        ('test_trigger', '0006_softdelete_soft_delete'),
    ]

    operations = [
        migrations.CreateModel(
            name='RedundantUpdateModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('redundant_field1', models.BooleanField(default=False)),
                ('redundant_field2', models.BooleanField(default=False)),
            ],
        ),
        migrations.DeleteModel(
            name='SoftDelete',
        ),
        pgtrigger.migrations.AddTrigger(
            model_name='redundantupdatemodel',
            trigger=pgtrigger.compiler.Trigger(name='protect_redundant_updates', sql=pgtrigger.compiler.UpsertTriggerSql(condition='WHEN (OLD.* IS NOT DISTINCT FROM NEW.*)', func="RAISE EXCEPTION 'pgtrigger: Cannot update rows from % table', TG_TABLE_NAME;", hash='7866a4e24c41e73826aff55c0f7a916cdb2d6dc4', operation='UPDATE', pgid='pgtrigger_protect_redundant_updates_148a7', table='test_trigger_redundantupdatemodel', when='BEFORE')),
        ),
    ]
