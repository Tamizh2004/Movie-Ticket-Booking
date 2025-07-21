from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('movie/<int:movie_id>/', views.select_movie, name='select_movie'),
    path('details/<int:movie_id>/', views.provide_details, name='provide_details'),
    path('ticket/<int:booking_id>/', views.generate_ticket, name='generate_ticket'),
  path('movie/<int:movie_id>/confirm/', views.confirm_booking, name='confirmation'),
      path('movie/<int:movie_id>/details/', views.provide_details, name='details'),
      path('book_tickets/<int:movie_id>/', views.book_tickets, name='book_tickets'),
    path('confirm_booking/<int:booking_id>/', views.confirm_booking, name='confirm_booking'),
    path('success/', views.success, name='success'),
     path('thank-you/', views.thank_you, name='thank_you'),
     path('confirm-booking/<int:movie_id>/', views.confirm_booking, name='confirm_booking'),
    
   path('generate_ticket/<int:booking_id>/', views.generate_ticket, name='generate_ticket'),
 
 path('payment/<int:booking_id>/', views.payment_process, name='payment_process'),
    path('payment_success/<int:transaction_id>/', views.payment_success, name='payment_success'),
    path('payment_failed/<int:booking_id>/', views.payment_failed, name='payment_failed'),
    
]
   

