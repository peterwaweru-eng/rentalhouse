from django.contrib import admin
from .models import UserProfileInfo, Houses

# Register the UserProfileInfo model
class UserProfileInfoAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone')
    search_fields = ('user__username', 'phone')

admin.site.register(UserProfileInfo, UserProfileInfoAdmin)


class HousesAdmin(admin.ModelAdmin):
    list_display = (
        'house_name', 'address', 'house_no_bedrooms', 'house_no_bathrooms',
        'house_price', 'house_owner_name'
    )
    search_fields = ('house_name', 'address', 'house_owner_name')
    list_filter = ('house_no_bedrooms', 'house_no_bathrooms', 'house_price')

admin.site.register(Houses, HousesAdmin)
