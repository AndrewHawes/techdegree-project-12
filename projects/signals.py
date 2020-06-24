import django.dispatch

application_status_changed = django.dispatch.Signal(
    providing_args=['current_site', 'email_template'])
