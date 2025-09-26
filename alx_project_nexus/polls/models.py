from django.db import models
from django.utils import timezone

class Poll(models.Model):
    title = models.CharField(max_length=200)
    option1 = models.CharField(max_length=100, default="Unknown")
    option2 = models.CharField(max_length=100 , default="Unknown")

    def __str__(self):
        return self.title

class Option(models.Model):
    poll = models.ForeignKey(Poll, related_name='options', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)

    class Meta:
        unique_together = ('poll', 'text')  # Prevent duplicate options per poll

class Vote(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    user_ip = models.GenericIPAddressField()  # Simple duplicate prevention via IP
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('poll', 'user_ip')  # One vote per IP per poll
        indexes = [
            models.Index(fields=['poll', 'option']),  # For efficient counting
        ]