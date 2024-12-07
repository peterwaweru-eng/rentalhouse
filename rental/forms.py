from django import forms
from django.contrib.auth.models import User
from .models import Houses, UserProfileInfo
from django.contrib import admin

# User registration form
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    phone = forms.CharField(max_length=13, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password','phone']

    def save(self, commit=True):
        # Save User instance first
        user = super().save(commit=False)
        if commit:
            user.set_password(user.password)
            user.save()

        user_profile = UserProfileInfo.objects.create(user=user, phone=self.cleaned_data['phone'])
        return user_profile


# HousesForm for creating or updating house information
class HousesForm(forms.ModelForm):

    class Meta:
        model = Houses
        fields = [
            'house_name', 'address', 'house_no_bedrooms', 'house_no_bathrooms',
             'house_overlooking', 'house_floor_no',
            'house_owner_name', 'house_owner_number', 'house_owner_mail',
            'house_price', 'house_description', 'images1', 'images2', 'images3'
        ]

    def save(self, commit=True):
        # Save house object correctly
        house = super().save(commit=False)

        if commit:
            house.save()

        return house


# HousesAdmin for managing houses in the admin panel
class HousesAdmin(admin.ModelAdmin):
    list_display = (
        'location', 'address', 'house_no_bedrooms', 'house_no_bathrooms',
        'house_overlooking', 'house_floor_no',
        'house_price', 'house_description', 'house_owner_name',
        'house_owner_number', 'house_owner_mail', 'images1', 'images2', 'images3',
        'rating', 'comments_count'
    )
    search_fields = ('house_owner_name', 'address', 'location')
    list_filter = ('location', 'house_price')
