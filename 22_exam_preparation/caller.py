import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()
from django.db.models import Q, Avg, Count, F

from main_app.models import Director, Actor, Movie


def get_directors(search_name=None, search_nationality=None):
    if search_name is None and search_nationality is None:
        return ""

    query = Q()

    if search_name is not None:
        query &= Q(full_name__icontains=search_name)
    if search_nationality is not None:
        query &= Q(nationality__icontains=search_nationality)

    directors = Director.objects.filter(query).order_by('full_name')
    if not directors.exists():
        return ""

    return '\n'.join(
        f"Director: {director.full_name}, nationality: {director.nationality}, "
        f"experience: {director.years_of_experience}"
        for director in directors
    )


def get_top_director():
    """This function accepts no arguments.
        It retrieves the director with the greatest number of movies.
        If there is more than one director with the same number of movies, order them by full name, ascending, and return the first one’s info.
        Return a string in the following format:
        "Top Director: {full_name}, movies: {num_of_movies}."
        o	If there are no directors, return an empty string ("").
        o	Hint: You can use the custom model manager method.
    """
    top_director = Director.objects.get_directors_by_movies_count().first()
    if not top_director:
        return ""
    return f"Top Director: {top_director.full_name}, movies: {top_director.num_movies}."


def get_top_actor():
    """
        This function accepts no arguments.
            It retrieves the starring actor with the greatest number of movies s/he starred in.
            If there is more than one actor with the same number of movies, order them by full name, ascending, and return the first one’s info.
            Return a string in the following format:
            "Top Actor: {actor_full_name}, starring in movies: {movie_title1}, {movie_title2}, … {movie_titleN}, movies average rating: {movies_avg_rating}"
            o	Movie titles must be separated by a comma and space (", ")
            o	Average rating represents the average value of the ratings from the movies in which the actor stars. Format it to the first decimal place.
            o	If there are no movies and/or no starring actors, return an empty string ("").

    """
    top_actor = Actor.objects.annotate(
        num_movies=Count('movies_starring_actor'), movies_avg_rating=Avg('movies_starring_actor__rating', default=0)
    ).order_by('-num_movies', 'full_name').first()
    if not top_actor or not top_actor.num_movies:
        return ""
    return (f"Top Actor: {top_actor.full_name}, "
            f"starring in movies: {', '.join(movie.title for movie in top_actor.movies_starring_actor.all())}, "
            f"movies average rating: {top_actor.movies_avg_rating:.1f}")


def get_actors_by_movies_count():
    """This function accepts no arguments.
        It retrieves the top three actors from all movies, ordered by the number of times the actor has participated
        in movies, descending, then ascending by the actor’s full name.
        Take the top three ordered actors.
        Return a string in the following format:
        "{actor_full_name1}, participated in {num_movies1} movies
        {actor_full_name2}, participated in {num_movies2} movies
        {actor_full_name3}, participated in {num_movies3} movies"
        o	Each actor's info is on a new line.
        o	In case the actors are less than three in total, return all of them, ordered as described.
        o	If there are no movies and respectively no actors participating, return an empty string ("").
    """
    actors = Actor.objects.annotate(num_movies=Count('movies_actor')).order_by('-num_movies', 'full_name')[:3]
    if not actors.exists() or actors[0].num_movies == 0:
        return ''

    return '\n'.join(f"{actor.full_name}, participated in {actor.num_movies} movies" for actor in actors)


def get_top_rated_awarded_movie():
    """This function accepts no arguments.
        It retrieves a movie object with the highest rating that has been awarded and its status is "Awarded" (is_awarded=True).
        If there are more awarded movies with the same highest rating, order them by title, ascending, and get the first one.
        Return a string in the following format:
        "Top rated awarded movie: {movie_title}, rating: {movie_rating}. Starring actor: {starring_actor_full_name/'N/A'}. Cast: {participating_actor1}, {participating_actor2}, …{participating_actorN}."
        o	Movie rating must be formatted to the first decimal place.
        o	If the starring actor is None, return 'N/A' instead of the actor’s full name.
        o	Cast represents the list of all actors' full names who participated in the movie. Order them by full name, ascending, and separate each full name with a comma and space (", ").
        o	If no movies are awarded, return an empty string ("").
    """
    movie = Movie.objects.filter(is_awarded=True).select_related('starring_actor').prefetch_related('actors').order_by(
        '-rating', 'title').first()
    if not movie:
        return ""

    return (f"Top rated awarded movie: {movie.title}, "
            f"rating: {movie.rating:.1f}. "
            f"Starring actor: {movie.starring_actor.full_name if movie.starring_actor else 'N/A'}. "
            f"Cast: {', '.join(actor.full_name for actor in movie.actors.all().order_by('full_name'))}.")


def increase_rating():
    """
        This function accepts no arguments.
        It increases the rating for all movies that are considered classic – their status is "Classic" (is_classic=True) and their rating is not already set to the maximum level.
        Increase the rating by 0.1 (zero point one).
        Make sure you do not exceed the maximum rating value of 10.0.
        Return a string in the following format:
        "Rating increased for {num_of_updated_movies} movies."
        o	If a movie already has the maximum rating and is considered classic, you should not count it as updated as no change will occur.
        o	If there are no updated movies, return the string:
        "No ratings increased."
        o	Hint: You can use the F object to efficiently update the ratings.
    """
    movies_increased_rating = Movie.objects.filter(is_classic=True, rating__lt=10.0).update(rating=F('rating') + 0.1)

    if not movies_increased_rating:
        return "No ratings increased."

    return f"Rating increased for {movies_increased_rating} movies."
