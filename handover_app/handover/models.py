from django.db import models
from accounts.models import User
from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings
import uuid
import os
import environ


env = environ.Env(DEBUG=(bool, False),)
environ.Env.read_env(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))


def handover_directory_path(instance, filename):
    prefix = 'media/handover/'
    name = str(uuid.uuid4())
    extension = os.path.splitext(filename)[-1]
    return prefix + name + extension


class Tag(models.Model):
    tag_no = models.BigAutoField(
        verbose_name='Tag_No.',
        primary_key=True,
        unique=True
    )
    tag = models.CharField(max_length=256)

    def __str__(self):
        return self.tag

    class Meta:
        verbose_name = verbose_name_plural = "タグ"


class Handover(models.Model):
    handover_no = models.BigAutoField(
        verbose_name='Handover_No.',
        primary_key=True,
        unique=True
    )
    handover = models.TextField(verbose_name='引継ぎ')
    created_at = models.DateTimeField()
    user_name = models.CharField(max_length=256)
    user_ID = models.PositiveIntegerField()
    tag = models.ManyToManyField(
        Tag,
        verbose_name='タグ',
        through='HandoverTagRelation'
    )

    def __str__(self):
        return self.handover_no

    def get_user_image(self):
        get = User.objects.get(pk=self.user_ID)
        return get.user_image

    class Meta:
        verbose_name = verbose_name_plural = "引継ぎ"


class HandoverImage(models.Model):
    handover_image_no = models.BigAutoField(
        verbose_name='No.',
        primary_key=True,
        unique=True
    )
    handover = models.ForeignKey(
        Handover,
        on_delete=models.CASCADE
    )
    if settings.DEBUG:
        image = models.ImageField(
            upload_to=handover_directory_path,
            blank=True,
            null=True,
        )
    else:
        image = models.ImageField(
            upload_to=handover_directory_path,
            blank=True,
            null=True,
            storage=S3Boto3Storage(bucket_name=env('AWS_INPUT_BUCKET_NAME')),
        )


class HandoverTagRelation(models.Model):
    handover_tag_no = models.BigAutoField(
        verbose_name='No.',
        primary_key=True,
        unique=True
    )
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    handover_tag = models.ForeignKey(
        Handover,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = verbose_name_plural = "引継ぎタグ関連"


class Comment(models.Model):
    comment_no = models.BigAutoField(
        verbose_name='Comment_No.',
        primary_key=True,
        unique=True
    )
    comments = models.TextField()
    handover = models.ForeignKey(
        Handover,
        on_delete=models.CASCADE
    )
    parent = models.ForeignKey(
        'self',
        verbose_name='親コメント',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    user_name = models.CharField(max_length=256)
    User_ID = models.PositiveIntegerField()
    created_at = models.DateTimeField()

    def __str__(self):
        return self.comment_no

    def get_user_image(self):
        get = User.objects.get(pk=self.User_ID)
        return get.user_image

    class Meta:
        verbose_name = verbose_name_plural = "コメント"




