from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.base_user import BaseUserManager
from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings
import uuid
import os
import environ


env = environ.Env(DEBUG=(bool, False),)
environ.Env.read_env(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))


def avatar_directory_path(instance, filename):
    prefix = 'media/avatar/'
    name = str(uuid.uuid4())
    extension = os.path.splitext(filename)[-1]
    return prefix + name + extension


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, user_ID, password, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        username = self.model.normalize_username(username)
        user = self.model(username=username, user_ID=user_ID, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, user_ID=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(user_ID, username, password, **extra_fields)

    def create_superuser(self, username, user_ID, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_employee=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, user_ID, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.
    Username and password are required. Other fields are optional.
    """
    username_validator = UnicodeUsernameValidator()
    user_ID = models.PositiveIntegerField(_('ID'), primary_key=True, blank=True, unique=True)
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_(
            'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=100, blank=True)
    last_name = models.CharField(_('last name'), max_length=100, blank=True)
    if settings.DEBUG:
        user_image = models.ImageField(
            upload_to=avatar_directory_path,
            blank=True,
            null=True
        )
    else:
        user_image = models.ImageField(
            upload_to=avatar_directory_path,
            blank=True,
            null=True,
            storage=S3Boto3Storage(bucket_name=env('AWS_INPUT_BUCKET_NAME'))
        )
    email = models.EmailField(_('email address'), blank=True)
    is_staff = models.BooleanField(
        _('ユーザー'),
        default=False,
        help_text=_(
            '引継ぎを投稿できる権限'
        ),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'このユーザーをアクティブとして扱うかどうかを指定する '
            'アカウントを削除する代わりに、この選択を解除する'
        ),
    )

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['user_ID']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.last_name, self.first_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
