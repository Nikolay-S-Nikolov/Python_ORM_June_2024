import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()
from django.db.models import F, Q
from main_app.models import Pet, Artifact, Location, Car, Task, HotelRoom, Character


# 01. Pet ----------------------------------------------------------------
def create_pet(name: str, species: str):
    pet = Pet.objects.create(name=name, species=species)
    return f"{pet.name} is a very cute {pet.species}!"


# 02. Artifact ----------------------------------------------------------------
def create_artifact(
        name: str,
        origin: str,
        age: int,
        description: str,
        is_magical: bool
):
    artifact = Artifact.objects.create(
        name=name,
        origin=origin,
        age=age,
        description=description,
        is_magical=is_magical
    )
    return f"The artifact {artifact.name} is {artifact.age} years old!"


def rename_artifact(
        artifact: Artifact,
        new_name: str
):
    if artifact.is_magical and artifact.age > 250:
        artifact.name = new_name
        artifact.save()


def delete_all_artifacts():
    Artifact.objects.all().delete()


# 03. Location ----------------------------------------------------------------
def show_all_locations():
    locations_models = Location.objects.all().order_by('-id')
    result = []
    for location in locations_models:
        result.append(f'{location.name} has a population of {location.population}!')
    return '\n'.join(result)


def new_capital():
    locations_model = Location.objects.all().first()
    locations_model.is_capital = True
    locations_model.save()


def get_capitals():
    queryset = Location.objects.all().filter(is_capital=True).values('name')
    return queryset


def delete_first_location():
    Location.objects.all().first().delete()


# 04. Car ----------------------------------------------------------------
def apply_discount():
    cars = Car.objects.all()
    for car in cars:
        discount = sum(int(x) for x in str(car.year))
        car.price_with_discount = car.price - car.price * discount / 100
        car.save()


def get_recent_cars():
    return Car.objects.all().values('model', 'price_with_discount').filter(year__gt=2020)


def delete_last_car():
    Car.objects.all().last().delete()


# 05. Task Encoder ----------------------------------------------------------------
def show_unfinished_tasks():
    unfinished_tasks = Task.objects.filter(is_finished=False)
    result = []
    for task in unfinished_tasks:
        result.append(f'Task - {task.title} needs to be done until {task.due_date}!')
    return '\n'.join(result)


def complete_odd_tasks():
    odd_tasks = Task.objects.all()
    for task in odd_tasks:
        if task.id % 2 != 0:
            task.is_finished = True
            task.save()


def encode_and_replace(text: str, task_title: str):
    new_description = ''.join(chr(ord(x) - 3) for x in text)
    Task.objects.filter(title=task_title).update(description=new_description)

    # tasks_to_replace_description = Task.objects.filter(title=task_title)
    # for task in tasks_to_replace_description:
    #     task.description = new_description
    #     task.save()


# 06. Hotel Room ----------------------------------------------------------------
def get_deluxe_rooms():
    rooms = HotelRoom.objects.all().filter(room_type='Deluxe')
    result = []

    for room in rooms:
        if room.id % 2 == 0:
            result.append(room)
    return '\n'.join(str(r) for r in result)


def increase_room_capacity():
    rooms = HotelRoom.objects.all()

    previous_room_capacity = None

    for room in rooms:
        if not room.is_reserved:
            continue
        if not previous_room_capacity:
            room.capacity += room.id
        else:
            room.capacity += previous_room_capacity
        previous_room_capacity = room.capacity
        room.save()


def reserve_first_room():
    first_room = HotelRoom.objects.all().first()
    first_room.is_reserved = True
    first_room.save()


def delete_last_room():
    last_room = HotelRoom.objects.all().last()
    if not last_room.is_reserved:
        last_room.delete()


# 07. Character ----------------------------------------------------------------
"""
F expressions (F()):

F() expressions allow you to reference model field values within a query, enabling you to perform operations
  directly in the database without retrieving the data into Python memory.
They are useful for updating or filtering based on the values of other fields within the same model.
For example, F("field_name") represents the value of the field field_name in the database.

Q objects (Q()):
Q() objects are used to encapsulate complex query conditions, such as OR conditions, negations, and combinations of
conditions.
They allow you to build dynamic queries with multiple conditions using logical operators like AND (&), OR (|), and 
NOT (~).
For example, Q(field1=value1) | Q(field2=value2) represents a query where either field1 equals value1 or field2 equals 
value2.
"""


def update_characters() -> None:
    Character.objects.filter(class_name='Mage').update(
        level=F('level') + 3,
        intelligence=F('intelligence') - 7
    )

    Character.objects.filter(class_name='Warrior').update(
        hit_points=F('hit_points') / 2,
        dexterity=F('dexterity') + 4
    )

    Character.objects.filter(class_name__in=["Assassin", "Scout"]).update(
        inventory='The inventory is empty'
    )

    # Character.objects.filter(Q(class_name='Assassin') | Q(class_name='Scout').update(
    #     inventory='The inventory is empty'
    # )


def fuse_characters(first_character: Character, second_character: Character):
    if first_character.class_name in ['Mage', 'Scout']:
        new_inventory = "Bow of the Elven Lords, Amulet of Eternal Wisdom"
    else:
        new_inventory = "Dragon Scale Armor, Excalibur"
    Character.objects.create(
        name=first_character.name + ' ' + second_character.name,
        class_name='Fusion',
        level=(first_character.level + second_character.level) // 2,
        strength=(first_character.strength + second_character.strength) * 1.2,
        dexterity=(first_character.dexterity + second_character.dexterity) * 1.4,
        intelligence=(first_character.intelligence + second_character.intelligence) * 1.5,
        hit_points=(first_character.hit_points + second_character.hit_points),
        inventory=new_inventory
    )
    first_character.delete()
    second_character.delete()


def grand_dexterity():
    Character.objects.update(dexterity=30)


def grand_intelligence():
    Character.objects.update(intelligence=40)


def grand_strength():
    Character.objects.update(strength=50)


def delete_characters():
    Character.objects.filter(inventory='The inventory is empty').delete()


# character1 = Character.objects.create(
#     name='Gandalf',
#     class_name='Mage',
#     level=10,
#     strength=15,
#     dexterity=20,
#     intelligence=25,
#     hit_points=100,
#     inventory='Staff of Magic, Spellbook',
# )
#
# character2 = Character.objects.create(
#     name='Hector',
#     class_name='Warrior',
#     level=12,
#     strength=30,
#     dexterity=15,
#     intelligence=10,
#     hit_points=150,
#     inventory='Sword of Troy, Shield of Protection',
# )
#
# fuse_characters(character1, character2)
# fusion = Character.objects.filter(class_name='Fusion').get()
#
# print(fusion.name)
# print(fusion.class_name)
# print(fusion.level)
# print(fusion.intelligence)
# print(fusion.inventory)
