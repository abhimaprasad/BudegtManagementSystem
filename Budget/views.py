from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from Budget.forms import Expense
from Budget.forms import AddExpenseForm
from django.db.models import Sum,Aggregate
from django.contrib.auth.decorators import login_required


# Create your views here.

from Budget.forms import RegistrationForm,LoginForm,ReviewExpenseForm

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
@login_required()
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

@login_required()
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

@login_required()
def editExpense(request,pk):
    expense=Expense.objects.get(id=pk)
    print(expense)
    form=AddExpenseForm(instance=expense)
    context={}
    context["form"]=form
    if request.method=="POST":
        form=AddExpenseForm(instance=expense,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("addexpense")
        else:
            context["form"] = form
            return render(request, "Budget/editexpense.html", context)
    return render(request, "Budget/editexpense.html", context)
@login_required()
def deleteExpense(request,pk):
    try:
        Expense.objects.get(id=pk).delete()
        return redirect("addexpense")
    except Exception as e:
        return redirect("addexpense")
@login_required()
def reviewExpense(request):
    form=ReviewExpenseForm(initial={"user":request.user})
    context={}
    context["form"]=form
    if request.method=='POST':
        form=ReviewExpenseForm(request.POST)
        if form.is_valid():
            fromdate=form.cleaned_data.get("from_date")
            todate = form.cleaned_data.get("to_date")
            print(fromdate,",",todate)
            total=Expense.objects.filter(date__gte=fromdate,date__lte=todate,user=request.user).aggregate(Sum('amount'))
            ex=Expense.objects.filter(date__gte=fromdate,date__lte=todate,user=request.user)
            context["total"]=total
            context["ex"] =ex
            return render(request, "Budget/ReviewExpense.html", context)
    return render(request,"Budget/ReviewExpense.html",context)