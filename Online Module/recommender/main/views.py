from django.shortcuts import render, redirect
from .models import UserProfiles, User


# Create your views here.

def main(request):
    return render(request, "home.html", {"name": "Stranger"})


def profile(request):
    if request.method == 'POST':

        topics = request.POST["topics"]

        if UserProfiles.objects.filter(user=request.user).exists():
            print("user profile already exists")
            userProfile = UserProfiles.objects.filter(user=request.user).delete()

        userProfile = UserProfiles()

        userProfile.user = request.user
        userProfile.topics = topics
        userProfile.save()

        return redirect('profile')

    elif UserProfiles.objects.filter(user=request.user).exists():
        user_profile = UserProfiles.objects.get(user=request.user)
        topic = user_profile.topics
        return render(request, 'profile.html', {"topics": topic})

    else:
        topic = "<No Favourite Topics Added Yet>"
        return render(request, 'profile.html', {"topics": topic})
