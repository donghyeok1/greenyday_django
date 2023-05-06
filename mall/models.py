from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = "상품 분류"

class Store(models.Model):
    name = models.CharField(max_length=100, unique=True)
    position = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = "가맹점 분류"

class Product(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "a", "정상"
        SOLD_OUT = "s", "품절"
        OBSOLETE = "o", "단종"
        INACTIVE = "i", "비활성화"

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        db_constraint=False # db에서 외래키 제약사항 필드인데, 번거로워서 보통 끔
    )
    store_set = models.ManyToManyField('Store', blank=True)
    name = models.CharField(max_length=100, db_index=True)
    description = models.TextField(blank=True)
    calorie = models.PositiveIntegerField()
    price = models.PositiveIntegerField() # 0 포함
    status = models.CharField(
        choices=Status.choices,
        default=Status.INACTIVE,
        max_length=1
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"<{self.pk}> {self.name}"

    class Meta:
        verbose_name = verbose_name_plural = "상품"

class Product_Photo(models.Model):
    product = models.ForeignKey(
        Product,
        related_name='product_image',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=50, unique=True)
    photo = models.ImageField(
        upload_to="mall/product/photo/%Y/%m/%d",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = "상품 이미지"

class Product_Nutrition(models.Model):
    product = models.OneToOneField(
        Product,
        related_name='nutritions',
        on_delete=models.CASCADE
    )
    protein = models.FloatField(default=0)
    carbohydrate = models.FloatField(default=0)
    fat = models.FloatField(default=0)

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = verbose_name_plural = "상품 탄단지"

class Product_Ingredient(models.Model):
    product = models.OneToOneField(
        Product,
        related_name='ingredients',
        on_delete=models.CASCADE
    )
    description = models.TextField()

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = verbose_name_plural = "상품 영양 성분"