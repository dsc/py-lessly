import re

__all__ = ('trim', 'title_case','split_camel',)

def trim(s='', *suffixes):
    "Removes suffix from s. Each given suffix is removed in order; removal is not recursive."
    for suffix in suffixes:
        if suffix and s.endswith(suffix):
            s = s[:len(suffix)]
    return s


TITLE_PAT = re.compile(r"[A-Za-z]+('[A-Za-z]+)?")

def title_replacer(m):
    return m.group(0)[0].upper() + m.group(0)[1:]

def lower_title_replacer(m):
    return m.group(0).capitalize()
    # return m.group(0)[0].upper() + m.group(0)[1:].lower()

def title_case(s, force_lower=True):
    """ Return a titlecased version of the string, where words start
        with an uppercase character and the remaining characters are
        lowercase. Unlike `str.title()`, this function correctly
        handles apostrophes.
        
        >>> title_case("tHeY'rE bILl's frienDs.")
        "They're Bill's Friends."
        
        Compare with str.title():
        
        >>> "tHeY'rE bILl's frienDs.".title()
        "They'Re Bill'S Friends."
        
        If the optional argument `force_lower` is false-y, words will
        still be capitalized, but word tails will preserve their
        capitalization.
        
        >>> title_case("they're bill's friends from the UK")
        "They're Bill's Friends From The Uk"
        >>> title_case("they're bill's friends from the UK", force_lower=False)
        "They're Bill's Friends From The UK"
    """
    replacer = lower_title_replacer if force_lower else title_replacer
    return TITLE_PAT.subn(replacer, s)[0]


def split_camel(s):
    """ Splits the string at the camel-case boundaries, returning
        a list of its parts.
        
        >>> split_camel("splitCamelCaseString")
        ['split', 'camel', 'case', 'string']
        >>> split_camel("InscrutableGenericsRelatedTypeError")
        ['inscrutable', 'generics', 'related', 'type', 'error']
        >>> split_camel("EncodeURLComponent")
        ['encode', 'url', 'component']
    """
    out = []
    tok = s[0].lower()
    caps_run = False
    for c in s[1:]:
        is_caps = c.isupper()
        if caps_run and not is_caps:
            out.append(tok[:-1])
            tok = tok[-1] + c.lower()
        elif is_caps and not prev_caps:
            out.append(tok)
            tok = c.lower()
        else:
            tok += c.lower()
        caps_run  = is_caps and prev_caps
        prev_caps = is_caps
    out.append(tok)
    return out

