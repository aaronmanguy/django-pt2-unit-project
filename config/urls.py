from django.contrib import admin
from django.urls import path
from app.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', home, name='home'),
    path('<int:pk>', viewProduct, name='view-product'),
    path('create-product', createProduct, name='create-product'),
    # path("delete-product/<int:pk>", deleteProduct, name='delete-product'),
    path("register", registerPage, name='register'),
    path("login", loginPage, name='login'),
    path("logout", logoutUser, name='logout'),
    path("profile/<int:pk>", profilePage, name='profile'),
    path("edit-profile/<int:pk>", editProfile, name='edit-profile'),
    # path("all-users", all_users, name='all-users'),
    # path("delete-user/<int:pk>", delete_user, name='delete-user'),
    # path("self-user-delete/<int:pk>", self_user_delete, name='self-user-delete'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)