from django.db import models
from django.db.models import Q


class OpenPositionManager(models.Manager):
    def get_queryset(self):
        queryset = (
            super().get_queryset()
            .select_related('project')
            .filter(project__is_active=True, filled=False)
        )

        return queryset

    def positions_list(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        queryset = (
            queryset
            .prefetch_related('skills')
            .order_by('project__title', 'title')
        )

        positions = []
        for position in queryset:
            positions.append({
                'title': position.title,
                'id': position.id,
                'project': position.project,
                'skills': [skill.id for skill in position.skills.all()]
            })

        return positions

    def search(self, **kwargs):
        query = kwargs.get('query', '')
        queryset = (
            self.get_queryset()
            .filter(Q(project__title__icontains=query) |
                    Q(project__description__icontains=query))
        )

        return queryset
