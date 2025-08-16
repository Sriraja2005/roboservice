from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Reset admin user password'

    def handle(self, *args, **options):
        username = 'admin'
        new_password = 'admin123'
        
        try:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully reset password for user "{username}"!\n'
                    f'New password: {new_password}'
                )
            )
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'User "{username}" does not exist!')
            ) 