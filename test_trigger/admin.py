from django.contrib import admin
from .models import *

# # Register your models here.
# class TimeStampModelAdmin(admin.ModelAdmin):
#     # Define fields to be displayed in the admin panel
#     list_display = ('created_at', 'editable_value')
#
#     # Make the created_at field read-only in the admin panel
#     readonly_fields = ('created_at',)
#
# # Register the model with the custom admin options
# admin.site.register(TimeStampModel, TimeStampModelAdmin)
#
admin.site.register(MyModel)
admin.site.register(ProtectedModel)
admin.site.register(Versioned)
admin.site.register(Post)
admin.site.register(TimeStampModel)
admin.site.register(SoftDelete)
admin.site.register(RedundantUpdateModel)
admin.site.register(HistoryModel)
admin.site.register(TrackedModel)
admin.site.register(UpdateCheck)
admin.site.register(AppendOnlyModel)
admin.site.register(Product)
admin.site.register(Transaction)
admin.site.register(Audit)
