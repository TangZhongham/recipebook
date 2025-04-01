from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from .models import Recipe, Comment, Favorite, User
from .forms import RecipeForm, CommentForm, UserProfileForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST

def index(request):
    # Your homepage view
    return render(request, 'recipe_web/home.html')

@login_required
def recipe_list(request):
    recipes = Recipe.objects.all().order_by('-created_at')
    
    # Get search and filter parameters
    search_query = request.GET.get('q', '')
    cuisine_type = request.GET.get('cuisine_type', 'All')
    dietary_type = request.GET.get('dietary_type', 'All')

    # Apply search filter
    if search_query:
        recipes = recipes.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(cuisine_type__icontains=search_query)
        ).distinct()

    # Apply cuisine filter
    if cuisine_type and cuisine_type != 'All':
        recipes = recipes.filter(cuisine_type=cuisine_type)

    # Apply dietary filter
    if dietary_type and dietary_type != 'All':
        recipes = recipes.filter(dietary_restrictions=dietary_type)

    # Get unique values for filters
    cuisine_types = Recipe.objects.values_list('cuisine_type', flat=True).distinct()
    dietary_types = Recipe.objects.values_list('dietary_restrictions', flat=True).distinct()

    context = {
        'recipes': recipes,
        'cuisine_types': cuisine_types,
        'dietary_types': dietary_types,
        'selected_cuisine': cuisine_type,
        'selected_dietary': dietary_type,
        'search_query': search_query,
    }
    return render(request, 'recipe_web/recipe_list.html', context)

@login_required
def recipe_create(request):
    CUISINE_CHOICES = [
        'Chinese', 'Indian', 'Italian', 'Japanese', 'Korean', 'Mexican', 'Thai',
        'Vietnamese', 'American', 'Mediterranean', 'Middle Eastern', 'French',
        'Spanish', 'Greek', 'Other'
    ]

    DIETARY_CHOICES = [
        'Vegetarian', 'Vegan', 'Gluten-Free', 'Dairy-Free', 'Nut-Free',
        'Low-Carb', 'Keto', 'Paleo', 'None'
    ]

    if request.method == 'POST':
        try:
            recipe = Recipe(
                title=request.POST['title'],
                description=request.POST['description'],
                ingredients=request.POST['ingredients'],
                instructions=request.POST['instructions'],
                cooking_time=request.POST['cooking_time'],
                cuisine_type=request.POST['cuisine_type'],
                dietary_restrictions=request.POST.get('dietary_restrictions', ''),
                author=request.user
            )
            
            if 'image' in request.FILES:
                recipe.image = request.FILES['image']
            
            recipe.save()
            messages.success(request, 'Recipe created successfully!')
            return redirect('recipe_detail', pk=recipe.pk)
            
        except Exception as e:
            messages.error(request, f'Error creating recipe: {str(e)}')
            return render(request, 'recipe_web/recipe_form.html', {
                'cuisine_types': CUISINE_CHOICES,
                'dietary_restrictions': DIETARY_CHOICES,
                'form_data': request.POST  # Keep the form data for re-population
            })

    context = {
        'cuisine_types': CUISINE_CHOICES,
        'dietary_restrictions': DIETARY_CHOICES
    }
    return render(request, 'recipe_web/recipe_form.html', context)

