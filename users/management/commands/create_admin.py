from users.models import User
from carts.models import Cart
from addresses.models import Address
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.hashers import make_password


class Command(BaseCommand):
    help = "Creation of basic admin superuser"

    def add_arguments(self, parser):
        parser.add_argument("--username", type=str, help="Defina um username")
        parser.add_argument("--password", type=str, help="Defina um password")
        parser.add_argument("--email", type=str, help="Defina um email")

    def handle(self, *args, **kwargs):
        username = kwargs.get("username") or "admin"
        password = kwargs.get("password") or "123admin321"
        email = kwargs.get("email") or "admin@nomail.com"

        check_user = User.objects.filter(username=username)
        check_mail = User.objects.filter(email=email)
        if check_user:
            raise CommandError(f"Username `{username}` already taken.")
        elif check_mail:
            raise CommandError(f"Email `{email}` already taken.")
        else:
            admin_cart = Cart.objects.create()
            admin_address = Address.objects.create(
                street="Not informed",
                number=0,
                detail="Not informed",
                zip_code=0,
                city="Not informed",
                state="NO",
                country="Not informed",
            )
            new_admin = User.objects.create_superuser(
                username=username,
                password=password,
                email=email,
                address=admin_address,
                cart=admin_cart,
                first_name="System",
                last_name="Operator",
                is_vendor=True,
            )

            self.stdout.write(
                self.style.SUCCESS(f"Admin `{username}` successfully created!")
            )
