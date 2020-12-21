from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout



# Create your views here.

from Budget.forms import RegistrationForm,LoginForm

def register(request):
    form=RegistrationForm()
    context={}
    context["form"]=form
    if request.method=='POST':
        form=RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request,"Budget/login.html")
    return render(request,"Budget/registration.html",context)


def signIn(request):
    form=LoginForm()
    context={}
    context["form"]=form
    if request.method=='POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get("username")
            password=form.cleaned_data.get("password")
            user=authenticate(request,username=username,password=password)
            if user:
                login(request,user)
                return render(request, "Budget/home.html", context)
            else:
                return render(request, "Budget/login.html", context)

    return render(request,"Budget/login.html",context)


def signOut(request):
    logout(request)
    return redirect("signin")

from django.contrib.auth.models import User
def editProfile(request):
    user=User.objects.get(username=request.user)
    form=RegistrationForm(instance=user)
    context={}
    context["form"]=form
    if request.method=="POST":
        form=RegistrationForm(instance=user,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("signin")
    else:
        form[context]=form
        return render(request, "Budget/editprofile.html", context)

    return render(request,"Budget/editprofile.html",context)


def userHome(request):
    return render(request,"Budget/home.html")

from Budget.forms import Expense
from Budget.forms import AddExpenseForm
def addExpense(request):
    form=AddExpenseForm(initial={"user":request.user})
    context={}
    context["form"]=form
    expense=Expense.objects.filter(user=request.user)
    context["expense"]=expense
    if request.method=="POST":
        form=AddExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("addexpense")
    return render(request,"Budget/addexpense.html",context)
