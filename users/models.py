from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=200)
    lat = models.FloatField(null=True)
    lng = models.FloatField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'локация'
        verbose_name_plural = 'локации'


class User(models.Model):
    ROLE = [
        ('admin', 'Администратор'),
        ('moderator', 'Модератор'),
        ('member', 'Пользователь')
    ]


    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    role = models.CharField(max_length=20, choices=ROLE, default="member")
    age = models.PositiveIntegerField()
    location_id = models.ForeignKey(Location,  on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ["username"]
