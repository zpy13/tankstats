from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
from django.conf import settings

class Tank(models.Model):
    title = models.CharField(max_length=50, unique=True)

    # Weponary parameters
    dpm = models.DecimalField(max_digits=7, decimal_places=2,null=True)
    damage = models.IntegerField(null=True)
    penetration = models.IntegerField(null=True)
    reload_time = models.DecimalField(max_digits=5, decimal_places=2,null=True)
    aim_time = models.DecimalField(max_digits=5, decimal_places=2,null=True)
    dispersion = models.DecimalField(max_digits=5, decimal_places=2,null=True)
    caliber = models.DecimalField(max_digits=5, decimal_places=2,null=True)
    shell_velocity = models.IntegerField(null=True)
    ammo_capacity = models.IntegerField(null=True)

    #Mobility parameters
    top_speed = models.DecimalField(max_digits=5, decimal_places=2,null=True)
    reverse_speed = models.DecimalField(max_digits=5, decimal_places=2,null=True)
    power_weight_ratio = models.DecimalField(max_digits=5, decimal_places=2,null=True)
    traverse_speed = models.DecimalField(max_digits=5, decimal_places=2,null=True)
    gun_elevation = models.DecimalField(max_digits=5, decimal_places=2,null=True)
    gun_depresstion = models.DecimalField(max_digits=5, decimal_places=2,null=True)

    #Other parameters
    health = models.IntegerField(null=True)
    max_load = models.IntegerField(null=True)
    view_range = models.IntegerField(null=True)

    #Foreign parameters
    country = models.ForeignKey(Country, blank=True, null=True, on_delete=models.SET_NULL)
    tank_type = models.ForeignKey(Tank_type, blank=True, null=True, on_delete=models.SET_NULL)
    tier = models.ForeignKey(Tier, blank=True, null=True, on_delete=models.SET_NULL)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comments = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Comment', related_name='comments_owned')
    tags = models.ManyToManyField(Tag, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Tank_type(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Tier(models.Model):
    tier = models.IntegerField(null=True)

    def __str__(self):
        return self.tier

class Comment(models.Model):
    text = models.TextField(
        validators=[MinLengthValidator(3, "Comment must be greater than 3 characters")]
    )

    tank = models.ForeignKey(Tank, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if len(self.text) < 15 : return self.text
        return self.text[:11] + ' ...'