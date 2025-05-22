from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.core.mail import send_mail
from django.utils.html import strip_tags


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.ratingAuthor = pRat * 3 + cRat
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    subscribers = models.ManyToManyField(User, related_name='subscribed_categories', blank=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    NEWS = 'NS'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )
    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)
    dateCreations = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    rating = models.SmallIntegerField(default=0)
    postCategory = models.ManyToManyField(Category, through='PostCategory')

    def __str__(self):
        return f'Вы опубликовали {self.categoryType}: {self.title}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.content[:123] + '...'


def send_news_email_to_user(user, post):
    subject = post.title

    html_content = f"<h1>{post.title}</h1>{post.content}"

    preview_text = post.content[:50]

    text_content = f"Здравствуй, {user.username}. Новая статья в твоём любимом разделе!\n\n" \
                   f"{strip_tags(html_content)[:50]}..."

    message_body = f"<!DOCTYPE html><html><body>{html_content}</body></html>"

    send_mail(
        subject,
        text_content,
        't.maill@yandex.ru',
        [user.email],
        html_message=message_body,
        fail_silently=False,
    )


@receiver(post_save, sender=Post)
def send_news_email(self, instance, created, **kwargs):
    if created:
        category = instance.category
        subscribers = category.subscribers.all()
        for user in subscribers:
            send_news_email_to_user(user, instance)


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryTrough = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    postComment = models.ForeignKey(Post, on_delete=models.CASCADE)
    userComment = models.ForeignKey(User, on_delete=models.CASCADE)
    commentary = models.TextField()
    dateCreations = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

