from decimal import Decimal

from django.db import models
from django.db.models import Q, Count, QuerySet, Avg


# 01. Real Estate Listing ----------------------------------------------------------------
class RealEstateListingManager(models.Manager):

    def by_property_type(self, property_type: str) -> QuerySet:
        return self.filter(property_type=property_type)

    def in_price_range(self, min_price: Decimal, max_price: Decimal) -> QuerySet:
        query = Q(price__gte=min_price) & Q(price__lte=max_price)
        return self.filter(query)
        # return self.filter(price__range=(min_price, max_price))

    def with_bedrooms(self, bedrooms_count: int) -> QuerySet:
        return self.filter(bedrooms=bedrooms_count)

    def popular_locations(self) -> QuerySet:
        return self.values('location').annotate(
            location_count=Count('location')
        ).order_by('-location_count', 'location')[:2]


# 02. Video Games Library ----------------------------------------------------------------
class VideoGameManager(models.Manager):
    def games_by_genre(self, genre: str):
        return self.filter(genre=genre)

    def recently_released_games(self, year: int):
        return self.filter(release_year__gte=year)

    def highest_rated_game(self):
        return self.all().order_by('-rating').first()

    def lowest_rated_game(self):
        return self.all().order_by('rating').first()

    def average_rating(self):
        avg_rating = self.aggregate(average=Avg('rating'))['average']
        return f'{avg_rating:.1f}'

# 03. Shopaholic Haven ----------------------------------------------------------------
