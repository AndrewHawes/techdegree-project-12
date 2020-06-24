from django.shortcuts import render

from accounts.models import Skill
from projects.models import Position


def index(request):
    positions = Position.open_positions.positions_list()
    position_names = sorted(set(position['title'] for position in positions))

    skills = Skill.objects.order_by('name').distinct()

    my_positions = get_my_positions(request)
    print(my_positions)

    context = {
        'positions': positions,
        'position_names': position_names,
        'skills': skills,
        'my_positions': my_positions
    }

    return render(request, 'index.html', context)


def search(request):
    query = request.GET.get('q')
    queryset = Position.open_positions.search(query=query)

    positions = Position.open_positions.positions_list(queryset)
    position_names = sorted(set(position['title'] for position in positions))

    skills = Skill.objects.distinct()

    my_positions = get_my_positions(request, queryset)

    context = {
        'query': query,
        'positions': positions,
        'position_names': position_names,
        'skills': skills,
        'my_positions': my_positions
    }

    return render(request, 'search.html', context)


def get_my_positions(request, queryset=None):
    if queryset is None:
        queryset = Position.open_positions

    my_positions = []

    if request.user.is_authenticated:
        my_queryset = (
            queryset
            .filter(skills__in=request.user.profile.skills.all())
            .order_by('project__title', 'title')
            .distinct()
        )
        my_positions = Position.open_positions.positions_list(my_queryset)

    return my_positions
