from celery import shared_task
import time
from datetime import datetime, timedelta

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post, Category


@shared_task
def notification_about_news(pk):
    post = Post.objects.get(pk=pk)
    categories = post.category.all()
    title = post.title
    subscribers_emails = []

    for cat in categories:
        subscribers = cat.subscribers.all()
        subscribers_emails += [s.email for s in subscribers]

    html_content = render_to_string(
            'post_created_email.html',
        {
            'title': title,
            'link':  f'{settings.SITE_URL}/news/{post.id}',
        }
        )

    msg = EmailMultiAlternatives(
            subject=title,
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=subscribers_emails
        )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()

@shared_task
def notification():
    today = datetime.now()
    last_week = today - timedelta(days=7)
    posts = Post.objects.filter(post_time__gte=last_week)
    categories = set(posts.values_list('category__name', flat=True))
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))

    html_content = render_to_string(
        'weekly_posts.html',
        {
            'link': settings.SITE_URL,
            'posts': posts
        }
    )

    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()



