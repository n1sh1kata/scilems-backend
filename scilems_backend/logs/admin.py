from django.contrib import admin
from .models import TransactionLog

@admin.register(TransactionLog)
class TransactionLogAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'user', 'log_type', 'previous_status', 
                   'new_status', 'timestamp')
    list_filter = ('log_type', 'previous_status', 'new_status')
    search_fields = ('transaction_id', 'user__username', 'message')
    readonly_fields = ('timestamp',)