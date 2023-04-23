from django.contrib.auth.models import AbstractUser
from django.db import models


class AdvUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name='Are you activated?')
    send_messages = models.BooleanField(default=True,
                                        verbose_name='Do you want to receive messages about new comments?')

    class Meta(AbstractUser.Meta):
        pass
