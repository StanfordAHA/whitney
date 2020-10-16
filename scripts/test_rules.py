from lassen.sim import PE_fc
import lassen.asm as asm

from peak.mapper import ArchMapper, RewriteRule, read_serialized_bindings
from metamapper.irs.coreir import gen_CoreIRNodes
import metamapper.coreir_util as cutil
from metamapper import CoreIRContext

from pysmt.logics import QF_BV
from hwtypes import BitVector
import coreir
import pytest
import json

c = CoreIRContext(reset=True)
cutil.load_libs(["commonlib"])
CoreIRNodes = gen_CoreIRNodes(16)

lassen_ops = (

    "coreir.or_",
    "coreir.mul",
    "coreir.and_",
    "commonlib.smax",
    "commonlib.smin",
    "commonlib.umax",
    "commonlib.umin",
    "coreir.add",
    "coreir.ule",
    "coreir.sle",
    "coreir.ult",
    "coreir.slt",
    "coreir.ugt",
    "coreir.sgt",
    "corebit.not_",
    "corebit.mux",
    "corebit.or_",
    "corebit.and_",
    "corebit.xor",
    "coreir.sub",
    "commonlib.abs",
    "coreir.eq",
    "coreir.lshr",
    "coreir.ashr",
    "coreir.shl",
    "coreir.mux",
)


with open("scripts/rewrite_rules/lassen_rewrite_rules.json", "r") as read_file:
    rrs = json.loads(read_file.read())

for op in lassen_ops:
    print(f"testing {op}", flush=True)
    ir_fc = CoreIRNodes.peak_nodes[op]
    new_rewrite_rule = read_serialized_bindings(rrs[op], ir_fc, PE_fc)
    counter_example = new_rewrite_rule.verify()

    if counter_example is not None:
        print(counter_example)
        exit()