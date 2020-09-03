from django.views.generic import DetailView, ListView

from invoices.models import Invoice
from rooms.models import Room

# Create your views here.


class InvoiceListView(ListView):
    model = Invoice
    template_name = 'custom_admin/invoices.html'
    context_object_name = 'invoices'

    def get_queryset(self):
        return Invoice.objects.all().order_by('-id')


class InvoiceDetailView(DetailView):
    model = Invoice
    template_name = 'custom_admin/invoices_detail.html'
    context_object_name = 'invoice'

    def get_context_data(self, **kwargs):
        context = super(InvoiceDetailView, self).get_context_data()
        context['rooms'] = Room.objects.filter(
            creator=self.get_object().payor,
            partner=self.get_object().payee
        ).order_by('date_created')
        return context
