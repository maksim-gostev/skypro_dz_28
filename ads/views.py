import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from ads.models import Category, Ad
from users.models import User


def index(request):
    return JsonResponse({"status": "ok"}, status=200)


class CategoriesListView(ListView):
    model = Category

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object_list = self.object_list.order_by('name')
        respons = []

        for category in self.object_list:
            respons.append({
                'id': category.id,
                'name': category.name
            })

        return JsonResponse(respons, safe=False)


class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        category = self.get_object()

        return JsonResponse({
            "id": category.id,
            "name": category.name,
        })


@method_decorator(csrf_exempt, name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    fields = ["name"]

    def post(self, request, *args, **kwargs):
        category_data = json.loads(request.body)

        category = Category.objects.create(
            name=category_data["name"],
        )

        return JsonResponse({
            "id": category.id,
            "name": category.name,
        })


@method_decorator(csrf_exempt, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Category
    fields = ["name"]

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        category_data = json.loads(request.body)

        self.object.name = category_data["name"]

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
        })


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


class AdListView(ListView):
    model = Ad

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object_list = self.object_list.select_related('author_id').order_by('-price')

        response = []
        for ad in self.object_list:
            response.append({
                "id": ad.id,
                'name': ad.name,
                'author_id': ad.author_id.username,
                'price': ad.price,
                'description': ad.description,
                'is_published': ad.is_published,
                'image': ad.image.url if ad.image else None,
                'category_id': ad.category_id.name,
            })

        return JsonResponse(response, safe=False)


class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        ad = self.get_object()

        return JsonResponse({
            "id": ad.id,
            'name': ad.name,
            'author_id': ad.author_id.username,
            'price': ad.price,
            'description': ad.description,
            'is_published': ad.is_published,
            'image': ad.image.url if ad.image else None,
            'category_id': ad.category_id.name
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdCreateView(CreateView):
    model = Ad
    fields = ['name', 'author_id', 'price', 'description', 'is_published', 'image', 'category_id']

    def post(self, request, *args, **kwargs):
        ad_data = json.loads(request.body)

        try:
            user_obj = User.objects.get(id=ad_data['author_id'])
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)


        category_obj, _ =Category.objects.get_or_create(name=ad_data['category'])


        ad = Ad.objects.create(
            name=ad_data['name'],
            author_id=user_obj,
            price=ad_data['price'],
            description=ad_data['description'],
            is_published=ad_data['is_published'],
            image=ad_data['image'],
            category_id=category_obj
        )

        return JsonResponse({
            "id": ad.id,
            'name': ad.name,
            'author_id': ad.author_id.username,
            'author': ad.author_id.id ,
            'price': ad.price,
            'description': ad.description,
            'is_published': ad.is_published,
            'image': ad.image.url if ad.image else None,
            'category': ad.category_id.name
        })

@method_decorator(csrf_exempt, name='dispatch')
class AdUpdateView(UpdateView):
    model = Ad
    fields = ['name', 'author_id', 'price', 'description', 'is_published', 'image', 'category_id']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        ad_data = json.loads(request.body)

        try:
            user_obj = User.objects.get(id=ad_data['author_id'])
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

        category_obj, _ = Category.objects.get_or_create(name=ad_data['category'])

        self.object.name = ad_data.get("name")
        self.object.author_id = user_obj
        self.object.price = ad_data.get("price")
        self.object.description = ad_data.get("description")
        self.object.category_id = category_obj

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            'name': self.object.name,
            'author_id': self.object.author_id.username,
            'author':self.object.author_id.id,
            'price': self.object.price,
            'description': self.object.description,
            'is_published': self.object.is_published,
            'image': self.object.image.url if self.object.image else None,
            'category_id': self.object.category_id.id
        })

@method_decorator(csrf_exempt, name='dispatch')
class AdDeleteView(DeleteView):
    model = Ad
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)

@method_decorator(csrf_exempt, name='dispatch')
class AdImageView(UpdateView):
    model = Ad

    fields = ['name', 'author_id', 'price', 'description', 'is_published', 'image', 'category_id']

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.image = request.FILES["image"]

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            'name': self.object.name,
            'author_id': self.object.author_id.username,
            'author': self.object.author_id.id,
            'price': self.object.price,
            'description': self.object.description,
            'is_published': self.object.is_published,
            'image': self.object.image.url if self.object.image else None,
            'category_id': self.object.category_id.id
        }, status=200)