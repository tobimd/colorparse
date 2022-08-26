import re

# fmt: off
__all__ = ["_PAT_SPECIAL_CHARS", "_PAT_ENCAPSULATION", "_PAT_REPEATED_RESET", "_PAT_ACCEPTED_NAME_CHARS", "_PAT_ANSI_CODE", "_PAT_COMMAND"]

_PAT_SPECIAL_CHARS:re.Pattern[str]= re.compile(r"\\+[nabfrvt]")
_PAT_ENCAPSULATION:re.Pattern[str]= re.compile(r"[\s\[\]/\(\)]")
_PAT_REPEATED_RESET:re.Pattern[str]= re.compile(r"(\x1b\[0m)(\n)*\1+")
_PAT_ACCEPTED_NAME_CHARS:re.Pattern[str]= re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")
_PAT_ANSI_CODE:re.Pattern[str]= re.compile( r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
_PAT_COMMAND:re.Pattern[str]= re.compile(r"((?:(?P<sqb>\[(?=[^\]\(\)\\]*?\]))\s*|(?P<par>\((?=[^\)\[\]\\]*?\)))\s*)|\/)?(?:\\)*((?P<fg>;)|(?P<bg>:))(;|:|(?P<cl>(?(fg)(?P<fgc>(?P<a>[roygcbpma])(?P=a)?|[ROYGCBPMAkw])|(?(bg)(?P<bgc>(?P<b>[roygcbpma])(?P=b)?|[ROYGCBPMAkw]))))|[\+\-](?P<st>b|i|u|s|d|r|h)|(?P<eq>=)|(?P<hs>#)|\.)(?(eq)(?P<rgb>\d{0,3},?\d{0,3},?\d{0,3})|(?(hs)(?P<hex>[0-9a-fA-F]{0,6})))(?(sqb)(?:\s*\])|(?(par)(?:\s*\))|\/?))")

# fmt: on
