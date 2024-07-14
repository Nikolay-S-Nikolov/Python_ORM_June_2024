import os

import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()
from typing import List
from main_app.models import ArtworkGallery, Laptop, ChessPlayer, Meal, Dungeon, Workout
from django.db.models import Case, Value, When, Q, F


# 01. Artwork Gallery ----------------------------------------------------------------
def show_highest_rated_art() -> str:
    art = ArtworkGallery.objects.order_by('-rating', 'id').first()
    return f"{art.art_name} is the highest-rated art with a {art.rating} rating!"


def bulk_create_arts(first_art: ArtworkGallery, second_art: ArtworkGallery) -> None:
    ArtworkGallery.objects.bulk_create([first_art, second_art])


def delete_negative_rated_arts():
    ArtworkGallery.objects.filter(rating__lt=0).delete()


# artwork1 = ArtworkGallery(artist_name='Vincent van Gogh', art_name='Starry Night', rating=4, price=1200000.0)
# artwork2 = ArtworkGallery(artist_name='Leonardo da Vinci', art_name='Mona Lisa', rating=5, price=1500000.0)
# # Bulk saves the instances
# bulk_create_arts(artwork1, artwork2)
# print(show_highest_rated_art())
# print(ArtworkGallery.objects.all())


# 02. Laptop --------------------------------------------------------------------------------


def show_the_most_expensive_laptop() -> str:
    most_expensive_laptop = Laptop.objects.order_by('-price', '-id').first()

    return f"{most_expensive_laptop.brand} is the most expensive laptop available for {most_expensive_laptop.price}$!"


def bulk_create_laptops(args: List[Laptop]) -> None:
    Laptop.objects.bulk_create(args)


def update_to_512_GB_storage():
    # Laptop.objects.filter(Q(branda="Asus") | Q(branda="Lenovo")).update(storage=512)
    Laptop.objects.filter(brand__in=["Asus", "Lenovo"]).update(storage=512)


def update_to_16_GB_memory():
    Laptop.objects.filter(brand__in=["Apple", "Dell", "Acer"]).update(memory=16)


def update_operation_systems():
    Laptop.objects.update(operation_system=Case(
        When(brand="Asus", then=Value("Windows")),
        When(brand="Apple", then=Value("MacOS")),
        When(brand__in=["Dell", "Acer"], then=Value("Linux")),
        When(brand="Lenovo", then=Value("Chrome OS")),
        default=F("operation_system")
    ))


def delete_inexpensive_laptops():
    Laptop.objects.filter(price__lt=1200).delete()


# laptop1 = Laptop(
#     brand='Asus',
#     processor='Intel Core i5',
#     memory=8,
#     storage=256,
#     operation_system='MacOS',
#     price=899.99
# )
# laptop2 = Laptop(
#     brand='Apple',
#     processor='Chrome OS',
#     memory=16,
#     storage=256,
#     operation_system='MacOS',
#     price=1399.99
# )
# laptop3 = Laptop(
#     brand='Lenovo',
#     processor='AMD Ryzen 7',
#     memory=12,
#     storage=256,
#     operation_system='Linux',
#     price=999.99,
# )

# # Create a list of instances
# laptops_to_create = [laptop1, laptop2, laptop3]
#
# # Use bulk_create to save the instances
# bulk_create_laptops(laptops_to_create)
#
# update_to_512_GB_storage()
# update_operation_systems()
#
# # Retrieve 2 laptops from the database
# asus_laptop = Laptop.objects.filter(brand__exact='Asus').get()
# lenovo_laptop = Laptop.objects.filter(brand__exact='Lenovo').get()
#
# print(asus_laptop.storage)
# print(lenovo_laptop.operation_system)

# 03. Chess Player ----------------------------------------------------------------------------------------

def bulk_create_chess_players(args: List[ChessPlayer]):
    ChessPlayer.objects.bulk_create(args)


def delete_chess_players():
    ChessPlayer.objects.filter(title="no title").delete()


