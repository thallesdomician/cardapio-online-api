from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re

from cardapioOnlineApi.settings import MEDIA_LOGO_SIZE


def valite_cnpj(cnpj):
    cnpj = ''.join(re.findall('\d', str(cnpj)))
    if (not cnpj) or (len(cnpj) < 14):
        raise ValidationError(
            _('%(value)s is not an valid CNPJ'),
            params={'value': cnpj},
        )
    inteiros = list(map(int, cnpj))
    novo = inteiros[:12]

    prod = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    while len(novo) < 14:
        r = sum([x*y for (x, y) in zip(novo, prod)]) % 11
        if r > 1:
            f = 11 - r
        else:
            f = 0
        novo.append(f)
        prod.insert(0, 6)

    if novo != inteiros:
        raise ValidationError(
            _('%(value)s is not an valid CNPJ'),
            params={'value': cnpj},
        )


def validate_logo_size(image):
    max_size = MEDIA_LOGO_SIZE
    if hasattr(image, 'image'):
        height = image.image.height
        width = image.image.width
    else:
        height = image.height
        width = image.width
    if width != max_size or height != max_size:
        raise ValidationError(_("Height and Width must be %(value)dpx"), params={'value': MEDIA_LOGO_SIZE})
