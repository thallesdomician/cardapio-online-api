import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

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
        r = sum([x * y for (x, y) in zip(novo, prod)]) % 11
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


def validate_image_square(image):
    limit_size = MEDIA_LOGO_SIZE
    size = image.size
    if hasattr(image, 'image'):
        height = image.image.height
        width = image.image.width
    else:
        height = image.height
        width = image.width

    if width != height:
        raise ValidationError(_("Imagem deve ter largura e altura iguais."))

    if size > limit_size * 1024 * 1024:
        raise ValidationError(_("Imagem deve ter menos de %(size)sMB"), params={'size':limit_size})

def validate_start_end(start, end):
    if end <= start:
        raise ValidationError(
                _('%(end)s must be longer than the %(start)s'),
                params={'end': end, 'start': start},
        )
