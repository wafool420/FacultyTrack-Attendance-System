from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login_user', views.login_user, name="login"),
    path('logout_user', views.logout_user, name="logout"),
    path('register_user', views.register_user, name="register"),
    path('', views.home, name="home"),
    path("delete-account/", views.delete_account, name="delete_account"),
    path("change-password/", views.change_password, name="change_password"),
    path("incoming-requests/", views.incoming_requests, name="incoming_requests"),
    path("approve-user/<int:profile_id>/", views.approve_user, name="approve_user"),
    path("reject-user/<int:profile_id>/", views.reject_user, name="reject_user"),
    path("delete-rejected-user/<int:profile_id>/", views.delete_rejected_user, name="delete_rejected_user"),
    path("remove-approved-user/<int:profile_id>/", views.remove_approved_user, name="remove_approved_user"),
]
