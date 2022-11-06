from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # let's assume that the email is already verified
    # of course in production it must be assured!
    email_verified = models.BooleanField(default=True)
