#The COPYRIGHT file at the top level of this repository contains the full
#copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta

__all__ = ['BOM', 'BOMInput', 'BOMOutput']


class BOM(metaclass=PoolMeta):
    __name__ = 'production.bom'

    def compute_factor(self, product, quantity, uom):
        res = super(BOM, self).compute_factor(product, quantity, uom)
        if res:
            for output in self.outputs:
                if output.product == product:
                    return res / (output.efficiency if output.efficiency
                        else 0.0)
        return res


class BOMMixin(metaclass=PoolMeta):
    efficiency = fields.Float('Efficiency', required=True, digits=(16, 4))
    wastage = fields.Float('Wastage', required=True, digits=(16, 4))

    @staticmethod
    def default_efficiency():
        return 1.0

    @staticmethod
    def default_wastage():
        return 0.0

    @fields.depends('wastage')
    def on_change_with_efficiency(self):
        return None if self.wastage is None else 1 - self.wastage

    @fields.depends('efficiency')
    def on_change_with_wastage(self):
        return None if self.efficiency is None else 1 - self.efficiency


class BOMInput(BOMMixin):
    __name__ = 'production.bom.input'

    def compute_quantity(self, factor):
        if factor and self.efficiency and self.efficiency > 0:
            value = factor / self.efficiency
        else:
            value = factor
        return super(BOMInput, self).compute_quantity(value)


class BOMOutput(BOMMixin):
    __name__ = 'production.bom.output'

    def compute_quantity(self, factor):
        if factor:
            value = factor * self.efficiency
        else:
            value = factor
        return super(BOMOutput, self).compute_quantity(value)
