from lassen.sim import PE_fc
import magma as m
import sys, os
from peak import family

PE = PE_fc(family.MagmaFamily())

if not os.path.exists('scripts/build'):
    os.makedirs('scripts/build')
m.compile(f"scripts/build/PE", PE, output="coreir-verilog")

