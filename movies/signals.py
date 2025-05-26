from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Movie

@receiver(post_save, sender=Movie)
def notify_friends_on_movie_add(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        friends = user.friends.all()
        channel_layer = get_channel_layer()

        print("Signal triggered. Notifying friends...")

        for friend in friends:
            print(f"Sending to: user_{friend.id}")
            async_to_sync(channel_layer.group_send)(
                f"user_{friend.id}",
                {
                    "type": "send_notification",
                    "message": f"{user.name} watched a new movie: {instance.title}"
                }
            )
