

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views import View

from django.contrib.auth.models import User
from zuzas_store.models import UserProfile, Category, Product, Property
from cart.forms import CartAddProductForm


class MainPage(View):

    def get(self, request):
        return render(request, 'main_page.html')





class CreateUser(View):

    def get(self, request):
        return render(request, 'create_user.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmpassword')
        phone_number = request.POST.get('phone_number')
        if not username or not password or password != confirm_password:
            ctx = {"text": "Uzupełnij pola"}
            return render(request, 'create_user.html', ctx)

        else:
            user = User.objects.create_user(username=username, email=None, password=password, )
            UserProfile.objects.create(user=user, phone_number=phone_number)
        return render(request, 'create_user.html', context={'username': username, 'password': password})


class LoginUser(View):
    def get(self, request):
        return render(request, 'registration/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("main_page")
        else:
            return redirect('create_user.html')





class CategoriesList(View):

    def get(self, request):

        categories = list(Category.objects.all())

        return render(request, "categories.html", context={'categories': categories})


class ProductList(View):
    def get(self, request, cat_id):
        products = list(Product.objects.filter(category=cat_id))
        category_name = Category.objects.get(id=cat_id)
        # for product in products:
        #     images_prod = list(product.images.all())
        #     print(images_prod)
        #     image_pict = images_prod[0].image
        return render(request, 'products.html', context={'products': products,
                                                             'category_name': category_name})


class ProductCard(View):
    def get(self, request, prod_id):
        product = Product.objects.get(id=prod_id)
        images = list(product.images.all())
        properties = Property.objects.get(product=prod_id)
        return render(request, 'product.html', {'product': product, 'images': images, 'properties': properties})

    def post(self, request, prod_id):
        product = Product.objects.get(id=prod_id)
        cart_product_form = CartAddProductForm()
        if product.quantity < cart_product_form:
            text = f"Błąd : Ilość niedostepna !"
            return render(request, 'product.htm', context={'text': text})
        else:
            return render(request, 'product.html', {'qproduct': product, 'cart_product_form': cart_product_form})

