#The COPYRIGHT file at the top level of this repository contains the full
#copyright notices and license terms.

from trytond.pool import Pool
from .production import *

def register():
    Pool.register(
        BOM,
        BOMInput,
        BOMOutput,
        module='production_efficiency_percentage', type_='model')
