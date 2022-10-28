from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
# Create your views here.

def login_request(request):


    if request.user.is_authenticated:
        return redirect("/products")


    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request , user)
            nextUrl = request.GET.get('next', None)

            if nextUrl is None:
                return redirect('products')

            else:
                return redirect(nextUrl)
        else:
            return render(request, "account/login.html" , {
                "error": "Kullanıcı adı veya parola yanlış"
            })

    else:
        return render(request, "account/login.html")

def register_request(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        repassword = request.POST["repassword"]
        email = request.POST["email"]

        if password == repassword:

            if User.objects.filter(username = username).exists():
                return render(request , "account/register.html" , {
                "error": "Bu kullanıcı adı zaten var."
            })

            else:
                if User.objects.filter(email=email).exists():
                    return render(request , "account/register.html" , {
                    "error": "Bu email zaten var."
                })

                else:
                    user = User.objects.create_user(username=username,email=email,password=password)
                    user.save()
                    return redirect("/login")



        
        else:
            return render(request , "account/register.html" , {
                "error": "Parolalar eşleşmiyor"
            })


    else:
        return render(request, "account/register.html")

def logout_request(request):
    logout(request)
    return redirect("products")