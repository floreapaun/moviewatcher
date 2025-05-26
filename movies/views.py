from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Movie, CustomUser
from .forms import MovieForm, RegisterForm, LoginForm
from .serializers import UserWithFriendsSerializer, FriendSerializer
from django.template.loader import render_to_string

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserWithFriendsSerializer

    @action(detail=True, methods=['post'])
    def add_friend(self, request, pk=None):
        user = self.get_object()
        friend_id = request.data.get('friend_id')
        try:
            friend = CustomUser.objects.get(pk=friend_id)
            user.add_friend(friend)
            return Response({'status': 'friend added'})
        except CustomUser.DoesNotExist:
            return Response({'error': 'Friend not found'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def remove_friend(self, request, pk=None):
        user = self.get_object()
        friend_id = request.data.get('friend_id')
        try:
            friend = CustomUser.objects.get(pk=friend_id)
            user.remove_friend(friend)
            return Response({'status': 'friend removed'})
        except CustomUser.DoesNotExist:
            return Response({'error': 'Friend not found'}, status=status.HTTP_400_BAD_REQUEST)

# -------------------------
# Movie Views
# -------------------------

@login_required
def movie_list(request):
    movies = Movie.objects.all().order_by('-watched_on')
    form = MovieForm()
    return render(request, 'movies/movie_list.html', {'movies': movies, 'form': form})

@login_required
def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.user = request.user
            movie.save()
            movies = Movie.objects.all().order_by('-watched_on')
            return render(request, 'movies/partials/movie_rows_add.html', {'movies': movies})
    return HttpResponse(status=400)

@login_required
def edit_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == "POST":
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            return render(request, "movies/partials/movie_row.html", {"movie": movie})
    else:
        form = MovieForm(instance=movie)

    return render(request, "movies/partials/movie_form_modal.html", {"form": form, "movie": movie})

@require_POST
@login_required
def delete_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    movie.delete()
    return HttpResponse("<!-- deleted -->")

@login_required
def movie_search(request):
    query = request.GET.get('q', '')
    movies = Movie.objects.all()
    if query:
        movies = movies.filter(
            Q(title__icontains=query) |
            Q(user__name__icontains=query)
        )
    return render(request, 'movies/partials/movie_rows.html', {'movies': movies})

# -------------------------
# Auth Views
# -------------------------

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'movies/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                email=form.cleaned_data['username'],  # Email used as username
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                return redirect('movie_list')
    else:
        form = LoginForm()
    return render(request, 'movies/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')


# -------------------------
# Friend Views
# -------------------------

@login_required
def friend_list(request):
    user = request.user
    friends = user.friends.all()  # users the current user follows

    # Get the list of IDs the user follows
    friends_ids = friends.values_list('id', flat=True)

    # Exclude self and already-followed users
    all_users = CustomUser.objects.exclude(id=user.id).exclude(id__in=friends_ids)

    return render(request, 'movies/friends.html', {
        'friends': friends,
        'all_users': all_users,
    })

@login_required
def add_friend(request, user_id):
    friend = get_object_or_404(CustomUser, id=user_id)
    request.user.friends.add(friend)
    return redirect('friend_list')

@login_required
def remove_friend(request, user_id):
    friend = get_object_or_404(CustomUser, id=user_id)
    request.user.friends.remove(friend)
    return redirect('friend_list')
