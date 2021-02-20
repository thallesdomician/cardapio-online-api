from PIL import Image
import os
from io import BytesIO
from django.db.models.fields.files import ImageFieldFile
from django.core.files.storage import default_storage as storage
from django.core.files.base import ContentFile


def create_thumbnail(self, image_field: ImageFieldFile, thumbnail_image_field: ImageFieldFile, size: tuple):
    if not image_field:
        return
    """
            Create and save the thumbnail for the photo (simple resize with PIL).
            """
    fh = storage.open(image_field.file.file.name, 'r')
    try:
        image = Image.open(fh)
    except Exception as e:
        return False

    image.thumbnail(size, Image.ANTIALIAS)
    fh.close()

    # Path to save to, name, and extension
    thumb_name, thumb_extension = os.path.splitext(image_field.name)
    thumb_extension = thumb_extension.lower()

    thumb_filename = thumb_name + '_thumb' + thumb_extension

    if thumb_extension in ['.jpg', '.jpeg']:
        FTYPE = 'JPEG'
    elif thumb_extension == '.gif':
        FTYPE = 'GIF'
    elif thumb_extension == '.png':
        FTYPE = 'PNG'
    else:
        return False  # Unrecognized file type

    # Save thumbnail to in-memory file as StringIO
    temp_thumb = BytesIO()
    image.save(temp_thumb, FTYPE)
    temp_thumb.seek(0)

    # Load a ContentFile into the thumbnail field so it gets saved
    thumbnail_image_field.save(thumb_filename, ContentFile(temp_thumb.read()), save=True)
    temp_thumb.close()

    return True
