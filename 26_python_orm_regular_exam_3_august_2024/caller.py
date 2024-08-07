import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from django.db.models import Q, Count, Sum, F, Avg
from main_app.models import Astronaut, Mission, Spacecraft


def get_astronauts(search_string=None):
    if search_string is None:
        return ""

    query = Q(name__icontains=search_string) | Q(phone_number__icontains=search_string)

    astronauts = Astronaut.objects.filter(query).order_by('name')

    if not astronauts.exists():
        return ""

    return '\n'.join(
        f"Astronaut: {a.name}, phone number: {a.phone_number}, status: {'Active' if a.is_active else 'Inactive'}"
        for a in astronauts
    )


def get_top_astronaut():
    astronaut = Astronaut.objects.get_astronauts_by_missions_count().first()

    if not astronaut or not astronaut.num_missions:
        return "No data."

    return f"Top Astronaut: {astronaut.name} with {astronaut.num_missions} missions."


def get_top_commander():
    commander = Astronaut.objects.annotate(
        num_of_missions=Count('commander_missions')
    ).order_by('-num_of_missions', 'phone_number').first()

    if not commander or not commander.num_of_missions:
        return "No data."

    return f"Top Commander: {commander.name} with {commander.num_of_missions} commanded missions."


def get_last_completed_mission():
    last_mission = Mission.objects.select_related(
        'commander', 'spacecraft').filter(
        status='Completed').order_by('-launch_date').first()

    if not last_mission:
        return "No data."

    total_spacewalks = last_mission.astronauts.aggregate(sum_walks=Sum('spacewalks'))['sum_walks']

    return (f"The last completed mission is: {last_mission.name}. "
            f"Commander: {last_mission.commander.name if last_mission.commander else 'TBA'}. "
            f"Astronauts: {', '.join(a.name for a in last_mission.astronauts.all().order_by('name'))}. "
            f"Spacecraft: {last_mission.spacecraft.name}. Total spacewalks: {total_spacewalks}.")


def get_most_used_spacecraft():
    spacecraft = Spacecraft.objects.annotate(
        num_missions=Count('missions', distinct=True),
        num_astronauts=Count('missions__astronauts', distinct=True)
    ).order_by('-num_missions', 'name').first()

    if not spacecraft or not spacecraft.num_missions:
        return "No data."

    return (f"The most used spacecraft is: {spacecraft.name}, manufactured by {spacecraft.manufacturer}, "
            f"used in {spacecraft.num_missions} missions, astronauts on missions: {spacecraft.num_astronauts}.")


def decrease_spacecrafts_weight():
    num_of_spacecrafts_affected = (Spacecraft.objects.filter(
        missions__status='Planned', weight__gte=200.0).distinct().update(weight=F('weight') - 200.0))
    if not num_of_spacecrafts_affected:
        return "No changes in weight."

    avg_weight = Spacecraft.objects.aggregate(avg_weight=Avg('weight'))['avg_weight']

    return (f"The weight of {num_of_spacecrafts_affected} spacecrafts has been decreased. "
            f"The new average weight of all spacecrafts is {avg_weight:.1f}kg")
