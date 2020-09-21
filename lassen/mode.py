from peak import Peak, gen_register, family_closure
from hwtypes.adt_util import rebind_type
from functools import lru_cache
from hwtypes.adt import Enum
"""
Field for specifying register modes
"""
class Mode_t(Enum):
    CONST = 0   # Register returns constant in constant field
    BYPASS = 2  # Register is bypassed and input value is returned

@lru_cache(None)
def gen_register_mode(T, init=0):
    @family_closure
    def RegisterMode_fc(family):
        T_f = rebind_type(T, family)
        Reg = gen_register(T_f, init)(family)
        Bit = family.Bit
        @family.assemble(locals(), globals())
        class RegisterMode(Peak):
            def __init__(self):
                self.register: Reg = Reg()

            #Outputs <based on mode>, register_value
            def __call__(self, mode: Mode_t, const_: T_f, value: T_f) -> (T_f):

                if mode == Mode_t.CONST:
                    return const_
                else: #if mode == Mode_t.BYPASS:
                    return value

        return RegisterMode

    return RegisterMode_fc
