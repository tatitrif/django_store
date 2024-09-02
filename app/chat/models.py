from django.db import models

from account.models import User


class Room(models.Model):
    name = models.CharField(max_length=128)
    online = models.ManyToManyField(User, related_name="room_joined", blank=True)

    def get_online_count(self):
        return self.online.count()

    def join(self, user):
        self.online.add(user)
        self.save()

    def leave(self, user):
        self.online.remove(user)
        self.save()

    def __str__(self):
        return f"{self.name} ({self.get_online_count()})"


class Message(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="chat_messages",
    )
    room = models.ForeignKey(
        "Room",
        on_delete=models.CASCADE,
        related_name="chat_messages",
    )
    content = models.CharField(max_length=512)
    sent_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}: {self.content} [{self.sent_on}]"
