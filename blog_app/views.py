from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product, Comment, Color, Favorite, Storage
from django.http import HttpResponse
from .forms import LoginForm, RegisterForm, CommentForm, ColorForm, ProductForm, FavoriteForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.generic import UpdateView, DeleteView, ListView
import json

# Create your views here.


def home(request):
    product = Product.objects.all()
    category_line = Category.objects.all()[:3]
    context = {
        'product': product,
        'category_line': category_line
    }
    return render(request, 'blog_app/index.html', context)


def faq(request):
    return render(request, 'blog_app/faq.html')


def storage(request):
    storage_user = Storage.objects.filter(user=request.user)
    context = {
        'storage': storage_user
    }
    return render(request, 'blog_app/storage.html', context)


def all_categories(request):
    product = Product.objects.all()
    query = request.GET.get('sort', '')
    if query:
        product = product.order_by(query)

    context = {
        'product': product,
        'category_title': 'Все категории',
    }
    return render(request, 'blog_app/categories.html', context)


def category_view(request, slug):
    category = Category.objects.get(slug=slug)
    product = Product.objects.filter(category=category)
    query = request.GET.get('sort', '')
    if query:
        product = product.order_by(query)

    context = {
        'category': category,
        'category_title': category.title,
        'product': product,
    }

    return render(request, 'blog_app/categories.html', context)


def product_detail(request, pk):
    product_1 = Product.objects.filter(pk=pk)
    product = get_object_or_404(Product, pk=pk)
    color = Color.objects.filter(product_parent=product)
    comments = Comment.objects.filter(product=product)[:3]
    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.product = product
            form.author = request.user
            form.save()
            return redirect('detail', pk=pk)
    else:
        form = CommentForm()

    context = {
        'product1': product_1,
        'color': color,
        'comments': comments,
        'form': form,
        'product': product,
    }
    return render(request, 'blog_app/detail.html', context)


def color_detail(request, pk):
    color = Color.objects.filter(pk=pk)
    for color in color:
        color = color
    product = get_object_or_404(Product, pk=color.product_parent.pk)
    color_all = Color.objects.filter(product_parent=product)
    comments = Comment.objects.filter(product=product)[:3]
    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.product = product
            form.author = request.user
            form.save()
            return redirect('detail', pk=pk)
    else:
        form = CommentForm()

    context = {
        'color_all': color_all,
        'color': color,
        'comments': comments,
        'form': form,
        'product': product,
    }
    return render(request, 'blog_app/detail_color.html', context)


