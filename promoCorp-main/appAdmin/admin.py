from django.contrib import admin

from appAdmin.models import Account, ClientContract, ClientGroup,MaterialInvoice, MaterialInvoiceItems

# Registering models with the admin site
admin.site.register(ClientGroup)
admin.site.register(ClientContract)
admin.site.register(Account)

class MaterialInvoiceItemsInline(admin.TabularInline):
    model = MaterialInvoiceItems
    extra = 1

class MaterialInvoiceAdmin(admin.ModelAdmin):
    inlines = [MaterialInvoiceItemsInline]

admin.site.register(MaterialInvoice, MaterialInvoiceAdmin)