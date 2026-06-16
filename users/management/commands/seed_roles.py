from django.core.management.base import BaseCommand

from users.models import Role, User


class Command(BaseCommand):

    help = "Seed default roles"

    def handle(self, *args, **kwargs):

        roles = [
            "Admin",
            "Manager",
            "Author",
            "Student"
        ]

        for role_name in roles:

            role, created = Role.objects.get_or_create(
                name=role_name
            )

            if created:

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created role: {role_name}"
                    )
                )

            else:

                self.stdout.write(
                    self.style.WARNING(
                        f"Role already exists: {role_name}"
                    )
                )

        try:
            admin_role, _ = Role.objects.get_or_create(
                name="Admin"
            )

            admin_user = User.objects.get(
                username="Admin"
            )

            admin_user.roles.add(
                admin_role
            )

            self.stdout.write(
                self.style.SUCCESS(
                    "Admin role assigned to admin user."
                )
            )

        except User.DoesNotExist:

            self.stdout.write(
                self.style.WARNING(
                    "User admin does not exist."
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Role seeding completed."
            )
        )