from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Room


def index_view(request):
    return render(
        request,
        "chat/index.html",
        {
            "rooms": Room.objects.all(),
        },
    )


@login_required
def room_view(request, room_name):
    room, created = Room.objects.get_or_create(name=room_name)
    # retrieve chat history
    latest_messages = room.chat_messages.select_related("user").order_by("-id")[:5]
    latest_messages = reversed(latest_messages)
    return render(
        request,
        "chat/room.html",
        {
            "room": room,
            "latest_messages": latest_messages,
        },
    )
