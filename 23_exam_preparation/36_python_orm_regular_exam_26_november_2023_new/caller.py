import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from django.db.models import Count, Q, Avg, Max
from main_app.models import *


def get_authors(search_name=None, search_email=None):
    if search_name is None and search_email is None:
        return ""

    query = Q()

    if search_name is not None:
        query &= Q(full_name__icontains=search_name)

    if search_email is not None:
        query &= Q(email__icontains=search_email)

    authors = Author.objects.filter(query).order_by("-full_name")
    if not authors.exists():
        return ""

    return "\n".join(
        f"Author: {author.full_name}, email: {author.email}, status: {'Banned' if author.is_banned else 'Not Banned'}"
        for author in authors)


def get_top_publisher():
    author = Author.objects.get_authors_by_article_count().first()
    if not author or not author.num_article:
        return ""
    return f"Top Author: {author.full_name} with {author.num_article} published articles."


def get_top_reviewer():
    top_reviewer = Author.objects.annotate(reviews_count=Count("reviews")).order_by("-reviews_count", "email").first()
    if top_reviewer is None or top_reviewer.reviews_count == 0:
        return ""
    return f"Top Reviewer: {top_reviewer.full_name} with {top_reviewer.reviews_count} published reviews."


def get_latest_article():
    latest_article = Article.objects.prefetch_related('reviews', 'authors').order_by('-published_on').first()
    if not latest_article:
        return ""
    avg_article_rating = latest_article.reviews.aggregate(avg_rating=Avg('rating',default=0))['avg_rating']
    result = (
        f"The latest article is: {latest_article.title}. "
        f"Authors: {', '.join(author.full_name for author in latest_article.authors.all().order_by('full_name'))}. "
        f"Reviewed: {latest_article.reviews.count()} times. Average Rating: {avg_article_rating:.2f}.")
    return result


def get_top_rated_article():
    article = Article.objects.annotate(
        avg_rating=Avg('reviews__rating', default=0),
        num_reviews=Count('reviews__rating')
    ).order_by('-avg_rating', 'title').first()
    if not article or not article.num_reviews:
        return ""
    return (f"The top-rated article is: {article.title}, "
            f"with an average rating of {article.avg_rating:.2f}, reviewed {article.num_reviews} times.")


def ban_author(email=None):
    if email is None:
        return "No authors banned."
    author = Author.objects.filter(email=email
                                   ).prefetch_related('reviews').first()
    if not author:
        return "No authors banned."
    num_reviews = author.reviews.count()
    author.is_banned = True
    author.save()
    for review in author.reviews.all():
        review.delete()
    return f"Author: {author.full_name} is banned! {num_reviews} reviews deleted."
