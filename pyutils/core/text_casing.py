import re


def lcc2ucc(string: str) -> str:
    """Converts lower-camel-case to upper-camel-case"""
    return string[0].upper() + string[1:]


def ucc2lcc(string: str) -> str:
    """Converts upper-camel-case to lower-camel-case"""
    return string[0].lower() + string[1:]


def ucc2sc(string: str) -> str:
    """Converts upper-camel-case to snake-case"""
    words = re.findall(pattern="[A-Z][^A-Z]*", string=string)
    words = [word.lower() for word in words]
    return "_".join(words)


def lcc2sc(string: str) -> str:
    """Converts lower-camel-case to snake-case"""
    string_ucc = lcc2ucc(string=string)
    return ucc2sc(string=string_ucc)


def sc2ucc(string: str) -> str:
    """Converts snake-case to upper-camel-case"""
    words = string.split('_')
    words_capitalized = [word.strip().capitalize() for word in words]
    return "".join(words_capitalized)


def sc2lcc(string: str) -> str:
    """Converts snake-case to lower-camel-case"""
    string_ucc = sc2ucc(string=string)
    return ucc2lcc(string=string_ucc)