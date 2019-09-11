from django.db import models


# Create your models here.

# User Models
class User(models.Model):
    id = models.IntegerField
    username = models.CharField(unique=True, max_length=60, default="")
    password = models.CharField(max_length=128, default="")

    def __str__(self):
        return "%s %s %s" % (self.id, self.username, self.password)


# Ticket Models
class Ticket(models.Model):
    id = models.IntegerField
    description = models.CharField(max_length=400)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20)

    def __str__(self):
        return self.id
