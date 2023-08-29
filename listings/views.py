from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q

from .models import Category, Product, Review, Color, Season
from .forms import ReviewForm
from cart.forms import CartAddProductForm


categories = Category.objects.all()


def product_list(request, category_slug=None):
    if request.GET != None:
        query_seasons = None
        query_brands = None
        query_colors = None
        print(request.GET)
        if request.GET.get('season'):
            query_seasons = dict(request.GET)['season']
        if request.GET.get('brand'):
            query_brands = dict(request.GET)['brand']
        if request.GET.get('color'):
            query_colors = dict(request.GET)['color']

        seasons = Season.objects.all()
        brands = list(set([i.brand for i in Product.objects.all()]))
        colors = Color.objects.all()

        products = Product.objects.all()
        if query_seasons:
            products = products.filter(seasons__in=query_seasons)
        else:
            query_seasons = None

        if query_brands:
            products = products.filter(brand__in=query_brands)
        else:
            query_brands = None

        if query_colors:
            products = products.filter(color__in=query_colors)
        else:
            query_colors = None

    if category_slug:
        requested_category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=requested_category)
        if query_seasons:
            products = products.filter(category=requested_category, seasons__in=query_seasons)
        else:
            query_seasons = None

        if query_brands:
            products = products.filter(category=requested_category, brand__in=query_brands)
        else:
            query_brands = None

        if query_colors:
            products = products.filter(category=requested_category, color__in=query_colors)
        else:
            query_colors = None
    else:
        requested_category = None
        # products = Product.objects.all()

    context = {
        'categories': categories,
        'products': products,
        'colors': colors,
        'requested_category': requested_category,
        'seasons': seasons,
        'brands': brands
    }
    return render(request, 'product/list.html', context)


def product_detail(request, category_slug, product_slug):
    category = get_object_or_404(Category, slug=category_slug)
    product = get_object_or_404(
        Product, category_id=category.id, slug=product_slug)
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            cf = review_form.cleaned_data
            author_name = "Анонимный"
            if request.user.is_authenticated and request.user.first_name != '':
                author_name = request.user.first_name + " " + request.user.last_name
            Review.objects.create(
                product=product,
                author=author_name,
                rating=cf['rating'],
                text=cf['text']
            )
        return redirect('listings:product_detail', category_slug=category_slug, product_slug=product_slug)
    else:
        review_form = ReviewForm()
        cart_product_form = CartAddProductForm()
        context = {
            'product': product,
            'review_form': review_form,
            "cart_product_form": cart_product_form,
        }
    return render(request, 'product/detail.html', context)


def search_list(request):
    if request.method == 'POST':
        if 'keywords' in request.POST:
            keywords = request.POST['keywords']
            if keywords:
                products = Product.objects.filter(
                    Q(name__icontains=keywords) |
                    Q(description__icontains=keywords) |
                    Q(price__icontains=keywords) |
                    Q(category__name__icontains=keywords) |
                    Q(top_height__icontains=keywords) |
                    Q(articul__iexact=keywords) |
                    Q(brand__icontains=keywords)
                )
        context = {
            "products": products,
            'categories': categories
        }
        return render(request, 'product/search.html', context)
    else:
        return render(request, 'product/list.html')
