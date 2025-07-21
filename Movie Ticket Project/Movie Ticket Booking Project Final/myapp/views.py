from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie, Booking, Transaction
import requests
from datetime import datetime
from django.http import HttpResponse
from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponseBadRequest
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

colors.darkbrown = colors.Color(0.4, 0.2, 0.1)  

API_KEY = '444718ae5d4f5dc19c780e79ada78271'

def index(request):
    query = request.GET.get('query', '')
    movies = []
    if query:
        response = requests.get(f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={query}&language=ta-IN")
        if response.status_code == 200:
            movies = response.json().get('results', [])
    return render(request, 'index.html', {'movies': movies})

def select_movie(request, movie_id):
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=ta-IN")
    movie_data = response.json()
    movie, created = Movie.objects.get_or_create(
        title=movie_data['title'],
        defaults={
            'poster_path': f"https://image.tmdb.org/t/p/w500{movie_data.get('poster_path', '')}",
            'description': movie_data.get('overview', ''),
            'release_date': movie_data.get('release_date', None),
        }
    )
    return render(request, 'movie.html', {'movie': movie})

def book_tickets(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    seat_numbers = range(1, 101)
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        show_date = request.POST.get('show_date')
        seats = request.POST.get('seats') 
        if not customer_name or not show_date or not seats:
            return HttpResponseBadRequest("All fields are required.")
        try:
            show_date = datetime.strptime(show_date, "%Y-%m-%d").date()
        except ValueError:
            return HttpResponseBadRequest("Invalid show date format.")
        seat_list = seats.split(',')
        amount_paid = len(seat_list) * 200 
        existing_bookings = Booking.objects.filter(movie=movie, show_date=show_date)
        occupied_seats = [
            seat for booking in existing_bookings for seat in booking.seats.split(',')
        ]
        for seat in seat_list:
            if seat in occupied_seats:
                return HttpResponseBadRequest(f"Seat {seat} is already booked for this date.")
        booking = Booking.objects.create(
            movie=movie,
            customer_name=customer_name,
            seats=seats,
            show_date=show_date,
            amount_paid=amount_paid
        )
        return redirect('confirm_booking', booking_id=booking.id) 
    else:
        show_date = request.GET.get('show_date', datetime.now().date())
        bookings = Booking.objects.filter(movie=movie, show_date=show_date)
        occupied_seats = [
            seat for booking in bookings for seat in booking.seats.split(',')
        ]
    return render(request, 'book_tickets.html', {
        'movie': movie,
        'seat_numbers': seat_numbers,
        'occupied_seats': occupied_seats,
    })



def generate_ticket(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    margin = 40
    width, height = letter
    p.setFillColor(colors.lightblue)
    p.rect(0, 0, width, height, fill=1)
    p.setFillColor(colors.green)
    p.rect(0, height - 70, width, 70, fill=1)
    p.setFont("Helvetica-Bold", 26)
    p.setFillColor(colors.white)
    p.drawString(margin, height - 50, "🎬 Movie Ticket 🎬")
    p.setStrokeColor(colors.grey)
    p.setLineWidth(1)
    p.line(margin, height - 100, width - margin, height - 100)
    p.setFont("Helvetica-Bold", 16)
    p.setFillColor(colors.black)
    p.drawString(margin, height - 130, f"Movie: {booking.movie.title}")
    p.setFont("Helvetica", 12)
    p.setFillColor(colors.darkbrown)
    p.drawString(margin, height - 150, f"Customer: {booking.customer_name}")
    p.drawString(margin, height - 170, f"Seats: {booking.seats}")
    p.drawString(margin, height - 190, f"Show Date: {booking.show_date}")
    p.drawString(margin, height - 210, f"Amount Paid: Rs.{booking.amount_paid}")
    right_section_width = 100
    p.setFillColor(colors.darkbrown)
    p.rect(width - right_section_width, 0, right_section_width, height, fill=1)
    p.setFont("Helvetica-Bold", 14)
    p.setFillColor(colors.white)
    p.drawString(width - right_section_width + 10, height - 100, "Ticket ID:")
    p.drawString(width - right_section_width + 10, height - 120, f"{booking.id}")
    p.setStrokeColor(colors.grey)
    p.setLineWidth(2)
    p.roundRect(margin - 10, margin, width - margin * 2 + 20, height - margin * 2, radius=10, stroke=1)
    p.setFont("Helvetica-Oblique", 12)
    p.setFillColor(colors.grey)
    p.drawString(margin, margin - 10, "Thank you for choosing us! Enjoy the show.")
    p.showPage()
    p.save()
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=ticket_{booking.id}.pdf'
    return response


def provide_details(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == 'POST':
        seats = request.POST.get('seats', '')
        customer_name = request.POST.get('customer_name', 'Anonymous')
        show_date = request.POST.get('show_date', '')
        if not seats:
            return redirect('book_tickets', movie_id=movie_id)
        seat_list = seats.split(',')
        total_price = len(seat_list) * 200
        context = {
            'movie': movie,
            'seats': seat_list,
            'customer_name': customer_name,
            'show_date': show_date,
            'total_price': total_price,
        }
        return render(request, 'details.html', context)

def confirm_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'confirmation.html', {'booking': booking})

def thank_you(request):
    return render(request, 'thank_you.html')

def success(request):
    return render(request, 'success.html')

def payment_process(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        try:
            payment_successful = True
            if payment_successful:
                booking.paid = True
                booking.save()
                transaction = Transaction.objects.create(
                    booking=booking,
                    amount=booking.amount_paid,
                    status='successful',
                )
                return redirect('payment_success', transaction_id=transaction.id)
            else:
                return redirect('payment_failed', booking_id=booking.id)
        except Exception:
            return redirect('payment_failed', booking_id=booking.id)
    return render(request, 'payment.html', {'booking': booking})

def payment_success(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    booking = transaction.booking
    return render(request, 'payment_success.html', {'transaction': transaction, 'booking': booking})

def payment_failed(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'payment_failed.html', {'booking': booking})
