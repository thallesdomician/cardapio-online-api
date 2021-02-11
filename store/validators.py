from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re

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
