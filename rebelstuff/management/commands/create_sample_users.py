from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                'admin', 'admin@example.com', 'password'
            )

        for name in ['stuffer', 'booker']:
            if not User.objects.filter(username=name).exists():
                user = User.objects.create(
                    username=name, email=name + '@example.com', is_staff=True
                )
                user.set_password('password')
                user.groups.set(Group.objects.filter(name=name))
                user.save()
