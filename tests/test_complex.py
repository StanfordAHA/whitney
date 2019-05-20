from lassen.stdlib.fma import gen_FMA
from lassen.isa import DATAWIDTH
from hwtypes import BitVector, Bit
from lassen.sim import gen_pe
import lassen.asm as asm

Bit = Bit
Data = BitVector[DATAWIDTH]

FMA = gen_FMA(BitVector.get_family())

def test_fma():
    fma = FMA()
    assert Data(58) == fma(Data(5), Data(10), Data(8))
