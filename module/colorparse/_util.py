import re
from typing import Any, Union
from ._datatypes import callable_property

__all__ = ["_dprint", "_readonly_attrs", "_odir", "_any_in", "_in_any", "_break_str"]

def _dprint(*values):
    """Print wrapper to add a "debug" tag at the start of each
    value."""
    s = f"[ \033[38;5;82mdebug\033[0m ] "
    v = [a for a in ("\n".join(values)).split("\n")]
    print(s, end="")
    print(*values, sep=f"\n{s}")


def _readonly_attrs(obj:object, kwattrs:dict, kwdocs:Union[dict[str, Any], str]=dict(), *, tuple_as_callable:bool=True): # fmt: skip
    def scoped_lambda(value):
        return lambda self: getattr(self, value)

    cls = type(obj)
    
    # Copy attributes and methods
    clsdict = dict()
    for attrkey, attrvalue in cls.__dict__.items():
        if not attrkey.startswith("__"):
            clsdict[attrkey] = attrvalue

    # Add specific attribute to avoid redoing this step
    if not hasattr(cls, "__instance_with_prop_attribute"):
        cls = type(cls.__name__, (), dict(**clsdict))
        cls.__instance_with_prop_attribute = True
        obj.__class__ = cls

    # Add attributes listed in items argument
    for attrkey, attrvalue in kwattrs.items():
        # Private attributes aren't treated as readonly
        if attrkey[0] == "_":
            setattr(obj, attrkey, attrvalue)

        else:
            _attrkey = "_" + attrkey
            iscallable = type(attrvalue) is tuple and tuple_as_callable
            
            fget = scoped_lambda(_attrkey)

            if iscallable:
                fget.__doc__ = attrvalue[0].__doc__
            
            if type(kwdocs) is dict and attrkey in kwdocs:
                doc = kwdocs[attrkey]
            elif type(kwdocs) is str:
                doc = kwdocs
            else:
                doc = None

            if iscallable:
                setattr(cls, attrkey, callable_property(fget, doc=doc))
            else:
                setattr(cls, attrkey, property(fget, doc=doc))

            setattr(obj, _attrkey, attrvalue)


def _odir(obj: object) -> list[object]:
    """Wrapper for builtin ``dir``, returning the corresponding
    object instead of the attribute name."""

    return [getattr(obj, name) for name in dir(obj) if not name.startswith("_")]


def _any_in(value: str, items: list[str]) -> bool:
    """Check if any item in ``ìtems`` is in ``value``."""
    return any([i in value for i in items])


def _in_any(value: str, items: list[str]) -> bool:
    """Check if ``value`` is in any item in ``items``."""
    return any([value in i for i in items])


def _break_str(input_string: str, max_len: int) -> str:
    """Add newlines and indentation of the input_string at
    max_len number of characters per line. ANSI escape sequences
    are not considered as part of the length."""

    esc_pat = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    pst_pat = re.compile(r"%\d+")
    spc_pat = re.compile(r"[^\S\r\n]+")

    c = "¿"

    string = input_string

    esc_list = []  # ansi codes (<code>, <pos>)
    nlp_list = []  # new line positions <index>

    while "\x1b" in string:
        search_mo = re.search(esc_pat, string)

        string = string.replace(search_mo[0], c, 1)
        esc_index = string.index(c)
        string = string.replace(c, "", 1)

        esc_list.append((search_mo[0], esc_index))

    _len = len(string)
    if max_len is None or _len < max_len:
        return input_string + "\n\n"

    pos = max_len
    repl = f"\n"
    while pos < _len:
        search_slice = string[:pos][::-1]
        sub_result = re.sub(spc_pat, repl, search_slice, count=1)
        string = sub_result[::-1] + string[len(sub_result) :]
        nlp_list.append(len(sub_result) - 1)
        pos += max_len

    for esc, esc_idx in esc_list[::-1]:
        string = string[:esc_idx] + esc + string[esc_idx:]

    return string + "\033[0m\n\n"