def change_chess_games_won():
    ChessPlayer.objects.filter(title="GM").update(games_won=30)


def change_chess_games_lost():
    ChessPlayer.objects.filter(title="no title").update(games_lost=25)


def change_chess_games_drawn():
    ChessPlayer.objects.all().update(games_drawn=10)


def grand_chess_title_GM():
    ChessPlayer.objects.filter(rating__gte=2400).update(title="GM")


def grand_chess_title_IM():
    ChessPlayer.objects.filter(rating__range=(2300, 2399)).update(title="IM")


def grand_chess_title_FM():
    ChessPlayer.objects.filter(rating__range=(2200, 2299)).update(title="FM")


def grand_chess_title_regular_player():
    ChessPlayer.objects.filter(rating__range=(0, 2199)).update(title="regular player")


#
# player    1 = ChessPlayer(
#     username='Player1',
#     title='no title',
#     rating=2200,
#     games_played=50,
#     games_won=20,
#     games_lost=25,
#     games_drawn=5,
# )
# player2 = ChessPlayer(
#     username='Player2',
#     title='IM',
#     rating=2350,
#     games_played=80,
#     games_won=40,
#     games_lost=25,
#     games_drawn=15,
# )
#
# # Call the bulk_create_chess_players function
# bulk_create_chess_players([player1, player2])
#
# # Call the delete_chess_players function
# delete_chess_players()
#
# # Check that the players are deleted
# print("Number of Chess Players after deletion:", ChessPlayer.objects.count())


# 04. Meal -----------------------------------------------------------------------------

def set_new_chefs():
    Meal.objects.update(chef=Case(
        When(meal_type='Breakfast', then=Value('Gordon Ramsay')),
        When(meal_type='Lunch', then=Value('Julia Child')),
        When(meal_type='Dinner', then=Value('Jamie Oliver')),
        When(meal_type='Snack', then=Value('Thomas Keller')),
    ))


def set_new_preparation_times():
    Meal.objects.update(preparation_time=Case(
        When(meal_type='Breakfast', then=Value('10 minutes')),
        When(meal_type='Lunch', then=Value('12 minutes')),
        When(meal_type='Dinner', then=Value('15 minutes')),
        When(meal_type='Snack', then=Value('5 minutes')),
    ))


def update_low_calorie_meals():
    Meal.objects.filter(meal_type__in=["Breakfast", "Dinner"]).update(calories=400)


def update_high_calorie_meals():
    Meal.objects.filter(meal_type__in=["Lunch", "Snack"]).update(calories=700)


def delete_lunch_and_snack_meals():
    Meal.objects.filter(meal_type__in=["Lunch", "Snack"]).delete()


#
# meal1 = Meal.objects.create(
#     name="Pancakes",
#     meal_type="Breakfast",
#     preparation_time="20 minutes",
#     difficulty=3,
#     calories=350,
#     chef="Jane",
# )
#
# meal2 = Meal.objects.create(
#     name="Spaghetti Bolognese",
#     meal_type="Dinner",
#     preparation_time="45 minutes",
#     difficulty=4,
#     calories=550,
#     chef="Sarah",
# )
# # Test the set_new_chefs function
# set_new_chefs()
#
# # Test the set_new_preparation_times function
# set_new_preparation_times()
#
# # Refreshes the instances
# meal1.refresh_from_db()
# meal2.refresh_from_db()

# Print the updated meal information
# print("Meal 1 Chef:", meal1.chef)
# print("Meal 1 Preparation Time:", meal1.preparation_time)
# print("Meal 2 Chef:", meal2.chef)
# print("Meal 2 Preparation Time:", meal2.preparation_time)
#

# 05. Dungeon ------------------------------------------------------------------


def show_hard_dungeons():
    dungeons = Dungeon.objects.filter(difficulty="Hard").order_by('-location')
    return '\n'.join(
        f"{dungeon.name} is guarded by {dungeon.boss_name} who has {dungeon.boss_health} health points!"
        for dungeon in dungeons
    )


