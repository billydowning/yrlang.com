from django.contrib.auth.models import Group, Permission


# group is not exists create a new group if and add permissions to group
# if group is exists add user to group
def group_obj(user):
    professionals, created = Group.objects.get_or_create(name='Professionals')
    if created:
        permissions = ['change_customuser']
        permissions_obj = []

        for permission in permissions:
            permissions_obj.append(Permission.objects.get(codename=permission))

        professionals.permissions.set(permissions_obj)
        user.groups.add(professionals)
        return True
    else:
        user.groups.add(professionals)
        return True
