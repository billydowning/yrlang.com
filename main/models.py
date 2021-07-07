from django.db import models
from users.models import CustomUser
from jsonfield import JSONField

class Notification(models.Model):
	name = models.CharField(max_length=150)
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	timestamp = models.DateTimeField(auto_now=True)
	payload = JSONField()

	def __str__(self):
		return self.name

class Review(models.Model):
	date_posted = models.DateTimeField(auto_now=True)
	review = models.TextField()
	rating = models.CharField(max_length=10)
	reviewer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="reviewer")
	reviewee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="reviewee")

	def __str__(self):
		return self.reviewer.email+" "+self.rating