from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Unik related_name untuk menghindari bentrokan
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # Unik related_name untuk menghindari bentrokan
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

class MemberProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    height = models.DecimalField(max_digits=5, decimal_places=2)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    medical_history = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.full_name
