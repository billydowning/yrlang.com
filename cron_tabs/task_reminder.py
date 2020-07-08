from appointments.models import Appointment, ProviderAppointment
from main.models import Notification
import datetime
from users.models import CustomUser

def appointment_reminder_before_24H():

    one_day_ago = datetime.date.today() + datetime.timedelta(days=1)
    appointmnet_res = Appointment.objects.filter(date_created__date=one_day_ago,
                                                 status=Appointment.CREATED)

    provider_appointmnet_res = ProviderAppointment.objects.filter(request_date=one_day_ago,
                                                                  status=ProviderAppointment.REQUESTED)

    if appointmnet_res:
        appointment_name = "Appointment For Localite"
        payload_data = {
            "reason": 'your have a appoitment to visit Tommorow '
        }
        for data in appointmnet_res:
            Notification.objects.create(user=data.requestee,
                                        name=appointment_name, payload=payload_data)

    if provider_appointmnet_res:
        appointment_name = "Appointment For Provider"
        payload_data = {
            "reason": 'your have a appoitment to visit Tommorow '
        }
        for data in provider_appointmnet_res:
            Notification.objects.create(user=data.requestee,
                                        name=appointment_name, payload=payload_data)
