from dataclasses import dataclass

import requests
from django.core.files.base import ContentFile
from django.core.management import BaseCommand
from tqdm import tqdm

from mall.models import Category, Product, Product_Nutrition, Product_Ingredient, Product_Photo

BASE_URL = "https://greenyday.co.kr/dev/api/items/"


@dataclass
class Item:
    pk: int
    name: str
    calorie: int
    price: int
    description: str
    nutritions: dict
    ingredients: dict
    itemimges: list
    category: dict
class Command(BaseCommand):
    help = "Load products from JSON file."

    def handle(self, *args, **options):
        item_dict_list = requests.get(BASE_URL).json()

        item_list = [Item(**item_dict) for item_dict in item_dict_list]
        category_name_set = {item.category['name'] for item in item_list}

        category_dict = dict()

        for category_name in category_name_set:
            category, __ = Category.objects.get_or_create(name=category_name)
            category_dict[category.name] = category

        for item in tqdm(item_list):
            category: Category = category_dict[item.category['name']]
            product, is_created = Product.objects.get_or_create(
                category=category,
                name=item.name,
                calorie=item.calorie,
                price=item.price,
                description=item.description,
            )

            if is_created:
                nutritions, __ = Product_Nutrition.objects.get_or_create(product=product, **item.nutritions)
                ingredients, __ = Product_Ingredient.objects.get_or_create(product=product, **item.ingredients)

            if product.name == item.name:
                for photo_list in item.itemimges:
                    filename = photo_list['photo'].rsplit("/", 1)[-1]
                    photo_data = requests.get(photo_list['photo']).content
                    photo, __ = Product_Photo.objects.get_or_create(
                        product=product,
                        name=f'{product.name}_사진',
                    )

                    photo.photo.save(
                        name=filename,
                        content=ContentFile(photo_data),
                        save=True,
                    )
                print(item.itemimges)

