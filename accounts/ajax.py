from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import markdown


def get_markdown(request):
    text = request.GET.get('text')
    html = markdown.markdown(text)
    data = {'markdown': html}

    return JsonResponse(data)


@csrf_exempt
def toggle_markdown(request):
    status = request.POST['status']
    profile = request.user.profile
    if status == 'true':
        profile.using_markdown = True
    else:
        profile.using_markdown = False
    profile.save()

    return JsonResponse({'using_markdown': profile.using_markdown})