def bulk_create_dungeons(args: List[Dungeon]):
    Dungeon.objects.bulk_create(args)


def update_dungeon_names():
    Dungeon.objects.update(name=Case(
        When(difficulty="Easy", then=Value("The Erased Thombs")),
        When(difficulty="Medium", then=Value("The Coral Labyrinth")),
        When(difficulty="Hard", then=Value("The Lost Haunt")),
    ))


def update_dungeon_bosses_health():
    Dungeon.objects.exclude(difficulty='Easy').update(boss_health=500)


def update_dungeon_recommended_levels():
    Dungeon.    objects.update(recommended_level=Case(
        When(difficulty="Easy", then=Value(25)),
        When(difficulty="Medium", then=Value(50)),
        When(difficulty="Hard", then=Value(75)),
    ))


def update_dungeon_rewards():
    Dungeon.objects.update(reward=Case(
        When(boss_health=500, then=Value("1000 Gold")),
        When(location__startswith="E", then=Value("New dungeon unlocked")),
        When(location__endswith="s", then=Value("Dragonheart Amulet")),
    ))


def set_new_locations():
    Dungeon.objects.update(location=Case(
        When(recommended_level=25, then=Value("Enchanted Maze")),
        When(recommended_level=50, then=Value("Grimstone Mines")),
        When(recommended_level=75, then=Value("Shadowed Abyss")),
    ))


# Create two instances
dungeon1 = Dungeon(
    name="Dungeon 1",
    boss_name="Boss 1",
    boss_health=1000,
    recommended_level=75,
    reward="Gold",
    location="Eternal Hell",
    difficulty="Hard",
)

dungeon2 = Dungeon(
    name="Dungeon 2",
    boss_name="Boss 2",
    boss_health=400,
    recommended_level=25,
    reward="Experience",
    location="Crystal Caverns",
    difficulty="Easy",
)


#
# # Bulk save the instances
# bulk_create_dungeons([dungeon1, dungeon2])
#
# # Update boss's health
# update_dungeon_bosses_health()
#
# # Show hard dungeons
# hard_dungeons_info = show_hard_dungeons()
# print(hard_dungeons_info)
#
# # Change dungeon names based on difficulty
# update_dungeon_names()
# dungeons = Dungeon.objects.order_by('boss_health')
# print(dungeons[0].name)
# print(dungeons[1].name)
#
# # Change the dungeon rewards
# update_dungeon_rewards()
# dungeons = Dungeon.objects.order_by('boss_health')
# print(dungeons[0].reward)
# print(dungeons[1].reward)

# 06. Workout ------------------------------------------------------------------------------------


def show_workouts():
    workouts = Workout.objects.filter(workout_type__in=["Calisthenics", "CrossFit"])
    return '\n'.join(
        f"{workout.name} from {workout.workout_type} type has {workout.difficulty} difficulty!"
        for workout in workouts
    )


def get_high_difficulty_cardio_workouts():
    return Workout.objects.filter(workout_type="Cardio", difficulty="High").order_by("instructor")


def set_new_instructors():
    Workout.objects.update(instructor=Case(
        When(workout_type='Cardio', then=Value("John Smith")),
        When(workout_type='Strength', then=Value("Michael Williams")),
        When(workout_type='Yoga', then=Value("Emily Johnson")),
        When(workout_type='CrossFit', then=Value("Sarah Davis")),
        When(workout_type='Calisthenics', then=Value("Chris Heria")),
    ))


def set_new_duration_times():
    Workout.objects.update(duration=Case(
        When(instructor='John Smith', then=Value("15 minutes")),
        When(instructor='Sarah Davis', then=Value("30 minutes")),
        When(instructor='Chris Heria', then=Value("45 minutes")),
        When(instructor='Michael Williams', then=Value("1 hour")),
        When(instructor='Emily Johnson', then=Value("1 hour and 30 minutes")),
    ))


def delete_workouts():
    Workout.objects.exclude(workout_type__in=["Strength", "Calisthenics"]).delete()
