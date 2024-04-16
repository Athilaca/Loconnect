from django.db import models

# Create your models here.
class UserProfile(models.Model):
    phone_number=models.CharField(max_length=15)
    otp = models.CharField(max_length=6, null=True, blank=True)


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Service(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.CharField(max_length=50, help_text="Estimated duration of the service")
    location = models.CharField(max_length=100, help_text="Location where the service is provided")
    provider = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='services', help_text="Service provider")
    
    
    def __str__(self):
        return self.name

class ServiceImage(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='services/', help_text="Image related to the service", blank=True, null=True)

    def __str__(self):
        return self.image.name


class Appointment(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='appointments')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='appointments', help_text="User who booked the service")
    date_time = models.DateTimeField(help_text="Date and time of the appointment")
    notes = models.TextField(blank=True, help_text="Any additional notes for the appointment")

   