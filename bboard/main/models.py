from django.contrib.auth.models import AbstractUser
from django.db import models

from .utilities import get_timestamp_path


class AdvUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name='Are you activated?')
    send_messages = models.BooleanField(default=True,
                                        verbose_name='Do you want to receive messages about new comments?')

    def delete(self, *args, **kwargs):
        for bb in self.bb_set.all():
            bb.delete()
        super().delete(*args, **kwargs)

    class Meta(AbstractUser.Meta):
        pass


class Rubric(models.Model):
    name = models.CharField(max_length=20, db_index=True, unique=True, verbose_name='Title')
    order = models.SmallIntegerField(default=0, db_index=True, verbose_name='Order')
    super_rubric = models.ForeignKey('SuperRubric', on_delete=models.PROTECT, null=True, blank=True,
                                     verbose_name='super_rubric')


class SuperRubricManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_rubric__isnull=True)


class SuperRubric(Rubric):
    objects = SuperRubricManager()

    def __str__(self):
        return self.name

    class Meta:
        proxy = True
        ordering = ('order', 'name')
        verbose_name = 'Super_rubric'
        verbose_name_plural = 'Super_rubrics'


class SubrubricManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_rubric__isnull=False)


class SubRubric(Rubric):
    objects = SubrubricManager()

    def __str__(self):
        return '%s - %s' % (self.super_rubric.name, self.name)

    class Meta:
        proxy = True
        ordering = ('super_rubric__order', 'super_rubric__name', 'order', 'name')
        verbose_name = 'Sub_rubric'
        verbose_name_plural = 'Sub_rubrics'


class Bb(models.Model):
    rubric = models.ForeignKey(SubRubric, on_delete=models.PROTECT, verbose_name='Rubric')
    title = models.CharField(max_length=40, verbose_name='Product')
    content = models.TextField(verbose_name='Description')
    price = models.FloatField(default=0, verbose_name='Price')
    contacts = models.TextField(verbose_name='Contacts')
    image = models.ImageField(blank=True, upload_to=get_timestamp_path, verbose_name='Image')
    author = models.ForeignKey(AdvUser, on_delete=models.CASCADE, verbose_name='Author')
    is_active = models.BooleanField(default=True, db_index=True, verbose_name='Show in the list?')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Published')

    def delete(self, *args, **kwargs):
        for ai in self.additionalimage_set.all():
            ai.delete()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Bulletins'
        verbose_name = 'Bulletin'
        ordering = ['-created_at']


class AdditionalImage(models.Model):
    bb = models.ForeignKey(Bb, on_delete=models.CASCADE, verbose_name='Bulletin')
    image = models.ImageField(upload_to=get_timestamp_path, verbose_name='Image')

    class Meta:
        verbose_name_plural = 'Additional images'
        verbose_name = 'Additional image'


class Comment(models.Model):
    bb = models.ForeignKey(Bb, on_delete=models.CASCADE, verbose_name='Bulletin')
    author = models.CharField(max_length=30, verbose_name='Author')
    content = models.TextField(verbose_name='content')
    is_active = models.BooleanField(default=True, db_index=True, verbose_name='Show on screen?')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Published')

    class Meta:
        verbose_name_plural = 'Comments'
        verbose_name = 'Comment'
        ordering = ['created_at']
