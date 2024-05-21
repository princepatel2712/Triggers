# Generated by Django 5.0.6 on 2024-05-21 06:30

import pgtrigger.compiler
import pgtrigger.migrations
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_trigger', '0011_bookmodel_mymodel_post_protectedmodel_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('old_field', models.CharField(max_length=32)),
                ('new_field', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='TrackedModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field', models.CharField(max_length=32)),
            ],
        ),
        pgtrigger.migrations.AddTrigger(
            model_name='trackedmodel',
            trigger=pgtrigger.compiler.Trigger(name='track_history', sql=pgtrigger.compiler.UpsertTriggerSql(func='\n                                INSERT INTO test_trigger_historymodel(old_field, new_field)\n                                SELECT \n                                    old_values.field AS old_field,\n                                    new_values.field AS new_field\n                                    FROM old_values\n                                        JOIN new_values ON old_values.id = new_values.id;\n                                        RETURN NULL; \n            ', hash='84084b81fcbda8ac6ce6fb6a107cef85a0cde547', level='STATEMENT', operation='UPDATE', pgid='pgtrigger_track_history_42d2e', referencing='REFERENCING OLD TABLE AS old_values  NEW TABLE AS new_values ', table='test_trigger_trackedmodel', when='AFTER')),
        ),
    ]
