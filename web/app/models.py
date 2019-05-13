from django.db import models

# Create your models here.


class Room(models.Model):
    status = models.CharField(max_length=20)
    roomid = models.CharField(max_length=100)
    history = models.CharField(max_length=5000)
    cmd = models.CharField(max_length=200)
    time = models.CharField(max_length=20)
    lastTime = models.CharField(max_length=20)

    def __str__(self):
        return self.roomid


class User(models.Model):
    name = models.CharField(max_length=100)
    room = models.CharField(max_length=100)
    score = models.CharField(max_length=20)
    act = models.CharField(max_length=40)
    status = models.CharField(max_length=10)
    useScript = models.CharField(max_length=5)

    def __str__(self):
        return self.room + self.name
