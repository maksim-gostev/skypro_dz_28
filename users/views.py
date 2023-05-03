import json

from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from skypro_dz28 import settings
from users.models import User, Location


class UsersListView(ListView):
    model = User

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list = self.object_list.select_related('location_id').order_by('username')

        paginator = Paginator(self.object_list, settings.TOTOL_ON_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        users = []
        for user in page_obj:
            users.append({
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "role": user.role,
                "age": user.age,
                "location_id": user.location_id.name
            })

        response = {
            "items": users,
            "num_pages": paginator.num_pages,
            "total": paginator.count
        }

        return JsonResponse(response, safe=False)


class UsersDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        user = self.get_object()

        return JsonResponse({
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "role": user.role,
            "age": user.age,
            "location_id": user.location_id.name
        })


@method_decorator(csrf_exempt, name='dispatch')
class UsersCreateView(CreateView):
    model = User
    fields = ['first_name', 'last_name', 'username', 'password', 'role', 'age', 'location_id']

    def post(self, request, *args, **kwargs):
        user_data = json.loads(request.body)

        location_obj, _ = Location.objects.get_or_create(name=user_data['locations'])

        user = User.objects.create(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            username=user_data['username'],
            password=user_data['password'],
            role=user_data['role'],
            age=user_data['age'],
            location_id=location_obj
        )

        return JsonResponse({
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "role": user.role,
            "age": user.age,
            "location_id": user.location_id.name
        })


@method_decorator(csrf_exempt, name='dispatch')
class UsersUpdateView(UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'username', 'password', 'role', 'age', 'location_id']

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        user_data = json.loads(request.body)

        location_obj, _ = Location.objects.update_or_create(name=user_data['locations'])

        self.object.first_name = user_data.get("first_name")
        self.object.last_name = user_data.get("last_name")
        self.object.username = user_data.get("username")
        self.object.password = user_data.get("password")
        self.object.role = user_data.get("role")
        self.object.age = user_data.get("age")
        self.object.location_id = location_obj

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "first_name": self.object.first_name,
            "last_name": self.object.last_name,
            "username": self.object.username,
            "role": self.object.role,
            "age": self.object.age,
            "location_id": self.object.location_id.name
        })


@method_decorator(csrf_exempt, name='dispatch')
class UsersDeleteView(DeleteView):
    model = User
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


class UsersAdsDetailView(ListView):
    model = User

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list = self.object_list.annotate(
            total_ads=Count('ad', filter=Q(ad__is_published=True))).prefetch_related(
            'location_id').order_by('username')

        paginator = Paginator(self.object_list, settings.TOTOL_ON_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        users = []
        for user in page_obj:
            users.append({
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "role": user.role,
                "age": user.age,
                "location_id": user.location_id.name,
                "total_ads": user.total_ads
                })


        response = {
            "items": users,
            "num_pages": paginator.num_pages,
            "total": paginator.count
            }

        return JsonResponse(response, safe=False, status=200)