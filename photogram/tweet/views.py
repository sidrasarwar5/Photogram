from django.shortcuts import render
from .models import Tweet
from .forms import TweetForm , UserRegistrationForm
from django.shortcuts import get_object_or_404 , redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from .forms import LoginForm
from django.db.models import Q
from django.http import JsonResponse
from django.template.loader import render_to_string


# Create your views here.
def index(request):
  return render(request, 'index.html')

def tweet_list(request):
  tweets = Tweet.objects.all().order_by('-created_at')
  return render(request , 'tweet_list.html' , {'tweets': tweets})

@login_required
def tweet_create(request):
  if request.method== "POST":
    form =TweetForm(request.POST , request.FILES)
    if form.is_valid():
      tweet = form.save(commit=False)
      tweet.user = request.user
      tweet.save()
      return redirect('tweet_list')

  else:
    form = TweetForm()
  return render(request , 'tweet_form.html' , {'form': form})

@login_required
def tweet_edit(request , tweet_id ):
  tweet = (get_object_or_404(Tweet, pk = tweet_id , user= request.user))
  if request.method== "POST":
    form =TweetForm(request.POST , request.FILES , instance = tweet)
    if form.is_valid():
      tweet = form.save(commit=False)
      tweet.user = request.user
      tweet.save()
      return redirect('tweet_list')
  else:
    form = TweetForm(instance = tweet)
  return render(request , 'tweet_form.html' , {'form': form})

@login_required
def tweet_delete(request , tweet_id):
  tweet = (get_object_or_404(Tweet, pk = tweet_id , user= request.user))
  if request.method== "POST":
    tweet.delete()
    return redirect('tweet_list')
  return render(request , 'tweet_confirm_delete.html' , {'tweet': tweet})


def register(request):
  if request.method == 'POST':
    form =UserRegistrationForm(request.POST)
    if form.is_valid():
      user = form.save(commit=False)
      user.set_password(form.cleaned_data['password1'])
      user.save()
      login(request , user)
      return redirect('tweet_list')
    else:
      # This line will print the exact validation failures to your terminal console
      print("Form Validation Errors:", form.errors)
  else:
    form = UserRegistrationForm()

  return render(request , 'registration/register.html' , {'form': form}) 

class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'


def search_suggestions(request):
    query = request.GET.get('q', '').strip()
    users = []
    tweets = []

    if query:
        users = User.objects.filter(username__icontains=query)[:5]
        tweets = Tweet.objects.filter(text__icontains=query).select_related('user')[:5]

    html = render_to_string('search_dropdown.html', {'users': users, 'tweets': tweets, 'query': query})
    return JsonResponse({'html': html})


def search(request):
    query = request.GET.get('q', '').strip()
    users = []
    tweets_by_user = []

    if query:
        # Users matching the query directly
        matched_users = User.objects.filter(username__icontains=query)

        # Tweets matching text, OR tweets belonging to a matched user
        tweets = Tweet.objects.filter(
            Q(text__icontains=query) | Q(user__in=matched_users)
        ).select_related('user').order_by('user__username', '-created_at')

        # Group tweets by user for display
        grouped = {}
        for tweet in tweets:
            grouped.setdefault(tweet.user, []).append(tweet)

        tweets_by_user = grouped.items()
        users = matched_users

    return render(request, 'search_results.html', {
        'query': query,
        'tweets_by_user': tweets_by_user,
        'users': users,
    })

def profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    tweets = Tweet.objects.filter(user=profile_user).order_by('-created_at')

    return render(request, 'profile.html', {
        'profile_user': profile_user,
        'tweets': tweets,
    })