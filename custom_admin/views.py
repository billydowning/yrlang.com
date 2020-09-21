from django.views import generic
from invoices.models import Invoice
from rooms.models import Room, Message
from main.models import ReportAProblem
from users.models import UserRole
from django.shortcuts import HttpResponseRedirect, redirect, reverse, get_object_or_404
from django.contrib import messages
# Create your views here.


class InvoiceListView(generic.ListView):
    model = Invoice
    template_name = 'custom_admin/invoices.html'
    context_object_name = 'invoices'

    def get_queryset(self):
        return Invoice.objects.all().order_by('-id')


class InvoiceDetailView(generic.DetailView):
    model = Invoice
    template_name = 'custom_admin/invoices_detail.html'
    context_object_name = 'invoice'

    def get_context_data(self, **kwargs):
        context = super(InvoiceDetailView, self).get_context_data()
        try:
            room = Room.objects.get(
                creator=self.get_object().payor,
                partner=self.get_object().payee
            )
        except Exception as e:
            room = None
            print(e)
        if room:
            try:
                context['message'] = Message.objects.filter(room=room).order_by('date_created')
            except Exception as e:
                context['message'] = None
                print(e)
        return context


class UserComplainListView(generic.ListView):
    template_name = 'complains/complian_list.html'
    model = ReportAProblem
    context_object_name = 'complains'

    def get_queryset(self):
        return self.model.objects.order_by('-date_posted')

class UserComplainDetailView(generic.DetailView):
    template_name = 'complains/complain_detail.html'
    model =  ReportAProblem
    context_object_name = 'complain'

    def get_context_data(self, **kwargs):
        context = super(UserComplainDetailView, self).get_context_data(**kwargs)
        room = Room.objects.filter(creator_id=self.get_object().reporter, partner_id=self.get_object().reportee,
                            created_for__name = UserRole.CLIENT
                            ).first()
        context['room'] = room
        return context





class MakeComplainSolveView(generic.RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'custom_admin:complain_detail'


    def get_redirect_url(self, *args, **kwargs):
        report_obj = get_object_or_404(ReportAProblem, pk=self.kwargs.get('pk'))
        report_obj.problem_status = ReportAProblem.SOLEVE
        report_obj.save()
        return super(MakeComplainSolveView, self).get_redirect_url(*args, **kwargs)



