# billing/models.py
from django.db import models
from django.conf import settings

class Invoice(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='invoices')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Invoice {self.id} for {self.user.username}"

class Payment(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)  # e.g., Stripe, Paypal

    def __str__(self):
        return f"Payment {self.id} for Invoice {self.invoice.id}"