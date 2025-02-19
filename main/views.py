from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Product, Diamond, Gold, Silver, MetalRate,Admin
from django.db import connection
from django.http import JsonResponse
from django.http import HttpResponse
from django.db import transaction
from django.db.models import Q
import os
from django.conf import settings
from django.utils.timezone import now, localtime
import base64


def admin(request):
    auth_token=request.COOKIES.get('auth_token')
    if auth_token is not None:
        return render(request, 'admin.html')
    else:
        return redirect('/login')

def login(request):
    if request.method=='POST':
        email=request.POST.get("email")
        password=request.POST.get("password")
        adminDetails=Admin.objects.filter(email=email,password=password)
        if len(adminDetails)==1:
            response=redirect("/admin/")
            token=base64.b64encode(email.encode('utf-8'))
            response.set_cookie(
                'auth_token',token,max_age=60000,secure=True,httponly=True,samesite='strict'
            )
            return response
        else:
            return redirect("/login")
    else:
        return render(request,"Login.html")

def logout(request):
    auth_token=request.COOKIES.get('auth_token')
    if auth_token is not None:
        response=redirect("/login")
        response.delete_cookie('auth_token')
        return response
    else:
        return redirect('/login')


def add_product(request):
    auth_token=request.COOKIES.get('auth_token')
    if auth_token is not None:
        if request.method == 'POST':
            # Retrieve common fields
            product_name = request.POST.get('product_name')
            category = request.POST.get('category')

            image1 = request.FILES.get('image1')  # Get first image
            image2 = request.FILES.get('image2')  # Get second image
            image3 = request.FILES.get('image3')  # Get third image

            # Save images to Product model
            product = Product.objects.create(
                product_name=product_name,
                category=category,
                product_picture1=image1,
                product_picture2=image2,
                product_picture3=image3,
            )

            # Save product to get its ID
            product.save()
        
            # Handle category-specific fields
            if category == 'diamond':
                Diamond.objects.create(
                    product=product,
                    diamond_id=request.POST.get('Diamond-Id'),
                    diamond_shape=request.POST.get('diamond_shape'),
                    diamond_type=request.POST.get('diamond_type'),
                    diamond_color=request.POST.get('diamond_color'),
                    diamond_carat=float(request.POST.get('diamond_carat')),
                    diamond_quantity=request.POST.get('diamond_quantity'),
                    description=request.POST.get('diamond_description'),
                    diamond_mrp=request.POST.get('diamond_mrp'),
                    tax=request.POST.get('tax'),
                )
            elif category == 'gold':
                Gold.objects.create(
                    product=product,
                    gold_id=request.POST.get('Gold_p_id'),
                    gold_category=request.POST.get('gold_category'),
                    weight=float(request.POST.get('product_weight')),
                    carat=request.POST.get('gold_carat'),
                    labour_percentage=request.POST.get('gold_labour'),
                    gold_quantity=request.POST.get('gold_quantity'),
                    description=request.POST.get('gold_description'),
                    diamond_weight_in_gold=float(request.POST.get('diamond_weight')),
                    diamond_rate_in_gold=request.POST.get('diamond_rate_gold'),
                    other_charges=request.POST.get('other_charges'),
                    tax=request.POST.get('tax'),
                    gold_mrp=request.POST.get('gold_mrp'),
                    bangle_size=request.POST.get('bangles_size'),
                    ring_bracelet_size=request.POST.get('ring_bracelet_size'),
                )
            elif category == 'silver':
                Silver.objects.create(
                    product=product,
                    silver_id=request.POST.get('Silver_p_id'),
                    silver_category=request.POST.get('silver_category'),
                    weight=float(request.POST.get('silver_weight')),
                    silver_quantity=request.POST.get('silver_quantity'),
                    diamond_weight_in_silver=float(request.POST.get('diamond_weight_silver')),
                    diamond_rate_in_silver=request.POST.get('diamond_rate'),
                    description=request.POST.get('silver_description'),
                    tax=request.POST.get('tax'),    
                    silver_mrp=request.POST.get('silver_mrp'),
                    bangle_size=request.POST.get('silver_bangles_size'),
                    ring_bracelet_size=request.POST.get('silver_ring_bracelet_size'),
                )

            product.save()
            messages.success(request, 'Product added successfully!')
            return redirect('add_product')

        else:
            return render(request, 'add_product.html')
    else:
        return redirect('/login')

