from django.db import models
from django.utils import timezone
from django.urls import reverse
# Create your models here.
class Post(models.Model):
    author = models.ForeignKey('auth.User',on_delete=models.CASCADE) #not for multi users project, this is directed linked to superuser
    title = models.CharField(max_length=200)
    text = models.TextField()#don't know the length of words
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)#if you don't want it published just leave it blank or null(meaning empty)

    def publish(self): #it will have the publish button
        self.published_date = timezone.now()
        self.save()

    def approve_comments(self):
        return self.comments.filter(approved_comment=True)#filter it, and show them along the post

    def get_absolute_url(self):#you can't call it something out, django default, it means once you create the instance of the post, what's next
        return reverse("post_detail",kwargs={'pk':self.pk}) #go back to specific pk post_detail view page

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments',on_delete=models.CASCADE) #'blog.post'= blog application's post
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)# at beginning set all false

    def approve(self):#it will have the approve button
        self.approved_comment = True
        self.save() #存入資料庫

    def get_absolute_url(self): #當views已指定reverse 的urls時,這個method會變沒意義,  我猜這邊只是當作練習(advcbv 有相同練習)
        return reverse('post_list')#go back to post_list view

    def __str__(self):
        return self.text
