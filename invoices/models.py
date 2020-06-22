from django.db import models
from users.models import CustomUser

class Invoice(models.Model):
	title = models.CharField(max_length=100)
	date_created = models.DateField(auto_now=True)
	amount = models.DecimalField(decimal_places=2, max_digits=10)
	currency = models.CharField(max_length=10,default='USD')
	is_paid = models.BooleanField(default=False)
	date_paid = models.DateField(blank=True, null=True)
	payee = models.ForeignKey(CustomUser, blank=True, null=True, related_name="payee", on_delete=models.CASCADE)	
	payor = models.ForeignKey(CustomUser, blank=True, null=True, related_name="payor", on_delete=models.CASCADE)
	stripe_payment_id = models.CharField(max_length=150, blank=True, null=True)

	def __str__(self):
		return str(self.id)