from django.shortcuts import render, redirect
import datetime
from django.contrib.auth.decorators import login_required
import random

from .models import PostModel, CategoryModel


from userapp.models import UserModel
from django.contrib.auth.models import User
from .forms import PostForm

from django.contrib.auth.decorators import login_required


def get_featured_post(posts):
    if len(posts) == 0:
        return None
    else:
        num_of_posts = len(posts)
        featured_post_index = random.randint(0, num_of_posts-1)
        return posts[featured_post_index]


def index(request):
    posts = PostModel.objects.all().order_by(
        'posted_on', 'title', 'posted_by')[:10]
    categories = CategoryModel.objects.all()[:5]
    context = {
        'posts': posts,
        'categories': categories,
        'featured_post': get_featured_post(posts)
    }
    return render(request, 'newsapp/index.html', context)


def detail(request, id):
    post = PostModel.objects.filter(id=id).first()
    categories = CategoryModel.objects.all()[:5]
    context = {
        'post': post,
        'categories': categories
    }
    return render(request, 'newsapp/detail.html', context)


def categorynews(request, id):
    category = CategoryModel.objects.filter(id=id).first()
    if category:
        posts = PostModel.objects.filter(category=category)
        categories = CategoryModel.objects.all()[:5]
        context = {
            'posts': posts,
            'categories': categories,
            'featured_post': get_featured_post(posts),
            'current_category_id': id
        }
        return render(request, 'newsapp/index.html', context)
    else:
        return render(request, 'newsapp/error404.html')


@login_required
def add_post_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            # now write logic to add the form
            post = form.save(commit=False)
            current_user = UserModel.objects.filter(
                auth=request.user.id).first()
            if current_user:
                post.posted_by = current_user
                post.save()
                return redirect('index')
            else:
                return redirect('login')
            # this means the form has errors. Send the user back to the same page
            return render(request, 'newsapp/add_post.html', {'form': form})
    else:
        form = PostForm()
        categories = CategoryModel.objects.all()[:5]
        context = {
            'categories': categories,
            'form': form
        }
        return render(request, 'newsapp/add_post.html', context)


@login_required
def delete_post_view(request, id):
    post = PostModel.objects.filter(id=id).first()
    if post:
        logged_in_user_id = request.user.id
        post_user_id = post.posted_by.auth.id
        if logged_in_user_id == post_user_id:
            # this post is of this user. delete it
            post.delete()
            # send user to index
            return redirect('index')
        else:
            # user is trying to delete someone else post
            return render(request, 'newsapp/error404.html')
    else:
        # there is no post with that id
        return render(request, 'newsapp/error404.html')


@login_required
def edit_post_view(request, id):
    if request.method == "POST":
        post = PostModel.objects.filter(id=id).first()
        if post:
            current_user_id = request.user.id
            post_user_id = post.posted_by.auth.id
            if current_user_id == post_user_id:
                # this is valid user. give him to update the post
                form = PostForm(
                    request.POST, files=request.FILES, instance=post)
                if form.is_valid():
                    form.save()
                    return redirect('detail', post.id)
                else:
                    #form is not valid
                    return(request, 'newsapp/edit_post.html', {'form': form})
            else:
                return render(request, 'newsapp/error404.html')
        else:
            return render(request, 'newsapp/error404.html')
    else:
        post = PostModel.objects.filter(id=id).first()
        if post:
            form = PostForm(instance=post)
            return render(request, 'newsapp/edit_post.html', {'form': form})
        else:
            return render(request, 'newsapp/error404.html')


def search_view(request):
    categories = CategoryModel.objects.all()[:5]
    query = request.GET.get('query')
    results_in_title = PostModel.objects.filter(title__icontains=query)
    results_in_content = PostModel.objects.filter(content__icontains=query)
    results = (results_in_content | results_in_title).distinct()
    context = {
        'posts': results,
        'search_query': query,
        'categories': categories
    }
    return render(request, 'newsapp/search_results.html', context)