def create_color(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ColorForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.product_parent = product
            form.save()
            return redirect('detail', pk=pk)
    else:
        form = ColorForm()
    context = {
        'form': form
    }
    return render(request, 'blog_app/create_color.html', context)


def feedback_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    comments = Comment.objects.filter(product=product)
    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.product = product
            form.author = request.user
            form.save()
            return redirect('feedback', pk=pk)
    else:
        form = CommentForm()
    context = {
        'comments': comments,
        'form': form,
        'product': product,
    }
    return render(request, 'blog_app/feedback.html', context)


def registration_view(request):
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm

    context = {
        'form': form
    }
    return render(request, 'blog_app/registration.html', context)


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm

    context = {
        'form': form
    }
    return render(request, 'blog_app/login.html', context)


def user_logout(request):
    logout(request)
    return redirect('home')


def profile(request, username):
    shopping = []
    user_obj = User.objects.get(username=username)
    product = Product.objects.filter(producer=user_obj)
    total_comments = sum([i.comments.all().count() for i in product])
    for el in product:
        shopping.append(el.shopping)
        try:
            color = Color.objects.get(product_parent=el)
            if color:
                shopping.append(color.shopping)
        except Exception:
            color = 0
            shopping.append(color)
    print(shopping)
    shopping = sum(shopping)
    print(shopping)
    context = {
        'shopping': shopping,
        'user_obj': user_obj,
        'product': product,
        'total_product': product.count(),
        'total_comments': total_comments
    }
    return render(request, 'blog_app/profile.html', context)


def create_product(request):
    if request.method == 'POST':
        form = ProductForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.producer = request.user
            form.save()
            return redirect('home')
    else:
        form = ProductForm()
    context = {
        'form': form
    }
    return render(request, 'blog_app/create_product.html', context)


class ProductDelete(DeleteView):
    model = Product
    template_name = 'blog_app/product_confirm_delete.html'
    success_url = '/'


class ColorDelete(DeleteView):
    model = Color
    template_name = 'blog_app/color_confirm_delete.html'
    success_url = '/'


class ProductUpdate(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'blog_app/create_product.html'
    success_url = '/'


class ColorUpdate(UpdateView):
    model = Color
    form_class = ColorForm
    template_name = 'blog_app/create_color.html'
    success_url = '/'


def search(request):
    query = request.GET.get('q')
    product = Product.objects.filter(title__iregex=query)
    context = {
        'product': product
    }
    return render(request, 'blog_app/index.html', context)


def favorite(request, pk):
    if Favorite.objects.filter(user=request.user):
        favorite_create = Favorite.objects.get(user=request.user)
        deserialized_list = favorite_create.product
        try:
            deserialized_list.append(pk)
        except Exception:
            deserialized_list = json.loads(favorite_create.product)
            deserialized_list.append(pk)
        favorite_create.product = deserialized_list
        favorite_create.save(update_fields=['product'])
    else:
        favorite_create = Favorite.objects.create(user=request.user, product=json.dumps([pk]))
        favorite_create.save()
    return redirect(request.META['HTTP_REFERER'])


def remove_favorite(request, pk):
    favorites = Favorite.objects.get(user=request.user)
    deserialized_list = favorites.product
    deserialized_list.remove(pk)
    favorites.product = deserialized_list
    favorites.save(update_fields=['product'])
    return redirect(request.META['HTTP_REFERER'])


def favorites_view(request):
    product_list = []
    try:
        favorites = Favorite.objects.get(user=request.user).product
        for pk in favorites:
            product = Product.objects.get(pk=pk)
            product_list.append(product)
        context = {
            'product': product_list,
            'category_title': 'Избранное',
        }
        return render(request, 'blog_app/favorite.html', context)
    except Exception:
        context = {
            'product': product_list,
            'category_title': 'Избранное',
        }
        return render(request, 'blog_app/favorite.html', context)


def storage_add(request, pk):
    product = Product.objects.get(pk=pk)
    storage_product = Storage.objects.filter(user=request.user, product=product)
    print(storage_product)
    if storage_product:
      storage_product = storage_product.first()
      print(storage_product)
      if storage_product:
          storage_product.quantity += 1
          storage_product.save()
          product.quantity -= 1
          product.save(update_fields=['quantity'])
    else:
        storage_product.create(user=request.user, product=product, quantity=1)
        product.quantity -= 1
        product.save(update_fields=['quantity'])

    return redirect(request.META['HTTP_REFERER'])


def storage_add_color(request, pk):
    color = Color.objects.get(pk=pk)
    storage_product = Storage.objects.filter(user=request.user, product_color=color)

    if storage_product:
      storage_product = storage_product.first()
      if storage_product:
          storage_product.quantity += 1
          storage_product.save(update_fields=['quantity'])
          color.quantity -= 1
          color.save(update_fields=['quantity'])
    else:
        storage_product.create(user=request.user, product_color=color, quantity=1)
        color.quantity -= 1
        color.save(update_fields=['quantity'])

    return redirect(request.META['HTTP_REFERER'])


def storage_delete(request):
    storage_all = Storage.objects.filter(user=request.user)
    for i in storage_all:
        if i.product:
            product = Product.objects.get(pk=i.product.pk)
            product.quantity += i.quantity
            product.save(update_fields=['quantity'])
        else:
            product = Color.objects.get(pk=i.product_color.pk)
            product.quantity += i.quantity
            product.save(update_fields=['quantity'])
    storage_all.delete()
    return redirect('storage')


def storage_product_plus(request, pk):
    product = Product.objects.get(pk=pk)
    storage_product = Storage.objects.get(product=product, user=request.user)
    if product.quantity != 0:
        product.quantity -= 1
        product.save(update_fields=['quantity'])
        storage_product.quantity += 1
        storage_product.save(update_fields=['quantity'])
        return redirect('storage')
    return redirect('storage')


def storage_product_minus(request, pk):
    product = Product.objects.get(pk=pk)
    storage_product = Storage.objects.get(product=product, user=request.user)
    if storage_product.quantity <= 1:
        storage_product.delete()
    else:
        product.quantity += 1
        product.save(update_fields=['quantity'])
        storage_product.quantity -= 1
        storage_product.save(update_fields=['quantity'])
        return redirect('storage')
    return redirect('storage')


def storage_product_color_plus(request, pk):
    product = Color.objects.get(pk=pk)
    storage_product = Storage.objects.get(product_color=product, user=request.user)
    if product.quantity != 0:
        product.quantity -= 1
        product.save(update_fields=['quantity'])
        storage_product.quantity += 1
        storage_product.save(update_fields=['quantity'])
        return redirect('storage')
    return redirect('storage')


def storage_product_color_minus(request, pk):
    product = Color.objects.get(pk=pk)
    storage_product = Storage.objects.get(product_color=product, user=request.user)
    if storage_product.quantity == 0:
        storage_product.delete()
    else:
        product.quantity += 1
        product.save(update_fields=['quantity'])
        storage_product.quantity -= 1
        storage_product.save(update_fields=['quantity'])
        return redirect('storage')
    return redirect('storage')


def storage_product_trash(request, pk):
    product = Product.objects.get(pk=pk)
    storage_product = Storage.objects.get(user=request.user, product=product)
    product.quantity += storage_product.quantity
    product.save(update_fields=['quantity'])
    storage_product.delete()
    return redirect('storage')


def storage_color_trash(request, pk):
    product = Color.objects.get(pk=pk)
    storage_product = Storage.objects.get(user=request.user, product_color=product)
    product.quantity += storage_product.quantity
    product.save(update_fields=['quantity'])
    storage_product.delete()
    return redirect('storage')


def buy(request):
    storage_user = Storage.objects.filter(user=request.user)
    for i in storage_user:
        if i.product:
            i.product.shopping += i.quantity
            i.product.save(update_fields=['shopping'])
            i.delete()
        elif i.product_color:
            i.product_color.shopping += i.quantity
            i.product_color.save(update_fields=['shopping'])
            i.delete()
    return redirect('storage')


def comment_delete(request, pk):
    comment = Comment.objects.get(pk=pk)
    comment.delete()
    return redirect(request.META['HTTP_REFERER'])
