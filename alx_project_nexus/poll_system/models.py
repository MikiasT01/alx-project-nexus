from django.db import models

class Poll(models.Model):
          title = models.CharField(max_length=200)
          creation_date = models.DateTimeField(auto_now_add=True)
          expiry_date = models.DateTimeField()

          def __str__(self):
              return self.title

class Option(models.Model):
          poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='options')
          text = models.CharField(max_length=200)
          vote_count = models.IntegerField(default=0)

          def __str__(self):
              return f"{self.text} (Poll: {self.poll.title})"

class Vote(models.Model):
          user_id = models.CharField(max_length=100)
          option = models.ForeignKey(Option, on_delete=models.CASCADE)
          vote_date = models.DateTimeField(auto_now_add=True)

          class Meta:
              unique_together = ('user_id', 'option')

          def __str__(self):
              return f"Vote by {self.user_id} on {self.option.text}"