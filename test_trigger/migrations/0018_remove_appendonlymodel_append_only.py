# Generated by Django 5.0.6 on 2024-05-21 07:31

import pgtrigger.migrations
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('test_trigger', '0017_remove_post_freeze_published_model'),
    ]

    operations = [
        pgtrigger.migrations.RemoveTrigger(
            model_name='appendonlymodel',
            name='append_only',
        ),
    ]
