from rest_framework import serializers

from .models import Product, Review, StarForProduct, Category


class CreateReviewSerializers(serializers.ModelSerializer):
    '''Отзывы одного продукта'''

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Review
        fields = '__all__'


class ReviewSerializers(serializers.ModelSerializer):
    '''Детали отзыва одного продукта'''

    class Meta:
        model = Review
        fields = ('user', 'description', 'created')


class CategorySerializers(serializers.ModelSerializer):
    '''Категории'''

    class Meta:
        model = Category
        fields = '__all__'


class ProductListSerializers(serializers.ModelSerializer):
    '''Список продуктов'''
    rating_user = serializers.BooleanField()
    category = CategorySerializers(read_only=True)
    middle_star = serializers.IntegerField()

    class Meta:
        model = Product
        fields = ('name', 'price', 'category', 'rating_user', 'middle_star')


class ProductDetailSerializers(serializers.ModelSerializer):
    '''Детали одного продукта'''

    category = CategorySerializers(read_only=True)
    product_reviews = ReviewSerializers(many=True)

    class Meta:
        model = Product
        exclude = ('is_active',)


class ProductCreateSerializers(serializers.ModelSerializer):
    '''Создание продукта'''

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'poster', 'category', 'quantity', 'user')


class CreateRatingSerializer(serializers.ModelSerializer):
    '''Добавление рейтинга'''

    class Meta:
        model = StarForProduct
        fields = ('star', 'product')

    def create(self, validated_data):
        rating, _ = StarForProduct.update_or_create(
            ip=validated_data.get('ip', None),
            product=validated_data.get('product', None),
            defaults={'star': validated_data.get('star')}

        )
        return rating
