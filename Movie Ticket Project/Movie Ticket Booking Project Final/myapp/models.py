from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=200)
    poster_path = models.URLField(blank=True)
    description = models.TextField(blank=True)
    release_date = models.DateField()

    def __str__(self):
        return self.title

class Booking(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=200)
    seats = models.TextField()  # Store seat numbers as a comma-separated string
    show_date = models.DateField()
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} - {self.movie.title}"


class Transaction(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)  # E.g., 'successful', 'failed'
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction {self.id} - {self.status}"