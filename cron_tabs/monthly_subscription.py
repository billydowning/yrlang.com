from datetime import datetime

from invoices.models import MonthlySubscriptionInvoice


def provider_monthly_subscription():
    try:
        invoice = MonthlySubscriptionInvoice.objects.filter(
            is_paid=False
        ).exclude(
            date_created__year = datetime.now().date().year,
            date_created__month = datetime.now().date().month,
        )
    except Exception as e:
        invoice = False
        print(e)
    if invoice:
        for obj in invoice:
            obj.current_month = False
            obj.save()
