from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from blog.models import Post, Comment
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.forms import PostForm, CommentForm
from django.urls import reverse_lazy
from django.views.generic import (TemplateView,
                                    ListView,
                                    DetailView,
                                    CreateView,
                                    UpdateView,
                                    DeleteView,)

# Create your views here.


class AboutView(TemplateView):
    template_name = 'about.html'


class PostListView(ListView):#default expects post_list.html
    model = Post
    #define particular get method
    def get_queryset(self):#use django ORM(object-relational mapping) that can add little more custom touch on it
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date') #__lte means: less than or equal to
    #above like a sq query on my model: grab the post models all the objects there and filter out based on these conditions
    #'-published_date' desc order '-'
class PostDetailView(DetailView):#default expects post_detail.html
    model = Post


class CreatePostView(LoginRequiredMixin, CreateView):#LoginRequiredMixin for CBV, and fbv use decorator
    login_url = '/login/' # for LoginRequiredMixin
    redirect_field_name = 'blog/post_detail.html' #once you login it will send you to post_form.html,after create it sends you back to post_detail
    form_class = PostForm #use a particular form, instead of cbc form(advcbv)
    model = Post


class PostUpdateView(LoginRequiredMixin, UpdateView):#for post_form.html(default expect format)
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm #default context name = form,
    model = Post


class PostDeleteView(LoginRequiredMixin, DeleteView):#default expects post_confirm_delete.html
    model = Post
    success_url = reverse_lazy('post_list')


class DraftListView(LoginRequiredMixin, ListView):#list all my unpublished drafts, default expects post_draft_list.html
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')

@login_required
def post_publish(request,pk): #藉由傳送過來的url指定的pk 幫助你找尋特定pk的post
    post = get_object_or_404(Post, pk=pk)
    post.publish() #from post model 這邊記得post.publish() 加括號不然不會有動作
    return redirect('post_detail', pk=pk)
##### Comments #####


@login_required
def add_comment_to_post(request,pk):#pk, link comment to the specific post,想成在specific pk post 物件, 按下 add comment
    post = get_object_or_404(Post, pk=pk) #grab the specific pk post or 404 can't find,
    if request.method == 'POST':
        form = CommentForm(request.POST)#request.POST: hit the post request
        if form.is_valid():
            comment = form.save(commit=False) #via comment_form, model = comment, commit=False hasn’t yet been saved to the database
            comment.post = post #model, comment foreign key 綁定特定post, commit=False cause we want to do some custom processing
            comment.save()#save to database
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html',{'form':form})

@login_required
def comment_approve(request,pk):#藉由傳送過來的url指定的pk, get_object_or_404幫助你找尋特定pk的comment, 物件導向每個comment都有自己專屬的pk
    comment = get_object_or_404(Comment, pk=pk) #從cooment資料庫拿取特定pk的comment, 注意這裡的pk不是post資料庫的pk,是comment資料庫自己的pk
    comment.approve() #from comment model, 注意Comment(class),comment(class object) 不一樣 不要搞混
    return redirect('post_detail',pk=comment.post.pk)

@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk #pror to deleting comment, assign a post_pk variable to store post.pk
    comment.delete()
    return redirect('post_detail',pk=post_pk)
