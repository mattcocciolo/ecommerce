from django.urls import path, re_path

from . import views

urlpatterns = [
    # Ware.
    # Leave as empty string for base url.

    path('', views.ware, name="ware"),
    path('orders/', views.orders, name="orders"),
    path('process_orders/<str:pk_transaction_id>', views.process_orders, name="process_orders"),
    path('processed_orders/', views.processed_orders, name="processed_orders"),
    path('details/<str:pk_transaction_id>', views.details, name="details"),
    path('button_id/<str:pk_transaction_id>', views.button_id, name='button_id'),

]
