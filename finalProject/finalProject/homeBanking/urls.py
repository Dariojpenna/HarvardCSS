from django.urls import path
from django.contrib.auth import views as auth_views
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
    path('service_pay/<int:id>',views.service_pay,name='service_pay'),
    path('voucher/<int:id>', views.voucher, name='voucher'),
    path('account',views.account, name='account'),
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset_password/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset_password/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('cards',views.cards,name='cards'),
    path('addCard', views.addCard,name='addCard'),
    path('deleteCard', views.deleteCard,name='deleteCard'),

]