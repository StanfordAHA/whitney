from .cond import Cond_t
from .mode import Mode_t
from .lut import LUT_t_fc
from .alu import ALU_t, Signed_t
from .common import DATAWIDTH
from peak import Const, family_closure
from hwtypes.adt import Product

"""
https://github.com/StanfordAHA/CGRAGenerator/wiki/PE-Spec
"""
@family_closure
def Inst_fc(family):
    Data = family.BitVector[DATAWIDTH]
    Bit = family.Bit

    LUT_t, _ = LUT_t_fc(family)
    class Inst(Product):
        alu= ALU_t          # ALU operation
        signed= Signed_t     # unsigned or signed
        lut= LUT_t          # LUT operation as a 3-bit LUT
        cond= Cond_t        # Condition code (see cond.py)

    return Inst
