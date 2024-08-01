import os
import django
from django.db.models import Q, Count

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import TennisPlayer, Tournament, Match


def get_tennis_players(search_name=None, search_country=None):
    if search_name is None and search_country is None:
        return ''
    query = Q()
    if search_name:
        query &= Q(full_name__icontains=search_name)

    if search_country:
        query &= Q(country__icontains=search_country)

    players = TennisPlayer.objects.filter(query).order_by('ranking')

    if not players.exists():
        return ""

    return '\n'.join(f"Tennis Player: {p.full_name}, country: {p.country}, ranking: {p.ranking}" for p in players)


def get_top_tennis_player():
    player = TennisPlayer.objects.get_tennis_players_by_wins_count().first()

    if not player:
        return ""

    return f"Top Tennis Player: {player.full_name} with {player.num_wins} wins."


def get_tennis_player_by_matches_count():
    player = TennisPlayer.objects.annotate(
        num_of_matches=Count('matches')).order_by('-num_of_matches', 'ranking').first()

    if not player or not player.num_of_matches:
        return ""

    return f"Tennis Player: {player.full_name} with {player.num_of_matches} matches played."


def get_tournaments_by_surface_type(surface=None):
    if surface is None:
        return ""

    tournaments = Tournament.objects.filter(
        surface_type__icontains=surface).annotate(num_matches=Count('matches')).order_by('-start_date')

    if not tournaments.exists():
        return ""

    return '\n'.join(
        f"Tournament: {t.name}, start date: {t.start_date}, matches: {t.num_matches}"
        for t in tournaments)


def get_latest_match_info():
    last_match = Match.objects.select_related('tournament', 'winner').prefetch_related(
        'players').order_by('-date_played', '-pk').first()

    if not last_match:
        return ""

    player1_full_name, player2_full_name = [p.full_name for p in last_match.players.all().order_by('full_name')]

    return (f"Latest match played on: {last_match.date_played}, tournament: {last_match.tournament.name}, "
            f"score: {last_match.score}, players: {player1_full_name} vs {player2_full_name}, "
            f"winner: {last_match.winner.full_name if last_match.winner else 'TBA'}, summary: {last_match.summary}")


def get_matches_by_tournament(tournament_name=None):
    if tournament_name is None:
        return "No matches found."

    matches = Match.objects.filter(
        tournament__name=tournament_name).select_related('winner').order_by('-date_played')

    if not matches.exists():
        return "No matches found."

    return '\n'.join(
        f"Match played on: {m.date_played}, score: {m.score}, winner: {m.winner.full_name if m.winner else 'TBA'}"
        for m in matches)

