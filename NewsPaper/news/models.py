from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models import Sum
from django.urls import reverse

article = 'ART'
new = 'NEW'

POSTS = [
    (article, 'Статья'),
    (new, 'Новость'),
]


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        posts_rating = Post.objects.filter(author=self).aggregate(Sum('rating'))['rating__sum']
        author_comments_rating = Comment.objects.filter(user=self.user).aggregate(Sum('rating'))['rating__sum']
        post_comments_rating = Comment.objects.filter(post__author=self).aggregate(Sum('rating'))['rating__sum']
        if posts_rating is None:
            posts_rating = 0
        if author_comments_rating is None:
            author_comments_rating = 0
        if post_comments_rating is None:
            post_comments_rating = 0

        self.rating = posts_rating * 3 + author_comments_rating + post_comments_rating

        self.save()

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    subscribers = models.ManyToManyField(User, blank=True, related_name='categories')

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255, default='Без названия')
    text = models.TextField()
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='all_posts')
    post_kind = models.CharField(max_length=3, choices=POSTS, default=new)
    post_time = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[:50:] + '...'

    def __str__(self):
        return f'{self.title[:50]}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
