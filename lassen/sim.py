from peak import Peak, family_closure, name_outputs, Const
from functools import lru_cache
import magma as m

from .common import *
from .lut import LUT_fc
from .alu import ALU_fc
from .cond import Cond_fc
from .isa import Inst_fc

@family_closure
def PE_fc(family):
    BitVector = family.BitVector

    #Hack
    def BV1(bit):
        return bit.ite(family.BitVector[1](1), family.BitVector[1](0))
    Data = family.BitVector[DATAWIDTH]
    UData = family.Unsigned[DATAWIDTH]
    Data8 = family.BitVector[8]
    Data32 = family.BitVector[32]
    Bit = family.Bit
    ALU = ALU_fc(family)
    Cond = Cond_fc(family)
    LUT = LUT_fc(family)
    Inst = Inst_fc(family)

    @family.assemble(locals(), globals())
    class PE(Peak):
        def __init__(self):

            #ALU
            self.alu: ALU = ALU()

            #Condition code
            self.cond: Cond = Cond()

            #Lut
            self.lut: LUT = LUT()

        @name_outputs(alu_res=Data, res_p=Bit)
        def __call__(self, inst: Const(Inst), \
            data0: Data, data1: Data = Data(0), \
            bit0: Bit = Bit(0), bit1: Bit = Bit(0), bit2: Bit = Bit(0), \
            clk_en: Global(Bit) = Bit(1), \
        ) -> (Data, Bit):
            # Simulate one clock cycle

            # calculate alu results
            alu_res, alu_res_p, Z, N, C, V = self.alu(inst.alu, inst.signed, data0, data1, bit0)

            # calculate lut results
            lut_res = self.lut(inst.lut, bit0, bit1, bit2)

            # calculate 1-bit result
            res_p = self.cond(inst.cond, alu_res_p, lut_res, Z, N, C, V)

            # return 16-bit result, 1-bit result
            return alu_res, res_p
    return PE
