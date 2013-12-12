#The COPYRIGHT file at the top level of this repository contains the full
#copyright notices and license terms.

from trytond.model import fields
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval

__all__ = ['BOM', 'BOMInput', 'BOMOutput']
__metaclass__ = PoolMeta

class BOM:
    def compute_factor(self, product, quantity, uom):
        res = super(BOM, self).compute_factor(product, quantity, uom)
        if res:
            for output in self.outputs:
                if output.product == product:
                    return res / output.efficiency
        return res

class BOMInput:
    __name__ = 'production.bom.input'

    efficiency = fields.Float('Efficiency', required=True,
        on_change_with=['wastage'])
    wastage = fields.Float('Wastage', required=True,
        on_change_with=['efficiency'])

    @staticmethod
    def default_efficiency():
        return 1.0

    @staticmethod
    def default_wastage():
        return 0.0

    def compute_quantity(self, factor):
        return super(BOMInput, self).compute_quantity(factor/self.efficiency)

    def on_change_with_efficiency(self):
        return 1 - self.wastage

    def on_change_with_wastage(self):
        return 1 - self.efficiency

class BOMOutput:
    __name__ = 'production.bom.output'
    efficiency = fields.Float('Efficiency', required=True,
        on_change_with=['wastage'])
    wastage = fields.Float('Wastage', required=True,
        on_change_with=['efficiency'])

    @staticmethod
    def default_efficiency():
        return 1.0

    @staticmethod
    def default_wastage():
        return 0.0

    def compute_quantity(self, factor):
        return super(BOMOutput, self).compute_quantity(factor*self.efficiency)

    def on_change_with_efficiency(self):
        return 1 - self.wastage

    def on_change_with_wastage(self):
        return 1 - self.efficiency
