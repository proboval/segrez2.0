from django.contrib.auth.models import AbstractBaseUser
from django.db import models


class Company(AbstractBaseUser):
    companyName = models.CharField(
        max_length=50,
    )
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['companyName']

    def __str__(self):
        return f'{self.companyName} ({self.email})'


class Expert(AbstractBaseUser):
    Name = models.CharField(
        max_length=25
    )
    lastName = models.CharField(
        max_length=25
    )
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    company = models.ForeignKey('Company',
                                on_delete=models.CASCADE,
                                related_name='experts',
                                null=True,
                                )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['Name', 'lastName']

    def __str__(self):
        return f'{self.Name} {self.lastName} ({self.email})'
