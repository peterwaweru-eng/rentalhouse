from PIL.EpsImagePlugin import field
from django.contrib.auth.models import User
from django.db import models

class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=13)

    def __str__(self):
        return f"{self.user.username}"

# House model to store house-related data
class Houses(models.Model):
    location = models.CharField(max_length=100)
    address = models.CharField(max_length=100,default='')
    house_name = models.CharField(max_length=100, default='')
    house_furnishing=models.CharField(max_length=50,default='')
    house_carpet_area=models.DecimalField(max_digits=5,decimal_places=3,default=0.000)
    house_no_bedrooms = models.IntegerField(default=0)
    house_no_bathrooms = models.IntegerField(default=0)
    # house_buildup_area = models.DecimalField(max_digits=5,decimal_places=3,default=0.000,null=False)
    house_overlooking = models.CharField(max_length=30)
    house_floor_no = models.IntegerField(default=0)
    house_owner_name = models.CharField(max_length=100, default='')
    house_owner_number = models.CharField(max_length=15, default='')
    house_owner_mail = models.EmailField(max_length=100, default='')
    house_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    house_description = models.CharField(max_length=300,default='')
    images1 = models.ImageField(upload_to="images", default='')
    images2 = models.ImageField(upload_to="images", default='')
    images3 = models.ImageField(upload_to="images", default='')
    rating = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    comments_count = models.IntegerField(default=0)

    def __str__(self):
        return self.house_name or "Unnamed House"
