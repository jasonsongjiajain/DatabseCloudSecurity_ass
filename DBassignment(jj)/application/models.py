from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class user_detail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phoneno = models.CharField(max_length=12, unique=True)

    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "User Detail"

    def str(self):
        return self.user.username
    
class paymentmethod_detail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cardtype = models.CharField(max_length=50)
    CVV = models.CharField(max_length=50)
    cardnumber = models.CharField(max_length=50)
    expiryyear = models.CharField(max_length=50)
    expirymonth = models.CharField(max_length=50)
    cardholdername = models.CharField(max_length=50)


    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Payment Detail"

    def str(self):
        return self.user.username
    
class Plan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.CharField(max_length=100)
    amount = models.CharField(max_length=100)

    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Plan"
    def __str__(self):
        return self.user.username