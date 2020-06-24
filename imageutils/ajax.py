import logging
from io import BytesIO
import os

from django.contrib.auth import settings
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from PIL import Image

from imageutils.forms import PhotoForm

logger = logging.getLogger(__name__)


@require_POST
def save_image(request):
    """Processes image file and saves it as user avatar."""

    data = request.POST
    profile = request.user.profile

    src = data['src']
    x = float(data['x'])
    y = float(data['y'])
    width = float(data['width'])
    height = float(data['height'])
    rotate = float(data['rotate'])

    filename = os.path.basename(src)
    filepath = os.path.join(settings.BASE_DIR, src[1:])

    with Image.open(filepath) as image:
        image_format = image.format
        mime = Image.MIME[image_format]

        image = image.rotate(-rotate, expand=True)
        image = image.crop((x, y, width + x, height + y))

        with BytesIO() as buffer:
            image.save(fp=buffer, format=image_format)
            imagefile = ContentFile(buffer.getvalue())

    profile.avatar.save(filename, InMemoryUploadedFile(
        file=imagefile,
        field_name=None,
        name=filename,
        content_type=mime,
        size=imagefile.tell,
        charset=None)
    )

    return JsonResponse({'is_valid': True, 'url': profile.avatar.url})


@require_POST
def upload_avatar(request):
    """Creates new Photo object (from PhotoForm) and saves it to user avatar."""

    form = PhotoForm(request.POST, request.FILES)
    profile = request.user.profile

    if form.is_valid():
        photo = form.save(commit=False)
        filename = os.path.basename(photo.file.path)

        profile.avatar.save(filename, photo.file, save=True)
        data = {'is_valid': True, 'name': profile.avatar.name, 'url': profile.avatar.url}
    else:
        data = {'is_valid': False}
        if form.errors:
            logger.error('Problem uploading avatar.\n', form.errors)
            data['errors'] = form.errors.as_json()

    return JsonResponse(data)
