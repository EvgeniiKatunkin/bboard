from django.db import models
from django.contrib.auth.models import AbstractUser


class AdvUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name='Are you activated?')
    send_messages = models.BooleanField(default=True,
                                        verbose_name='Do you want to receive messages about new comments?')

    class Meta(AbstractUser.Meta):
        pass
