from collections import namedtuple
from itertools import product
import random

import pytest

from hwtypes import SIntVector, UIntVector, BitVector, Bit
from magma.bitutils import int2seq
from peak.family import PyFamily


import lassen.asm as asm
from lassen import PE_fc, Inst_fc
from lassen.common import DATAWIDTH, BFloat16_fc

from rtl_utils import rtl_tester, CAD_ENV

Inst = Inst_fc(PyFamily())
Mode_t = Inst.rega

PE = PE_fc(PyFamily())
pe = PE()

BFloat16 = BFloat16_fc(PyFamily())
Data = BitVector[DATAWIDTH]


def test_fp_mul():
    # Regression test for https://github.com/StanfordAHA/lassen/issues/111
    inst = asm.fp_add()
    data0 = Data(0x8000)
    data1 = Data(0x8000)
    res, res_p, _ = pe(inst, data0, data1)
    # print("res: ", res)
    if CAD_ENV:
        rtl_tester(inst, data0, data1, res=res)
    else:
        pytest.skip("Skipping since DW not available")