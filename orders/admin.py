import csv
import datetime
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
	model = OrderItem
	raw_id_fields = ['product']


def export_to_csv(modeladmin, request, queryset):
	opts = modeladmin.model._meta
	response = HttpResponse(content_tupe='text/csv')
	response['Content-Dispostion'] = 'attachment; filename={}.csv'.format(opts.verbose_name)
	writer = csv.writer(response)

	fields = [fiel for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
	# write a first row with header information
	writer.writerow([field.verbose_name for field in fields])
	# write data rows
	for obj in queryset:
		data_row = []
		for field in fields:
			value = getattr(obj, field.name)
			if isinstance(value, datetime.datetime):
				value = value.strftime('%d/%m/%Y')
			data_row.append(value)
		writer.writerow(data_row)
	return response
export_to_csv.short_description = 'Export to csv'

def order_detail(obj):
	return '<a href="{}">View</a>'.format(reverse('orders:admin_order_detail', args=[obj.id]))
order_detail.allow_tags = True

class OrderAdmin(admin.ModelAdmin):
	list_display = ['id', 'first_name', 'last_name', 'email', 'address', 'postal_code', 'city', 'paid', 'created', 'updated', order_detail]
	list_filter = ['paid', 'created', 'updated']
	inlines = [OrderItemInline]
	actions = [export_to_csv]


admin.site.register(Order, OrderAdmin)