
from django.contrib import admin
from django.urls import path,include
from Budget.views import register,signIn,signOut,editProfile,userHome,addExpense
urlpatterns = [
    path("register",register,name="register"),
    path("signin",signIn,name="signin"),
    path("signout",signOut,name="signout"),
    path("edit",editProfile,name="editprofile"),
    path("home",userHome,name="home"),
    path("add",addExpense,name="addexpense"),
]