
from django.utils import timezone

from django.contrib.auth.signals import (
    user_logged_in,
    user_logged_out
)

from django.dispatch import receiver

from users.models import (
    LoginLog,
    UserProfile
)

def get_client_ip(request):

    forwarded = request.META.get(
        "HTTP_X_FORWARDED_FOR"
    )

    if forwarded:

        return forwarded.split(",")[0]

    return request.META.get(
        "REMOTE_ADDR",
        ""
    )


@receiver(user_logged_in)
def create_login_log(
    sender,
    request,
    user,
    **kwargs
):

    fullname = ""

    profile = UserProfile.objects.filter(
        user=user
    ).first()

    if profile:

        fullname = profile.fullname or ""

    LoginLog.objects.create(

        username=user.username,

        fullname=fullname,

        login_time=timezone.now(),

        ip_address=get_client_ip(
            request
        ),

        user_agent=request.META.get(
            "HTTP_USER_AGENT",
            ""
        ),

        session_key=request.session.session_key or ""

    )

@receiver(user_logged_out)
def update_logout_time(
    sender,
    request,
    user,
    **kwargs
):

    if not request:
        return

    session_key = (
        request.session.session_key
    )

    if not session_key:
        return

    log = LoginLog.objects.filter(

        session_key=session_key,

        logout_time__isnull=True

    ).first()

    if not log:
        return

    log.logout_time = timezone.now()

    log.save(
        update_fields=[
            "logout_time"
        ]
    )