from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.urls import path

from . import utils as core_utils
from . import views
from . import views as core_views

urlpatterns = [
    # Store.
    # Leave as empty string for base url.
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateitem, name="update_item"),
    path('process_order/', views.processorder, name="process_order"),
    path('product_details/<int:pk_id>', views.product_details, name="product_details"),

    # User Profiles
    path('set_profile/', views.set_profile, name="set_profile"),
    path('profile_ship/', views.profile_ship, name="profile_ship"),
    path('profile_orders/', views.profile_orders, name="profile_orders"),
    path('profile_passwd_update/', views.profile_passwd_update, name="profile_passwd_update"),

    # Authentication
    path('register/', views.register_page, name="register"),
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_user, name="logout"),

    # Password Reset
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='store/password_reset.html'), name='password_reset'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='store/password_reset_done.html'), name='password_reset_done'),

    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='store/password_reset_confirm.html'), name='password_reset_confirm'),

    path('password_reset_complete', auth_views.PasswordResetCompleteView.as_view(
        template_name='store/password_reset_complete.html'), name='password_reset_complete'),

    # Register, activation email.
    url(r'^account_activation_finish/$', core_views.account_activation_finish,
        name='account_activation_finish'),

    url(r'^account_activation_invalid/$', core_views.account_activation_invalid,
        name='account_activation_invalid'),

    url(r'^account_activation_sent/$', core_views.account_activation_sent,
        name='account_activation_sent'),

    path('activate/<uidb64>/<token>/', core_utils.activate, name='activate'),
]