def delete_product(request):
    auth_token=request.COOKIES.get('auth_token')
    if auth_token is not None: 
        if request.method == "POST":
            product_id = request.POST.get("product_id")

            try:
                # Get the product using the ID
                product = get_object_or_404(Product, id=product_id)
                
                if product.product_picture1:
                    image1_path = os.path.join(settings.MEDIA_ROOT, str(product.product_picture1))
                    if os.path.exists(image1_path):
                        os.remove(image1_path)

                if product.product_picture2:
                    image2_path = os.path.join(settings.MEDIA_ROOT, str(product.product_picture2))
                    if os.path.exists(image2_path):
                        os.remove(image2_path)

                if product.product_picture3:
                    image3_path = os.path.join(settings.MEDIA_ROOT, str(product.product_picture3))
                    if os.path.exists(image3_path):
                        os.remove(image3_path)
                    
                # Check the category and delete related data
                if product.category == 'diamond':
                    Diamond.objects.filter(product=product).delete()
                elif product.category == 'gold':
                    Gold.objects.filter(product=product).delete()
                elif product.category == 'silver':
                    Silver.objects.filter(product=product).delete()

                # Delete the product itself
                messages.success(request, f"Product ID : {product.id} deleted successfully!")
                product.delete()

            except Exception as e:
                 return redirect('/error/')  

        return render(request, "delete_product.html")
    else:
        return redirect('/login')


def view_product(request):
    auth_token=request.COOKIES.get('auth_token')
    if auth_token is not None: 
        # Fetch all products initially
        products = Product.objects.all()

        # Get the selected category and search query from the GET request
        category_filter = request.POST.get('category', '').strip()
        search_query = request.POST.get('search', '').strip()

        # Apply category filter only if a specific category is selected (not "All" or empty)
        if category_filter and category_filter.lower() != 'all':
            products = products.filter(category=category_filter)

        # Apply search filter if a search query is provided
        if search_query:
            products = products.filter(
                Q(id__icontains=search_query) |
                Q(product_name__icontains=search_query)
            )
            
        context = {
            'products': products,
            'selected_category': category_filter,
            'search_query': search_query,
        }
        return render(request, 'view_product.html', context)
    else:
        return redirect('/login')

def update_rates(request):
    auth_token=request.COOKIES.get('auth_token')
    if auth_token is not None: 
        if request.method == "POST":
            # Get the rates from the form
            gold_rate = float(request.POST.get("gold_rate", 0))
            silver_rate = float(request.POST.get("silver_rate", 0))

            current_time = localtime().time()

            # Save the rates to MetalRate table with the current date
            if gold_rate > 0 or silver_rate > 0:
                MetalRate.objects.create(
                    date=localtime().date(),
                    time=current_time,
                    gold_rate=gold_rate if gold_rate > 0 else None,
                    silver_rate=silver_rate if silver_rate > 0 else None,
                )

            # Update Gold Table MRPs
            if gold_rate > 0:
                gold_items = Gold.objects.all()
                for gold in gold_items:
                    gold.gold_mrp = (
                        (((gold.weight - gold.diamond_weight_in_gold) * gold.carat * gold_rate) / 100
                        + ((gold_rate * gold.labour_percentage) / 100) + gold.diamond_rate_in_gold + gold.other_charges)
                    )
                    gold.save()

            # Update Silver Table MRPs (Uncomment if needed)
            if silver_rate > 0:
                silver_items = Silver.objects.all()
                for silver in silver_items:
                    silver.silver_mrp = ((gold.weight - gold.diamond_weight_in_gold) * silver_rate / 1000 + silver.diamond_rate_in_silver)
                    silver.save()

            # Add a success message
            messages.success(request, "Gold and Silver rates updated successfully!")

            # Redirect to the admin dashboard or any relevant page
            return redirect("/admin")

        # If GET request, render the form page
        return render(request, "admin.html")
    else:
        return redirect('/login')

def toggle_product_status(request, product_id):
    try:
        if request.method == 'POST':
            product = get_object_or_404(Product, id=product_id)
            product.status = not product.status  # Toggle status
            product.save()

        return redirect(request.META.get('HTTP_REFERER', 'view_products'))
    
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('/error/')


