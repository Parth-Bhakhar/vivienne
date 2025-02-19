from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.db import models
import os
from django.utils.timezone import now

class Admin(models.Model):
        email = models.CharField(max_length=255,unique=True)
        password = models.CharField(max_length=255)

        def __str__(self):
            return self.email


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('diamond', 'Diamond'),
        ('gold', 'Gold'),
        ('silver', 'Silver'),
    ]


    STATUS_CHOICES = [
        (1, 'Enabled'),
        (0, 'Disabled'),
    ]

    product_name = models.CharField(max_length=255, unique=True)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=1)


    # Common fields for images
    product_picture1 = models.ImageField(upload_to='media/')
    product_picture2 = models.ImageField(upload_to='media/')
    product_picture3 = models.ImageField(upload_to='media/')

    def __str__(self):
        return self.product_name


class Diamond(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='diamond_details')
    diamond_id = models.CharField(max_length=255, unique=True)
    diamond_shape = models.CharField(max_length=50)
    diamond_type = models.CharField(max_length=50, choices=[('natural', 'Natural'), ('lab_grown', 'Lab Grown')])
    diamond_color = models.CharField(max_length=50)
    diamond_carat = models.FloatField()
    diamond_quantity = models.PositiveIntegerField()
    description = models.TextField(null=True)
    diamond_mrp = models.DecimalField(max_digits=10, decimal_places=2)
    tax=models.PositiveIntegerField()

    def __str__(self):
        return f"Diamond - {self.product.product_name}"


class Gold(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='gold_details')
    gold_id = models.CharField(max_length=255, unique=True)
    gold_category = models.CharField(max_length=255)
    weight = models.FloatField()
    carat = models.FloatField(choices=[(91.60, '22K'), (84.00, '20K'), (76.00, '18K'), (58.33, '14K')])
    labour_percentage = models.PositiveIntegerField()
    description = models.TextField(null=True)
    gold_quantity = models.PositiveIntegerField()
    diamond_weight_in_gold = models.FloatField()
    diamond_rate_in_gold = models.PositiveIntegerField()
    gold_mrp = models.DecimalField(max_digits=10, decimal_places=2)
    bangle_size = models.CharField(max_length=10, null=True, blank=True)
    ring_bracelet_size = models.CharField(max_length=10, null=True, blank=True)
    other_charges = models.PositiveIntegerField(null=True)
    tax=models.PositiveIntegerField()

    def __str__(self):
        return f"Gold - {self.product.product_name}"


class Silver(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='silver_details')
    silver_id = models.CharField(max_length=255, unique=True)
    silver_category = models.CharField(max_length=255)
    weight = models.FloatField()
    silver_quantity = models.PositiveIntegerField()
    diamond_weight_in_silver = models.FloatField()
    diamond_rate_in_silver = models.PositiveIntegerField()
    description = models.TextField(null=True)
    silver_mrp = models.DecimalField(max_digits=10, decimal_places=2)
    bangle_size = models.CharField(max_length=10, null=True, blank=True)
    ring_bracelet_size = models.CharField(max_length=10, null=True, blank=True)
    tax=models.PositiveIntegerField()

    def __str__(self):
        return f"Silver - {self.product.product_name}"


def delete_produc(sender, instance, **kwargs):
    for field in ['product_picture1', 'product_picture2', 'product_picture3']:
        file_field = getattr(instance, field)
        if file_field:
            print(f"File Path: {file_field.path}")  # Debugging
            if os.path.isfile(file_field.path):
                os.remove(file_field.path)
                print(f"Deleted: {file_field.path}")


class MetalRate(models.Model):
    date = models.DateField(default=now) 
    time = models.TimeField()
    gold_rate = models.DecimalField(max_digits=10, decimal_places=2)
    silver_rate = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Rates on {self.date}: Gold - {self.gold_rate}, Silver - {self.silver_rate}"