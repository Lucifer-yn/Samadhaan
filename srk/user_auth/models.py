from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=255,unique=False)
    email = models.EmailField(unique=False)

    def __str__(self):
        return self.username

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class ReportIssue(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Associate with logged-in user
    full_name = models.CharField(max_length=255)
    contact_no = models.CharField(max_length=15)
    address = models.TextField()
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    reported_location = models.CharField(max_length=255)
    field_of_report = models.CharField(max_length=255, choices=[
        ('transport', 'Transport service & functionality'),
        ('electricity', 'Electric supply & outages'),
        ('water', 'Water system overflow'),
        ('road', 'Road Construction & maintenance'),
        ('infrastructure', 'Infrastructure & development'),
    ])
    location_image = models.ImageField(upload_to='report_images/', blank=True, null=True)
    latitude = models.DecimalField(max_digits=30, decimal_places=15, blank=True, null=True)
    longitude = models.DecimalField(max_digits=30, decimal_places=15, blank=True, null=True)
    description = models.TextField()
    issue_description = models.TextField()  
    submitted_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name



from django.contrib.auth.models import BaseUserManager,AbstractBaseUser


class AdminManager(BaseUserManager):
    def create_admin(self, full_name, application_id, email, post, posted_area, password=None):
        if not email:
            raise ValueError("Admins must have an email address")

        admin = self.model(
            full_name=full_name,
            application_id=application_id,
            email=self.normalize_email(email),
            post=post,
            posted_area=posted_area
        )

        if password:
            admin.set_password(password) 

        admin.save(using=self._db)
        return admin

class Admin(AbstractBaseUser): 
    full_name = models.CharField(max_length=255)
    application_id = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=False)
    post = models.CharField(max_length=255)
    posted_area = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.jpg')
    objects = AdminManager()  

    USERNAME_FIELD = 'email'  
    REQUIRED_FIELDS = ['full_name', 'application_id', 'post', 'posted_area']

    def __str__(self):
        return self.full_name


class ProjectDetail(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]
    location = models.CharField(max_length=255)
    work = models.CharField(max_length=255)
    start_date = models.DateField(null=True, blank=True)  # Allow NULL values
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    completion_date = models.DateField(null=True, blank=True)
    fund_granted = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    estimate_file = models.FileField(upload_to='estimates/', null=True, blank=True)
    site_image = models.ImageField(upload_to='site_images/', null=True, blank=True)


    # location = models.CharField(max_length=255)
    # work = models.CharField(max_length=255)
    # start_date = models.DateField(null=True, blank=True) 
    # completion_date = models.DateField(null=True, blank=True)
    # fund_granted = models.DecimalField(max_digits=10, decimal_places=2)
    # estimate_file = models.FileField(upload_to='estimates/')
    # site_image = models.ImageField(upload_to='site_images/')

    def __str__(self):
        return f"{self.work} - {self.location}"
