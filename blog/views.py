from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Post, Category, Tag, Comment
from .forms import PostForm, CommentForm, RecipeIngredientFormSet
from django.utils import timezone

def post_list(request):
    category = request.GET.get('category')
    tag = request.GET.get('tag')
    difficulty = request.GET.get('difficulty')
    search = request.GET.get('search')
    
    # فقط پست‌های منتشر شده را نمایش می‌دهیم
    posts = Post.objects.filter(status='published')
    
    if category:
        posts = posts.filter(category__slug=category)
    if tag:
        posts = posts.filter(tags__slug=tag)
    if difficulty:
        posts = posts.filter(difficulty=difficulty)
    if search:
        posts = posts.filter(
            Q(title__icontains=search) |
            Q(content__icontains=search) |
            Q(ingredients__ingredient__name__icontains=search)
        ).distinct()
    
    categories = Category.objects.all()
    tags = Tag.objects.all()
    
    return render(request, 'blog/post_list.html', {
        'posts': posts,
        'categories': categories,
        'tags': tags,
        'current_category': category,
        'current_tag': tag,
        'current_difficulty': difficulty,
        'search_query': search
    })

def post_detail(request, slug):
    # اگر کاربر ادمین نیست، فقط پست‌های منتشر شده را نمایش می‌دهیم
    if request.user.is_staff:
        post = get_object_or_404(Post, slug=slug)
    else:
        post = get_object_or_404(Post, slug=slug, status='published')
    
    comments = post.comments.all().order_by('-created_date')
    comment_form = CommentForm()
    
    # افزایش تعداد بازدید
    post.views += 1
    post.save()
    
    # محاسبه میانگین امتیازها
    average_rating = comments.aggregate(Avg('rating'))['rating__avg']
    
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'average_rating': average_rating
    })

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        ingredient_formset = RecipeIngredientFormSet(request.POST)
        
        if form.is_valid() and ingredient_formset.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()  # ذخیره برچسب‌ها
            
            ingredient_formset.instance = post
            ingredient_formset.save()
            
            return redirect('blog:post_detail', slug=post.slug)
    else:
        form = PostForm()
        ingredient_formset = RecipeIngredientFormSet()
    
    return render(request, 'blog/post_edit.html', {
        'form': form,
        'ingredient_formset': ingredient_formset
    })

@login_required
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.author != request.user:
        return redirect('blog:post_detail', slug=slug)
        
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        ingredient_formset = RecipeIngredientFormSet(request.POST, instance=post)
        
        if form.is_valid() and ingredient_formset.is_valid():
            post = form.save()
            ingredient_formset.save()
            return redirect('blog:post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)
        ingredient_formset = RecipeIngredientFormSet(instance=post)
    
    return render(request, 'blog/post_edit.html', {
        'form': form,
        'ingredient_formset': ingredient_formset
    })

@login_required
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.author == request.user:
        post.delete()
    return redirect('blog:post_list')

@login_required
@require_POST
def add_comment(request, slug):
    post = get_object_or_404(Post, slug=slug)
    form = CommentForm(request.POST)
    
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
        return redirect('blog:post_detail', slug=slug)
    
    return redirect('blog:post_detail', slug=slug)

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        text = request.POST.get('text')
        rating = request.POST.get('rating')
        if text:
            comment = Comment.objects.create(
                post=post,
                author=request.user,
                text=text
            )
            if rating:
                comment.rating = int(rating)
                comment.save()
    return redirect('blog:post_detail', slug=post.slug)

@login_required
@require_POST
def toggle_like(request, slug):
    post = get_object_or_404(Post, slug=slug)
    
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    
    return JsonResponse({
        'liked': liked,
        'likes_count': post.like_count()
    })

@login_required
@require_POST
def toggle_bookmark(request, slug):
    post = get_object_or_404(Post, slug=slug)
    
    if request.user in post.bookmarks.all():
        post.bookmarks.remove(request.user)
        bookmarked = False
    else:
        post.bookmarks.add(request.user)
        bookmarked = True
    
    return JsonResponse({
        'bookmarked': bookmarked,
        'bookmarks_count': post.bookmark_count()
    })

@login_required
def post_like(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
    return redirect('blog:post_detail', slug=post.slug)

@login_required
def post_bookmark(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        if request.user in post.bookmarks.all():
            post.bookmarks.remove(request.user)
        else:
            post.bookmarks.add(request.user)
    return redirect('blog:post_detail', slug=post.slug)
