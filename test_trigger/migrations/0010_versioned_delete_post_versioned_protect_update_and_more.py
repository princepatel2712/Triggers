# Generated by Django 5.0.6 on 2024-05-21 06:16

import pgtrigger.compiler
import pgtrigger.migrations
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_trigger', '0009_remove_post_freeze_published_model_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Versioned',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.IntegerField(default=0)),
                ('char_field', models.CharField(max_length=32)),
            ],
        ),
        migrations.DeleteModel(
            name='Post',
        ),
        pgtrigger.migrations.AddTrigger(
            model_name='versioned',
            trigger=pgtrigger.compiler.Trigger(name='protect_update', sql=pgtrigger.compiler.UpsertTriggerSql(condition='WHEN (OLD."version" IS DISTINCT FROM (NEW."version"))', func="RAISE EXCEPTION 'pgtrigger: Cannot update rows from % table', TG_TABLE_NAME;", hash='b9280eaa5e037f66a670677381fa3121b84ab548', operation='UPDATE', pgid='pgtrigger_protect_update_57b21', table='test_trigger_versioned', when='BEFORE')),
        ),
        pgtrigger.migrations.AddTrigger(
            model_name='versioned',
            trigger=pgtrigger.compiler.Trigger(name='versioning', sql=pgtrigger.compiler.UpsertTriggerSql(condition='WHEN (OLD.* IS DISTINCT FROM NEW.*)', func='NEW.version = NEW.version + 1;RETURN NEW;', hash='f342d4629c453ac2b8633f63f9b09b7198adedee', operation='UPDATE', pgid='pgtrigger_versioning_bedd2', table='test_trigger_versioned', when='BEFORE')),
        ),
    ]
