from django.db import models

def get_image_upload_path(instance, filename):
    return f'images/{instance.product.category.name}/{instance.product.product_code}/{filename}'

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)

    class Meta:
        ordering = ('name', )
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

class ProductItem(models.Model):
    out_of_stock = models.BooleanField(default=False)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255)
    quantity_in_stock = models.IntegerField(default=0)
    name = models.CharField(max_length=500, null=False, blank=False)
    price = models.DecimalField(max_digits=100, decimal_places=2)
    size = models.CharField(max_length=500)
    product_code = models.CharField(max_length=100, unique=True)
    # Opuingo's products don't really have
    # special names so the colors are going to be part
    # of the names
    #colors = models.CharField(max_length=500, null=True, blank=True) 
    
    def __str__(self):
        return self.name
    
class ProductImage(models.Model):
    product = models.ForeignKey(ProductItem, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_image_upload_path)

    def __str__(self):
        return f'{self.product.name} Image'