def update_product(request):
    auth_token=request.COOKIES.get('auth_token')
    if auth_token is not None: 
        try:
            product = None
            diamond = None
            gold = None
            silver = None

            if request.method == 'POST':
                product_id = request.POST.get('product_id')
                if product_id:
                    product = get_object_or_404(Product, id=product_id)

                    if product.category == 'diamond':
                        diamond = get_object_or_404(Diamond, product=product)
                    elif product.category == 'gold':
                        gold = get_object_or_404(Gold, product=product)
                    elif product.category == 'silver':
                        silver = get_object_or_404(Silver, product=product)

            return render(request, 'update_product.html', {
                'product': product,
                'diamond': diamond,
                'gold': gold,
                'silver': silver,
                'fetch_product': True
            })
        
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('error')
    else:
        return redirect('/login')

def save_updated_data(request):
    # Handling the second form to update product details
    if request.method=='POST':
        product_id = request.POST.get('product_id')
        if product_id:
            # Get the product instance again
            product = get_object_or_404(Product, id=product_id)
            product.product_name = request.POST.get('product_name', product.product_name)
            product.category = request.POST.get('category', product.category)
            if 'image1' in request.FILES:
                if product.product_picture1:
                    image1_path = os.path.join(settings.MEDIA_ROOT, str(product.product_picture1))
                    if os.path.exists(image1_path):
                        os.remove(image1_path)
                product.product_picture1 = request.FILES['image1']
            if 'image2' in request.FILES:
                if product.product_picture2:
                    image2_path = os.path.join(settings.MEDIA_ROOT, str(product.product_picture2))
                    if os.path.exists(image2_path):
                        os.remove(image2_path)

                product.product_picture2 = request.FILES['image2']
            if 'image3' in request.FILES:
                if product.product_picture3:
                    image3_path = os.path.join(settings.MEDIA_ROOT, str(product.product_picture3))
                    if os.path.exists(image3_path):
                        os.remove(image3_path)
                product.product_picture3 = request.FILES['image3']
            product.save()


            # Depending on the category, update the respective product details
            if product.category == 'diamond':
                diamond = get_object_or_404(Diamond, product=product)
                diamond.diamond_id=request.POST.get('Diamond-Id')
                diamond.diamond_shape=request.POST.get('diamond_shape')
                diamond.diamond_type=request.POST.get('diamond_type')
                diamond.diamond_color=request.POST.get('diamond_color')
                diamond.diamond_carat=float(request.POST.get('diamond_carat'))
                diamond.diamond_quantity=request.POST.get('diamond_quantity')
                diamond.description=request.POST.get('diamond_description')
                diamond.tax=request.POST.get('tax')
                diamond.diamond_mrp=float(request.POST.get('diamond_mrp'))
                diamond.save()
                

            elif product.category == 'gold':
                gold = get_object_or_404(Gold, product=product)
                gold.gold_id = request.POST.get('Gold_p_id')
                gold.gold_category = request.POST.get('gold_category')
                gold.weight = request.POST.get('gold_weight')
                gold.carat = request.POST.get('gold_carat')
                gold.labour_percentage = request.POST.get('gold_labour')
                gold.gold_quantity=request.POST.get('gold_quantity')
                gold.description = request.POST.get('gold_description')
                gold.diamond_weight_in_gold = request.POST.get('diamond_weight')
                gold.diamond_rate_in_gold = request.POST.get('diamond_rate_gold')
                gold.other_charges = request.POST.get('other_charges')
                gold.gold_mrp = request.POST.get('gold_mrp')
                gold.bangle_size = request.POST.get('bangles_size')
                gold.ring_bracelet_size = request.POST.get('ring_bracelet_size')
                gold.save()

            elif product.category == 'silver':
                silver = get_object_or_404(Silver, product=product)
                silver.silver_id = request.POST.get('Silver_p_id')
                silver.silver_category = request.POST.get('silver_category')
                silver.weight = request.POST.get('silver_weight')
                silver.silver_quantity=request.POST.get('silver_quantity')
                silver.diamond_weight_in_silver = request.POST.get('diamond_weight_silver')
                silver.diamond_rate_in_silver = request.POST.get('diamond_rate')
                silver.description = request.POST.get('silver_description')
                silver.silver_mrp = request.POST.get('silver_mrp')
                silver.bangle_size = request.POST.get('silver_bangles_size')
                silver.ring_bracelet_size = request.POST.get('silver_ring_bracelet_size')
                silver.save()
        messages.success(request, f"Product ID : {product.id} updated successfully!")       
        return redirect('/update_product/')

    return render(request, 'update_product.html', {
        'product': product,
        'diamond': diamond,
        'gold': gold,
        'silver': silver,
        'fetch_product': False,  # This indicates that the product hasn't been fetched yet
    })

def error(request):
    return render(request, "error.html")