@login_required
def recipe_edit(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    
    # Check if user is the author
    if request.user != recipe.author:
        messages.error(request, "You don't have permission to edit this recipe.")
        return redirect('recipe_detail', pk=pk)

    CUISINE_CHOICES = [
        'Chinese', 'Indian', 'Italian', 'Japanese', 'Korean', 'Mexican', 'Thai',
        'Vietnamese', 'American', 'Mediterranean', 'Middle Eastern', 'French',
        'Spanish', 'Greek', 'Other'
    ]

    DIETARY_CHOICES = [
        'Vegetarian', 'Vegan', 'Gluten-Free', 'Dairy-Free', 'Nut-Free',
        'Low-Carb', 'Keto', 'Paleo', 'None'
    ]

    if request.method == 'POST':
        try:
            recipe.title = request.POST['title']
            recipe.description = request.POST['description']
            recipe.ingredients = request.POST['ingredients']
            recipe.instructions = request.POST['instructions']
            recipe.cooking_time = request.POST['cooking_time']
            recipe.cuisine_type = request.POST['cuisine_type']
            recipe.dietary_restrictions = request.POST.get('dietary_restrictions', '')

            if 'image' in request.FILES:
                recipe.image = request.FILES['image']

            recipe.save()
            messages.success(request, 'Recipe updated successfully!')
            return redirect('recipe_detail', pk=recipe.pk)

        except Exception as e:
            messages.error(request, f'Error updating recipe: {str(e)}')

    context = {
        'recipe': recipe,
        'cuisine_types': CUISINE_CHOICES,
        'dietary_restrictions': DIETARY_CHOICES
    }
    return render(request, 'recipe_web/recipe_form.html', context)

@login_required
def recipe_delete(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    
    # Check if user is the author
    if request.user != recipe.author:
        messages.error(request, "You don't have permission to delete this recipe.")
        return redirect('recipe_detail', pk=pk)

    if request.method == 'POST':
        try:
            recipe.delete()
            messages.success(request, 'Recipe deleted successfully!')
            return redirect('recipe_list')
        except Exception as e:
            messages.error(request, f'Error deleting recipe: {str(e)}')
            return redirect('recipe_detail', pk=pk)
    
    # For GET request, show the confirmation page
    return render(request, 'recipe_web/recipe_confirm_delete.html', {'recipe': recipe})

@login_required
def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    comments = Comment.objects.filter(recipe=recipe).order_by('-created_at')
    is_favorite = Favorite.objects.filter(user=request.user, recipe=recipe).exists() if request.user.is_authenticated else False
    
    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.recipe = recipe
            comment.user = request.user
            comment.save()
            return redirect('recipe_detail', pk=pk)
    else:
        comment_form = CommentForm()

    context = {
        'recipe': recipe,
        'comments': comments,
        'comment_form': comment_form,
        'is_favorite': is_favorite,
        'user': request.user,
    }
    return render(request, 'recipe_web/recipe_detail.html', context)

# Generic toggle function
def toggle_m2m_relationship(request, model, object_id, relationship_field):
    obj = get_object_or_404(model, pk=object_id)
    relationship = getattr(obj, relationship_field)
    
    if request.user in relationship.all():
        relationship.remove(request.user)
        added = False
    else:
        relationship.add(request.user)
        added = True
    
    return added

# Refactored toggle views
@login_required
@require_POST
def toggle_like(request, pk):
    added = toggle_m2m_relationship(request, Recipe, pk, 'likes')
    return redirect('recipe_detail', pk=pk)

@login_required
@require_POST
def toggle_favorite(request, pk):
    added = toggle_m2m_relationship(request, Recipe, pk, 'favorites')
    next_url = request.POST.get('next', '')
    return redirect(next_url) if next_url else redirect('recipe_detail', pk=pk)

@login_required
def user_profile(request, pk):
    profile_user = get_object_or_404(User, pk=pk)
    user_recipes = Recipe.objects.filter(author=profile_user).order_by('-created_at')
    favorite_recipes = Recipe.objects.filter(favorites=profile_user).order_by('-created_at')
    
    if request.method == 'POST':
        if 'profile_picture' in request.FILES:
            request.user.profile_picture = request.FILES['profile_picture']
        if 'bio' in request.POST:
            request.user.bio = request.POST['bio']
        request.user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('user_profile', pk=request.user.pk)

    context = {
        'profile_user': profile_user,
        'user_recipes': user_recipes,
        'favorite_recipes': favorite_recipes,
    }
    return render(request, 'recipe_web/user_profile.html', context)

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ('email',)

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
@require_POST
def add_comment(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.recipe = recipe
            comment.user = request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')
    return redirect('recipe_detail', pk=pk)

@login_required
@require_POST
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk, user=request.user)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Comment updated successfully!')
    return redirect('recipe_detail', pk=comment.recipe.pk)

@login_required
@require_POST
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk, user=request.user)
    recipe_pk = comment.recipe.pk
    comment.delete()
    messages.success(request, 'Comment deleted successfully!')
    return redirect('recipe_detail', pk=recipe_pk)

@login_required
@require_POST
def toggle_follow(request, pk):
    user_to_follow = get_object_or_404(User, pk=pk)
    next_url = request.POST.get('next', '')
    
    if request.user.is_following(user_to_follow):
        request.user.unfollow(user_to_follow)
        messages.success(request, f'You unfollowed {user_to_follow.username}')
    else:
        request.user.follow(user_to_follow)
        messages.success(request, f'You are now following {user_to_follow.username}')
    
    return redirect(next_url) if next_url else redirect('user_profile', pk=user_to_follow.pk)

@login_required
def followers_list(request, pk):
    user = get_object_or_404(User, pk=pk)
    followers = user.followers.all()
    return render(request, 'recipe_web/followers.html', {
        'profile_user': user,
        'followers': followers
    })

@login_required
def following_list(request, pk):
    user = get_object_or_404(User, pk=pk)
    following = user.following.all()
    return render(request, 'recipe_web/following.html', {
        'profile_user': user,
        'following': following
    })

@login_required
def feed(request):
    following_users = request.user.following.all()
    feed_recipes = Recipe.objects.filter(user__in=following_users).order_by('-created_at')
    return render(request, 'recipe_web/feed.html', {'recipes': feed_recipes}) 
    