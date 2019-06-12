from hwtypes import BitVector
from lassen import gen_pe, asm
from lassen.mem import *
from peak import Peak
from lassen.tlut import tlut
import lassen.mem.asm as mem_asm
from lassen.mem.sim import depth
from lassen.utils import float2bfbin, bfbin2float
import math

def gen_fdiv(family):
    Data = family.BitVector[16]
    PE = gen_pe(family)
    MEM = gen_mem(family)
    TLUT = tlut()
    class fdiv(Peak):
        def __init__(self):
          self.pe_get_mant  = PE()
          self.rom          = MEM()
          self.pe_scale_res = PE()
          self.pe_mult      = PE()
        #result = op_a/op_b;
        def __call__(self,in0 : Data, in1 : Data):
            inst1 = asm.fgetmant()
            inst2 = asm.fsubexp()
            inst3 = asm.fp_mul()
            rom_instr = mem_asm.rom([TLUT.div_lut(i) for i in range(0,128)]+[0x0000]*(depth - 128))
            op_a = in0
            op_b = in1
            mant,_, _         = self.pe_get_mant(inst1, op_b, Data(0))
            lookup_result     = self.rom(rom_instr,mant,Data(0))
            scaled_result,_, _= self.pe_scale_res(inst2, lookup_result, op_b)
            result,_, _       = self.pe_mult(inst3, scaled_result, op_a)
            return result
    return fdiv

def gen_fln(family):
    Data = family.BitVector[16]
    PE = gen_pe(family)
    MEM = gen_mem(family)
    TLUT = tlut()
    class fln(Peak):
        def __init__(self):
          self.pe_get_mant = PE()
          self.pe_get_exp  = PE()
          self.rom         = MEM()
          self.pe_mult     = PE()
          self.pe_add      = PE()
        #result = ln(op_a)
        def __call__(self,in0 : Data):
          inst1 = asm.fgetmant()
          inst2 = asm.fcnvexp2f()
          inst3 = asm.fp_mul()
          inst4 = asm.fp_add()
          rom_instr = mem_asm.rom([TLUT.ln_lut(i) for i in range(0,128)]+[0x0000]*(depth - 128))
          op_a = in0
          ln2 = math.log(2)
          ln2_bf = int(float2bfbin(ln2), 2)
          const_ln2 = Data(ln2_bf)
          mant,_, _     = self.pe_get_mant(inst1, op_a, Data(0))
          fexp,_, _     = self.pe_get_exp(inst2, op_a, Data(0))
          lookup_result = self.rom(rom_instr,mant,Data(0))
          mult,_, _     = self.pe_mult(inst3, fexp, const_ln2)
          result,_, _   = self.pe_mult(inst4, lookup_result, mult)
          return result
    return fln

def gen_fexp(family):
    Data = family.BitVector[16]
    PE = gen_pe(family)
    MEM = gen_mem(family)
    TLUT = tlut()
    class fexp(Peak):
        def __init__(self):
          self.pe_get_int = PE()
          self.pe_get_frac = PE()
          self.pe_rom_idx = PE ()
          self.rom = MEM()
          self.pe_incr_exp = PE()
          self.pe_div_mult = PE ()
        #result = ln(op_a)
        def __call__(self,in0 : Data):
          # Perform op_a/ln(2)
          inst1 = asm.fp_mul()
          # Compute 2**op_a
          inst2 = asm.fgetfint()
          inst3 = asm.fgetffrac()
          inst4 = asm.and_()
          inst5 = asm.faddiexp()
          rom_instr = mem_asm.rom(
                      [TLUT.exp_lut(i) for i in range(0,128)]+
                      [TLUT.exp_lut(i) for i in range(-128,0)]+
                      [0x0000]*(depth - 256)
                      )
          op_a = in0
          ln2_inv = 1.0/math.log(2)
          ln2_inv_bf = int(float2bfbin(ln2_inv), 2)
          const_ln2_inv = Data(ln2_inv_bf)
          div_res,_, _  = self.pe_div_mult(inst1, const_ln2_inv, op_a)
          fint,_, _     = self.pe_get_int(inst2, div_res, Data(0))
          ffrac,_, _    = self.pe_get_frac(inst3, div_res, Data(0))
          idx,_, _      = self.pe_rom_idx(inst4, ffrac, Data(0xFF))
          lookup_result = self.rom(rom_instr,idx,Data(0))
          result,_, _   = self.pe_incr_exp(inst5, lookup_result, fint)
          return result
    return fexp