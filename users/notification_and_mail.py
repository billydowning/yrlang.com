from users.models import UserRole
from main.models import Notification

class NotificationToUser:

    def notifications_create_for_booking(self, instance, message_data):
        requestee_role = UserRole.objects.get(name=UserRole.CLIENT)
        requestor_role = UserRole.objects.get(name=UserRole.PROVIDER)
        Notification.objects.bulk_create([
            Notification(name='have booking', user=instance.requestee,
                         role=requestor_role, payload={'body': 'you have an booking with' + str(instance.requestor),
                                                       'url': str(instance.get_absolute_url())
                                                       }
                         ),
            Notification(name='booking created', user=instance.requestor,
                         role=requestee_role, payload={'body': message_data, "url": str(instance.get_absolute_url())
                                                       }),
        ])

    def notifications_create_for_appoitment(self, instance, message_data):
        requestee_role = UserRole.objects.get(name=UserRole.CLIENT)
        requestor_role = UserRole.objects.get(name=UserRole.PROVIDER)
        Notification.objects.bulk_create([
            Notification(name='have appointment', user=instance.requestee,
                         role=requestor_role, payload= {'body':'you have an appointment with'+str(instance.requestor),
                                                        'url':str(instance.get_absolute_url())
                                                        }
                         ),
            Notification(name='appointment created', user=instance.requestor,
                         role = requestee_role, payload={'body':message_data, "url":str(instance.get_absolute_url())
                                                                }),
        ])

    def notification_for_chat(self):
        pass

