from django.core.management.base import BaseCommand, CommandError

from users.models import CustomUser, UserRole


class Command(BaseCommand):
    help = 'Add User Role To User'

    def handle(self, *args, **options):
        self.stdout.write('Assigning User Role...')
        try:
            users = CustomUser.objects.filter(is_superuser=False)
        except:
            raise CommandError('Somethin is Wrong')
        for user in users:
            if len(user.user_role.all()) == 0:
                if user.is_client:
                    user.user_role.add(UserRole.objects.get(name=UserRole.CLIENT))
                else:
                    user.user_role.add(UserRole.objects.get(name=UserRole.PROVIDER))
            
        self.stdout.write('Assigning User Role Is Done...!')
