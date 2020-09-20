from datetime import datetime

from payment.models import MonthlyProviderAppointmentCount

def provider_monthly_subscription():
    print('Stert\n\n')
    print(datetime.now().date().year)
    print(datetime.now().date().month)
    count = MonthlyProviderAppointmentCount.objects.filter(
        date__year=datetime.now().date().year,
        date__month=datetime.now().date().month
    )
    print(count)
    print('End')
