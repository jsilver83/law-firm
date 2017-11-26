from django.contrib import admin
from reversion.admin import VersionAdmin
from django.utils.translation import ugettext_lazy as _
from .models import *


class FundRequestAdmin(VersionAdmin):
    list_display = ('justification', 'approved_amount', 'requester', 'request_date')


class TransactionAdmin(VersionAdmin):
    list_display = ('title', 'project', 'amount', 'type')


admin.site.register(FundRequest, FundRequestAdmin)
admin.site.register(Transaction, TransactionAdmin)
