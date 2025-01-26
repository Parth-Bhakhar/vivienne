from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Product, Diamond, Gold, Silver
from django.db import connection
from django.http import JsonResponse
from django.http import HttpResponse
from django.db import transaction
from django.db.models import Q



def admin(request):
    return render(request, 'admin.html')


def add_product(request):
    if request.method == 'POST':
        # Retrieve common fields
        product_name = request.POST.get('product_name')
        category = request.POST.get('category')

        # Create a product instance
        product = Product(product_name=product_name, category=category)

        # Save product to get its ID
        product.save()

        # Handle category-specific fields
        if category == 'diamond':
            Diamond.objects.create(
                product=product,
                diamond_id=request.POST.get('Diamond-Id'),
                product_name = request.POST.get('product_name'),
                diamond_shape=request.POST.get('diamond_shape'),
                diamond_type=request.POST.get('diamond_type'),
                diamond_color=request.POST.get('diamond_color'),
                diamond_carat=request.POST.get('diamond_carat'),
                diamond_mrp=request.POST.get('diamond_mrp'),
            )
        elif category == 'gold':
            Gold.objects.create(
                product=product,
                gold_id=request.POST.get('Gold_p_id'),
                gold_category=request.POST.get('gold_category'),
                weight=request.POST.get('product_weight'),
                carat=request.POST.get('gold_carat'),
                labour_percentage=request.POST.get('gold_labour'),
                description=request.POST.get('gold_description'),
                diamond_weight_in_gold=request.POST.get('diamond_weight'),
                gold_mrp=request.POST.get('gold_mrp'),
                bangle_size=request.POST.get('bangles_size'),
                ring_bracelet_size=request.POST.get('ring_bracelet_size'),
            )
        elif category == 'silver':
            Silver.objects.create(
                product=product,
                silver_id=request.POST.get('Silver_p_id'),
                silver_category=request.POST.get('silver_category'),
                weight=request.POST.get('silver_weight'),
                silver_mrp=request.POST.get('silver_mrp'),
                bangle_size=request.POST.get('silver_bangles_size'),
                ring_bracelet_size=request.POST.get('silver_ring_bracelet_size'),
            )

        # Handle image uploads
        for i in range(1, 4):
            image = request.FILES.get(f'product_picture{i}')
            if image:
                setattr(product, f'product_picture{i}', image)

        # Save images
        product.save()

        messages.success(request, 'Product added successfully!')
        return redirect('add_product')

    return render(request, 'add_product.html')


def delete_product(request):
    if request.method == "POST":
        product_id = request.POST.get("product-id-delete")

        try:
            # Get the product using the ID
            product = get_object_or_404(Product, id=product_id)

            # Check the category and delete related data
            if product.category == 'diamond':
                Diamond.objects.filter(product=product).delete()
            elif product.category == 'gold':
                Gold.objects.filter(product=product).delete()
            elif product.category == 'silver':
                Silver.objects.filter(product=product).delete()

            # Delete the product itself
            product.delete()

        except Exception as e:
            return HttpResponse(f"An error occurred: {str(e)}")

    return render(request, "delete_product.html")
 

def update_product(request):
    return render(request, 'update_product.html')


def view_product(request):
    # Fetch all products initially
    products = Product.objects.all()

    # Get the selected category and search query from the GET request
    category_filter = request.POST.get('category')
    search_query = request.POST.get('search')

    # If a category is selected and search query is None or empty, filter only by category
    if category_filter and (search_query or search_query == ''):
        products = products.filter(category=category_filter)
    
    # If a search query is provided, filter by both category and search query
    elif search_query and search_query != '':
        products = products.filter(
            Q(id__icontains=search_query) |
            Q(product_name__icontains=search_query)
        )

    # If both category and search query are provided, filter by both
    if category_filter and search_query and search_query != 'None':
        products = products.filter(category=category_filter).filter(
            Q(id__icontains=search_query) |
            Q(product_name__icontains=search_query)
        )

    # Prepare context for the template
    context = {
        'products': products,
        'selected_category': category_filter,
        'search_query': search_query,
    }
    return render(request, 'view_product.html', context)


def update_rates(request):
    if request.method == "POST":
        gold_rate = float(request.POST.get("gold_rate", 0))
        silver_rate = float(request.POST.get("silver_rate", 0))

        # Update Gold Table MRPs
        if gold_rate > 0:
            gold_items = Gold.objects.all()
            for gold in gold_items:
                gold.gold_mrp = gold.weight * gold_rate + (gold.weight * gold_rate * gold.labour_percentage / 100)
                gold.save()

        # Update Silver Table MRPs
        if silver_rate > 0:
            silver_items = Silver.objects.all()
            for silver in silver_items:
                silver.silver_mrp = silver.weight * silver_rate
                silver.save()

        messages.success(request, "Gold and Silver rates updated successfully!")
        return redirect("/admin")  # Redirect back to the admin dashboard

    return render(request, "admin.html")