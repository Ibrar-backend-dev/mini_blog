from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_comment_notification_email(post_title, commenter_name, comment_text,author_email):
    
    subject = f"New Comment on '{post_title}'"

    message = (
        f"A new comment has been added to your post '{post_title}'.\n\n"
        f"Commenter: {commenter_name}\n"
        f"Comment: {comment_text}\n\n"
    )

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[author_email],
        fail_silently=False,
    )

