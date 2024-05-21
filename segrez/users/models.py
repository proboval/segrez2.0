from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from segmentation.models import Project


class CompanyManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        company = self.model(email=email, name=name, **extra_fields)
        company.set_password(password)
        company.save(using=self._db)
        return company


class Company(AbstractBaseUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    secretcode = models.CharField(max_length=4, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CompanyManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name


class ExpertManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class Expert(AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, blank=True, null=True, related_name='experts')
    secretcode = models.CharField(max_length=4, null=True)
    projects = models.ManyToManyField(Project)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = ExpertManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.pk})'
