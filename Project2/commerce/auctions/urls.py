from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('categories',views.categories,name='categories'),
    path("product/<int:id>", views.product, name="product"),
    path('create',views.createListing, name='create'),
    path('addToWatchlist/<int:id>',views.addToWatchlist,name='addToWatchlist'),
    path('removeFromWatchlist/<int:id>',views.removeFromWatchlist, name='removeFromWatchlist'),
    path('watchlist',views.watchlist,name='watchlist'),
    path('comment/<int:id>',views.comment,name='comment'),
    path('offer/<int:id>',views.offer,name='offer'),
    path('removeAuction/<int:id>',views.removeAuction,name='removeAuction'),
    path('closed',views.closed,name='closed')
    

]
