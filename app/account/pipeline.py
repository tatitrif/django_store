from django.contrib.auth.models import Group


def new_users_handler(backend, user, response, *args, **kwargs):
    group = Group.objects.filter(name="social")
    if not len(group):
        Group.objects.create(name="social")
    user.groups.add(group[0])
