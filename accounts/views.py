from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_http_methods
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.core.cache import cache
from django.http import HttpResponseForbidden
from .forms import SignUpForm
import time

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def check_request_limit(request, key_prefix, max_attempts=5, timeout=3600):
    client_ip = get_client_ip(request)
    cache_key = f"{key_prefix}_{client_ip}"
    attempts = cache.get(cache_key, 0)
    
    if attempts >= max_attempts:
        return False
    
    cache.set(cache_key, attempts + 1, timeout)
    return True

@sensitive_post_parameters()
@csrf_protect
@never_cache
@require_http_methods(["GET", "POST"])
def signup(request):
    if getattr(request, 'limited', False):
        return HttpResponseForbidden('Too many signup attempts. Please try again later.')
        
    if request.user.is_authenticated:
        return redirect('blog:post_list')
    
    if request.method == 'POST':
        if not check_request_limit(request, 'signup', max_attempts=5, timeout=3600):
            return HttpResponseForbidden('تعداد تلاش‌های شما بیش از حد مجاز است. لطفاً یک ساعت دیگر امتحان کنید.')
        
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('blog:post_list')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def profile(request):
    if not request.user.is_authenticated:
        raise PermissionDenied()
    return render(request, 'registration/profile.html')
