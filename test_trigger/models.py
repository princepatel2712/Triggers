from django.db import models
from django.contrib.auth.models import User
import pgtrigger
from .triggers import append_only_with_check, prevent_update_delete_when_quantity_zero, \
    prevent_update_delete_on_processed_transactions, transaction_audit


class ProtectedModel(models.Model):
    """Active object cannot be deleted!"""
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        triggers = [
            pgtrigger.Protect(name="protect_deletes", operation=pgtrigger.Delete)
        ]


class BookModel(models.Model):
    name = models.CharField(max_length=40)
    status = models.CharField(max_length=32, default='unpublished')
    is_active = models.BooleanField(default=True)

    class Meta:
        triggers = [
            pgtrigger.FSM(
                name='status_fsm',
                field='status',
                transitions=[
                    ('unpublished', 'published'),
                    ('published', 'inactive')
                ]
            ),
            pgtrigger.SoftDelete(
                name='soft_delete',
                field='is_active'
            )
        ]


class MyModel(models.Model):
    int_field = models.IntegerField()
    in_sync_int = models.IntegerField(help_text="Stays the same as int_field")

    class Meta:
        triggers = [
            pgtrigger.Trigger(
                name="keep_in_sync",
                operation=pgtrigger.Update | pgtrigger.Insert,
                when=pgtrigger.Before,
                func="NEW.in_sync_int = NEW.int_field; RETURN NEW;",
            )
        ]


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    editable_value = models.TextField()

    class Meta:
        triggers = [
            pgtrigger.ReadOnly(name="read_only_created_at", fields=["created_at"])
        ]


class SoftDelete(models.Model):
    is_active = models.BooleanField(default=True)

    class Meta:
        triggers = [
            pgtrigger.SoftDelete(name="soft_delete", field="is_active")
        ]


class RedundantUpdateModel(models.Model):
    redundant_field1 = models.BooleanField(default=False)
    redundant_field2 = models.BooleanField(default=False)

    class Meta:
        triggers = [
            pgtrigger.Protect(name='protect_redundant_updates',
                              operation=pgtrigger.Update,
                              condition=pgtrigger.AnyDontChange()
                              )
        ]


class Post(models.Model):
    status = models.CharField(default="unpublished")
    content = models.TextField()

    class Meta:
        triggers = [
            # pgtrigger.Protect(name="freeze_published_model",
            #                   operation=pgtrigger.Update,
            #                   condition=pgtrigger.Q(old__status="published")),
            pgtrigger.Protect(
                name="freeze_publish_model_allowed_deactivate",
                operation=pgtrigger.Update,
                condition=(
                        pgtrigger.Q(old__status="published")
                        & ~pgtrigger.Q(new__status="inactive")
                )
            )
        ]


class Versioned(models.Model):
    version = models.IntegerField(default=0)
    char_field = models.CharField(max_length=32)

    class Meta:
        triggers = [
            pgtrigger.Protect(name='protect_update',
                              operation=pgtrigger.Update,
                              condition=pgtrigger.AnyChange("version")),
            pgtrigger.Trigger(name="versioning",
                              when=pgtrigger.Before,
                              operation=pgtrigger.Update,
                              func="NEW.version = NEW.version + 1;RETURN NEW;",
                              condition=pgtrigger.AnyChange())
        ]


class HistoryModel(models.Model):
    old_field = models.CharField(max_length=32)
    new_field = models.CharField(max_length=32)


class TrackedModel(models.Model):
    field = models.CharField(max_length=32)

    class Meta:
        triggers = [
            pgtrigger.Trigger(name="track_history",
                              level=pgtrigger.Statement,
                              when=pgtrigger.After,
                              operation=pgtrigger.Update,
                              referencing=pgtrigger.Referencing(old="old_values", new="new_values"),
                              func=f"""
                                INSERT INTO {HistoryModel._meta.db_table}(old_field, new_field)
                                SELECT 
                                    old_values.field AS old_field,
                                    new_values.field AS new_field
                                    FROM old_values
                                        JOIN new_values ON old_values.id = new_values.id;
                                        RETURN NULL; 
            """)
        ]


class UpdateCheck(models.Model):
    int_field = models.IntegerField()
    char_field = models.CharField(null=True)

    class Meta:
        triggers = [
            pgtrigger.Protect(name="update_check",
                              operation=pgtrigger.Update,
                              condition=~pgtrigger.AnyChange()),
            pgtrigger.Protect(name="change_protect_update_check",
                              operation=pgtrigger.Update,
                              condition=pgtrigger.AnyChange("int_field", "char_field"))
        ]


class AppendOnlyModel(models.Model):
    my_field = models.IntegerField()

    class Meta:
        triggers = [
            append_only_with_check()
        ]


class Product(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()

    class Meta:
        triggers = [
            prevent_update_delete_when_quantity_zero()
        ]


class Transaction(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    processed = models.BooleanField(default=False)

    class Meta:
        triggers = [
            prevent_update_delete_on_processed_transactions(),
            transaction_audit()
        ]


class Audit(models.Model):
    table_name = models.CharField(max_length=255)
    operation = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)
    user_name = models.CharField(max_length=255)
    data = models.JSONField()

    class Meta:
        db_table = 'audit_table'
