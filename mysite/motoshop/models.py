from django.db import models
from django.contrib.auth.models import User, AbstractUser
from PIL import Image
from tinymce.models import HTMLField


class CustomUser(AbstractUser):
    photo = models.ImageField(upload_to='profile_pics',
                              null=True,
                              blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.photo:
            img = Image.open(self.photo.path)
            min_side = min(img.width, img.height)
            left = (img.width - min_side) // 2
            top = (img.height - min_side) // 2
            right = left + min_side
            bottom = top + min_side
            img = img.crop((left, top, right, bottom))
            img = img.resize((300, 300), Image.LANCZOS)
            img.save(self.photo.path)

    class Meta:
        verbose_name = 'Vartotojas'
        verbose_name_plural = 'Vartotojai'

class Product(models.Model):
    title = models.CharField(verbose_name='Pavadinimas')
    code = models.CharField(verbose_name='Prekės kodas', max_length=10)
    product_category = (
        ('1', 'Motociklai'),
        ('2', 'Atsarginės dalys'),
        ('3', 'Apranga'),
        ('4', 'Aksesuarai'),
    )
    category = models.CharField(verbose_name='Kategorija',
                                max_length=1,
                                choices=product_category)
    manufacturer = models.CharField(verbose_name='Gamintojas')
    sizes = (
        ('1', 'S'),
        ('2', 'M'),
        ('3', 'L'),
        ('4', 'XL'),
        ('5', 'XXL'),
    )
    size = models.CharField(verbose_name='Dydis',
                            max_length=1,
                            choices=sizes,
                            null=True,
                            blank=True)

    stock_quantity = models.PositiveIntegerField(verbose_name='Kiekis sandėlyje/pas tiekėją')
    stocked = models.BooleanField(verbose_name='Ar yra sandelyje?', default=True)
    definition = HTMLField(verbose_name='Aprašymas',
                           null=True,
                           blank=True)
    new_product = models.BooleanField(verbose_name='Ar prekė nauja', default=False)
    rrp = models.DecimalField(verbose_name='Rekom. mažmeninė kaina',
                              max_digits=8,
                              decimal_places=2)
    final_price = models.DecimalField(verbose_name='Pardavimo kaina',
                                      max_digits=8,
                                      decimal_places=2)
    cover = models.ImageField(verbose_name='Nuotrauka',
                              upload_to='product_covers',
                              null=True,
                              blank=True)

    class Meta:
        verbose_name = 'Prekė'
        verbose_name_plural = 'Prekės'

    def __str__(self):
        return self.title

class Order(models.Model):
    order_date = models.DateField(verbose_name='Užsakymo pateikimo data', auto_now_add=True)
    client = models.ForeignKey(verbose_name='Klientas',
                               to=CustomUser,
                               on_delete=models.DO_NOTHING,
                               db_constraint=False,
                               null=False,
                               blank=False,
                               related_name='orders')
    order_status = (
        ('1', 'Pateiktas'),
        ('2', 'Surenkamas'),
        ('3', 'Paruoštas'),
        ('4', 'Perduotas pristatymui'),
        ('5', 'Vėluoja'),
        ('6', 'Užbaigtas'),
        ('7', 'Atšauktas'),
    )
    status = models.CharField(verbose_name='Statusas',
                              max_length=1,
                              choices=order_status,
                              default='1')
    due_date = models.DateField(verbose_name='Užsakymo užbaigimo data')

    class Meta:
        verbose_name = 'Užsakymas'
        verbose_name_plural = 'Užsakymai'

    def __str__(self):
        return f'{self.pk}'

class OrderLine(models.Model):
    order = models.ForeignKey(verbose_name='Užsakymas',
                              to=Order,
                              on_delete=models.DO_NOTHING,
                              db_constraint = False,
                              null = False,
                              blank = False,
                              related_name = 'ol')
    product = models.ForeignKey(verbose_name='Produktas',
                                to=Product,
                                on_delete=models.DO_NOTHING,
                                db_constraint=False,
                                null=False,
                                blank=False,
                                related_name='ol'
                                )
    quantity = models.PositiveIntegerField(verbose_name='Kiekis')

    class Meta:
        verbose_name = 'Užsakymo eilutė'
        verbose_name_plural = 'Užsakymo eilutės'

    def __str__(self):
        return f'{self.product.title} - {self.quantity}'

class Post(models.Model):
    title = models.CharField(verbose_name='Pavadinimas')
    content = HTMLField(verbose_name='Tūrinys')
    author = models.ForeignKey(verbose_name='Autorius',
                               to=CustomUser,
                               on_delete=models.SET_NULL,
                               null=True,
                               blank=True,
                               related_name = 'posts')
    created = models.DateTimeField(verbose_name='Įrašas sukūrtas', auto_now_add=True)
    cover = models.ImageField(verbose_name='Viršelis',
                              upload_to='posts_covers',
                              null=True,
                              blank=True)

    class Meta:
        verbose_name = 'Įrašas'
        verbose_name_plural = 'Įrašai'

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(verbose_name='Įrašas',
                             to="Post",
                             on_delete=models.CASCADE,
                             related_name='comments')
    content = models.TextField(verbose_name='Komentaras')
    author = models.ForeignKey(verbose_name='Komentatorius',
                               to=CustomUser,
                               on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name='Komentaro data',auto_now_add=True)

    def __str__(self):
        return f"{self.content}"

    class Meta:
        ordering = ["-pk"]
        verbose_name = 'Komentaras'
        verbose_name_plural = 'Komentarai'