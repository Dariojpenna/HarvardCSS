from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name='register'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("deposit", views.deposit, name="deposit"),
    path("transfer", views.transfer, name="transfer"),
    path("services", views.services, name="services"),
    path('code_generator/', views.code_generator, name='code_generator'),
    path('code_checker/', views.code_checker, name='code_checker'),
    path('transfer_detail/<int:transactionId>',views.transfer_detail,name="transfer_detail"),
    path('profile',views.profile,name="profile"),
    path('editEmail/',views.editEmail,name="editEmail"),
    path('editPhone/',views.editPhone,name="editPhone"),
    path('addService', views.addService,name='addService'),
    path('service_detail/<int:id>', views.service_detail, name='service_detail'),
    path('service_pay/<int:id>',views.service_pay,name='service_pay')
]