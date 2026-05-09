from users.models import User

users = User.objects.all()
for user in users:
    print(user)