from django.contrib.auth.views import redirect_to_login
from google.cloud import language_v1
from google.oauth2 import service_account
from django.http import  HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.conf import settings
import os
from .models import Houses

# View to create a house

def advt_form(request):
    if request.method == "POST":

        house_no_bedrooms = request.POST.get("house_no_bedrooms")
        house_no_bathrooms = request.POST.get("house_no_bathrooms")
        house_carpet_area = request.POST.get("house_carpet_area") or 0.000
        # house_buildup_area = request.POST.get("house_buildup_area") or 0.000
        house_furnishing = request.POST.get("house_furnishing")
        house_floor_no = request.POST.get("house_floor_no")
        house_price = request.POST.get("house_price") or 0.00
        house_description = request.POST.get("house_description")
        apartment_range = request.POST.get('property_range')



        img7 = request.FILES.get('img7')
        img8 = request.FILES.get('img8')
        img9 = request.FILES.get('img9')


        house_owner_mail = request.POST.get("house_owner_email")
        house_owner_number = request.POST.get("house_owner_number")
        house_owner_name = request.POST.get("house_owner_name")

        house_data = Houses(
            house_no_bedrooms=house_no_bedrooms,
            house_no_bathrooms=house_no_bathrooms,
            house_carpet_area=house_carpet_area,
            # house_buildup_area=house_buildup_area,
            house_furnishing=house_furnishing,
            house_floor_no=house_floor_no,
            house_price=house_price,
            house_description=house_description,
            images1=img7,
            images2=img8,
            images3=img9,
            house_owner_mail=house_owner_mail,
            house_owner_name=house_owner_name,
            house_owner_number=house_owner_number
        )


        house_data.save()

        # Return the appropriate view after form submission
        return render( request,'show_house.html')  # Redirect to a success page
    else:
        return render(request, 'advt_form.html')  # Return the form page for GET request

def view_houses(request):
    house_data=show_house.objects.all()
    return render(request,'show_house.html',{'house_data':house_data})


def rating_analysis(request):
    if request.method == 'POST':
        p_type = request.POST.get('p_type')
        property_id = request.POST.get('property_id')
        comment = request.POST.get('comment')

        if not comment:
            return HttpResponse("<h2>Comment cannot be empty!</h2>", status=400)

        credentials_path = os.path.join(settings.BASE_DIR, 'static/peppy-answer-443612-d6-449c859256f4.json')
        try:
            credentials = service_account.Credentials.from_service_account_file(credentials_path)
            client = language_v1.LanguageServiceClient(credentials=credentials)
            document = language_v1.Document(
                content=comment,
                type=language_v1.Document.Type.PLAIN_TEXT
            )

            response = client.analyze_sentiment(request={'document': document})
            sentiment = response.document_sentiment
            x = sentiment.score

            # Scale sentiment score to a rating
            a, b, c, d = -1.0, 1.0, 1, 5
            result = (((d - c) * (x - a)) / (b - a)) + c
            final_rating = round(result, 1)

        except Exception as e:
            return HttpResponse(f"<h2>Google Cloud API Error: {e}</h2>", status=500)

        # Update rating
        if p_type == "Houses":
            data_obj = get_object_or_404(Houses, id=property_id)

            rating = data_obj.rating
            comments_count = data_obj.comments_count or 0
            total = rating * comments_count

            new_rating = round((final_rating + total) / (comments_count + 1), 1) if comments_count > 0 else final_rating
            new_rating = max(1.0, min(5.0, new_rating))

            data_obj.rating = new_rating
            data_obj.comments_count += 1
            data_obj.save()

            return render(request, 'redirect.html', {'p_type': p_type, 'property_id': property_id})

        return HttpResponseRedirect(reverse('show_houses', args=[p_type, property_id]))


#
# def advt_form(request):
#     return render(request,'advt_form.html')


def show_house(request):
    return render(request,'show_house.html')

from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserForm
from django.http import HttpResponse

# User registration view
def register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            return redirect('user_login')
        else:
            return render(request, 'advt_form.html', {'user_form': user_form})
    else:
        user_form = UserForm()
    return render(request, 'register.html', {'user_form': user_form})
# User login view
def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        p_type = request.POST.get('p_type')
        property_id = request.POST.get('property_id')

        # Authenticate the user
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if not property_id:
                return HttpResponse("<h2>Login successful</h2>")
            return render(request, 'please_wait.html', {'p_type': p_type, 'property_id': property_id})
        else:
            # print(f"Login failed for Username: {username} and Password: {password}")
            check = "fail"
            return render(request, 'login_successfully.html', {'check': check})

    return render(request, 'register.html')

# User logout view
def user_logout(request):
    logout(request)
    return redirect('register')

# Special view for logged-in users
@login_required
def special(request):
    return redirect_to_login(request,'register')

    # return render(request,'copy_advt_form.html')


def index(request):
    return render(request,'index.html')


def copy_advt_form(request):
    return render(request,'copy_advt_form.html')


