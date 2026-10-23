"""penProgram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from pstart import views

urlpatterns = [
    #path('admin', admin.site.urls),
    path('',views.index,name="index"),
    path('inputp',views.inputP,name="inputproyek"),
    path('inputk',views.inputKriteria,name="inputkriteria"),
    path('prockrit',views.prosesKriteria,name="prockriteria"),
    path('displayper',views.displayPersamaan,name="displaypersamaan"),
    path('prosesubahpersamaan',views.ubahdataPersamaan,name="prosubahper"),
    path('hitungpersamaan',views.hasil,name="hitungpersamaan"),
    path('prosesproyek',views.prosesinputproyek,name="prosesinputproyek"),
    path('editproyek/<int:idpro>',views.editProyek,name="editproyek"),
    path('peditproyek/<int:idpro>',views.prosesedit,name="pproyek"),
    path('displayproyek',views.displaypro,name="dproyek"),
    path('hapuspro/<int:idpro>',views.hapuspro,name="hproyek"),
    path('selesaipro/<int:idpro>',views.setselesai,name="setproyek"),
    path('home',views.home,name="home"),
    path('editkrit/<slug:idkrit>',views.editKriteria,name="editkriteria"),
    path('daftarkrit',views.daftarKriteria,name="daftarkriteria"),
    path('daftarsub/<slug:idkrit>',views.daftarSubKrit,name="daftarsubkrit"),
    path('proceditkrit/<slug:idkrit>',views.prosesUbahKrit,name="prosesedit"),
    path('hapuskrit/<slug:idkrit>',views.hapuskriteria,name="hapuskrit"),
    path('inputopsi',views.tambahOpsi,name="tambahopsi"),
    path('prosesopsi',views.prosestambah,name="opsiproses"),
    path('daftaropsi',views.displayOpsi,name="daftaropsi"),
    path('ubahopsit/<slug:idopsi>',views.ubahOpsi,name="ubahOpsi"),
    path('ubahediopsit/<slug:idopsi>',views.procUbahOpsi,name="ubahOpsi"),
    path('deleteopsi/<slug:idopsi>',views.deleteOpsi,name="ubahOpsi"),
    path('login',views.login,name="ubahOpsi"),
    path('proclogin',views.proseslogin,name="proseslogin"),
    path('inputu',views.inputuser,name="inputuser"),
    path('procuser',views.procinputuser,name="procuser"),
    path('daftaruser',views.viuser,name="daftaruser"),
    path('edituser/<slug:iduser>',views.edituser,name="edituser"),
    path('procedituser/<slug:iduser>',views.procedituser,name="edituser"),
    path('deleteuser/<slug:iduser>',views.deleteuser,name="deleteuser"),
    path('logout',views.logout,name="logout")
]

