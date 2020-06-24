from datetime import date

from django.conf import settings
from django.db import models

import markdown

from accounts.models import Skill
from projects.managers import OpenPositionManager


class Project(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_projects'
    )
    title = models.CharField(max_length=120)
    url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True)
    timeline = models.CharField(max_length=254, blank=True)
    applicant_requirements = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    date_created = models.DateField(default=date.today)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['owner', 'title'], name='unique_project')
        ]

    def get_description(self):
        if self.owner.profile.using_markdown:
            return markdown.markdown(self.description)
        else:
            return self.description

    def __str__(self):
        return self.title


class Position(models.Model):
    title = models.CharField(max_length=60)
    description = models.TextField(blank=True)
    time_commitment = models.CharField(max_length=120, blank=True)
    filled = models.BooleanField(default=False)

    skills = models.ManyToManyField(Skill, related_name='positions')
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='positions'
    )
    filled_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='positions',
        null=True,
        blank=True,
    )
    applicants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='Application',
    )

    objects = models.Manager()
    open_positions = OpenPositionManager()

    class Meta:
        # Prevents users from accepting multiple positions on one project.
        constraints = [
            models.UniqueConstraint(fields=['project', 'filled_by'], name='unique_filled_by')
        ]
        ordering = ['title']

    def get_description(self):
        if self.project.owner.profile.using_markdown:
            return markdown.markdown(self.description)
        else:
            return self.description

    def save(self, *args, **kwargs):
        self.filled = bool(self.filled_by is not None)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Application(models.Model):
    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        related_name='applications',
    )
    # True = accepted, False = rejected, None(default) = undecided
    accepted = models.BooleanField(blank=True, null=True)

    class Meta:
        # Prevents users from applying for the same position twice.
        constraints = [
            models.UniqueConstraint(fields=['applicant', 'position'], name='unique_applicant')
        ]

    @property
    def project(self):
        return self.position.project

    def approve(self):
        self.accepted = True

    def reject(self):
        self.accepted = False

    def __str__(self):
        return f'{self.position}, Applicant: {self.applicant}'
