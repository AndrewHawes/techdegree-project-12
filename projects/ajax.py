from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST

from projects.models import Position, Application
from projects.signals import application_status_changed


@login_required(login_url=reverse_lazy('signin'))
@require_POST
def apply_for_position(request, pk):
    user = request.user
    position = get_object_or_404(Position, pk=pk)

    position.applicants.add(user)
    data = {'status': "Application received."}

    return JsonResponse(data)


@login_required(login_url=reverse_lazy('signin'))
@require_POST
def application_status(request, status, pk):
    application = get_object_or_404(Application, pk=pk)
    if status == 'accept':
        application.accepted = True
        email_template = 'projects/emails/acceptance_email.html'
    elif status == 'reject':
        application.accepted = False
        email_template = 'projects/emails/rejection_email.html'
    else:
        return JsonResponse({'errors': 'Bad URL.'})

    application.save()

    current_site = get_current_site(request)
    application_status_changed.send(
        sender=Application,
        instance=application,
        current_site=current_site,
        email_template=email_template
    )
    data = {'status': application.accepted}

    return JsonResponse(data)
