import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from django.db.models import Q, Count, F, Min, Avg
from main_app.models import House, Dragon, Quest


def get_houses(search_string=None):
    if search_string is None or search_string.strip() == "":  # If the search_string is None or empty:
        return "No houses match your search."

    query = Q(name__istartswith=search_string) | Q(motto__istartswith=search_string)
    houses = House.objects.filter(query).order_by('-wins', "name")

    if not houses.exists():
        return "No houses match your search."

    return '\n'.join(
        f"House: {h.name}, wins: {h.wins}, motto: {h.motto if h.motto else 'N/A'}"
        for h in houses
    )


def get_most_dangerous_house():
    house = House.objects.get_houses_by_dragons_count().first()

    if not house or not house.num_dragons:
        return "No relevant data."

    return (f"The most dangerous house is the House of {house.name} with {house.num_dragons} dragons. "
            f"Currently {'ruling' if house.is_ruling else 'not ruling'} the kingdom.")


def get_most_powerful_dragon():
    dragon = Dragon.objects.filter(is_healthy=True).annotate(
        num_quests=Count('quests')).order_by('-power', 'name').first()

    if not dragon:
        return "No relevant data."

    return (f"The most powerful healthy dragon is {dragon.name} with a power level of {dragon.power:.1f}, "
            f"breath type {dragon.breath}, and {dragon.wins} wins, coming from the house of {dragon.house.name}. "
            f"Currently participating in {dragon.num_quests} quests.")


def update_dragons_data():
    num_of_dragons_affected = Dragon.objects.filter(
        is_healthy=False, power__gt=1.0
    ).update(power=F('power') - 0.1, is_healthy=True)

    if not num_of_dragons_affected:
        return "No changes in dragons data."

    min_power = Dragon.objects.aggregate(minimum_power=Min('power'))['minimum_power']

    return (f"The data for {num_of_dragons_affected} dragon/s has been changed. "
            f"The minimum power level among all dragons is {min_power:.1f}")


def get_earliest_quest():
    quest = Quest.objects.prefetch_related('dragons').annotate(avg_power=Avg('dragons__power')).order_by(
        'start_time').first()

    if not quest:
        return "No relevant data."

    return (f"The earliest quest is: {quest.name}, code: {quest.code}, "
            f"start date: {quest.start_time.day}.{quest.start_time.month}.{quest.start_time.year}, "
            f"host: {quest.host.name}. "
            f"Dragons: {'*'.join(d.name for d in quest.dragons.all().order_by('-power', 'name'))}. "
            f"Average dragons power level: {quest.avg_power:.2f}")


def announce_quest_winner(quest_code):
    quest = Quest.objects.filter(code__exact=quest_code).first()

    if not quest:
        return "No such quest."

    dragon_winner = quest.dragons.order_by('-power', 'name').first()
    dragon_winner.wins += 1
    dragon_winner.save()

    winning_house = dragon_winner.house
    winning_house.wins += 1
    winning_house.save()

    quest.delete()

    return (f"The quest: {quest.name} has been won by dragon {dragon_winner.name} from house {winning_house.name}. "
            f"The number of wins has been updated as follows: {dragon_winner.wins} total wins "
            f"for the dragon and {winning_house.wins} total wins for the house. "
            f"The house was awarded with {quest.reward:.2f} coins.")

