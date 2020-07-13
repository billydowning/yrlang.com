from appointments.models import Appointment, ProviderAppointment
from main.models import Notification
import datetime
from webpush import send_user_notification

def appointment_reminder_before_24H():

    one_day_ago = datetime.date.today() + datetime.timedelta(days=1)
    appointmnet_res = Appointment.objects.filter(date_created__date=one_day_ago,
                                                 status=Appointment.CREATED)

    provider_appointmnet_res = ProviderAppointment.objects.filter(request_date=one_day_ago,
                                                                  status=ProviderAppointment.REQUESTED)

    if appointmnet_res:
        appointment_name = "YR-lang"
        payload_data = {
            "head": "Reminder !",
            "body": "your have an appoitment to visit Tommorow ",
                    "icon": "https://i0.wp.com/yr-lang.com/wp-content/uploads/2019/12/YRLANGBLACK.png?fit=583%2C596&ssl=1"
        }
        for data in appointmnet_res:
            Notification.objects.create(user=data.requestee,
                                        name=appointment_name, payload=payload_data)
            send_user_notification(user=data.requestee, payload=payload_data, ttl=100)

    if provider_appointmnet_res:
        appointment_name = "Appointment For Provider"
        payload_data = {
            "head": "YR-lang",
            "body":"your have an appoitment to visit Tommorow ",
            "icon": "https://i0.wp.com/yr-lang.com/wp-content/uploads/2019/12/YRLANGBLACK.png?fit=583%2C596&ssl=1"
        }
        for data in provider_appointmnet_res:
            Notification.objects.create(user=data.requestee,
                                        name=appointment_name, payload=payload_data)
            send_user_notification(user=data.requestee, payload=payload_data, ttl=100)
