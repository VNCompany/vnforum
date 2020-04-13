sym_lib = [
    ('$', '%24'),
    ('&', '%26'),
    ('+', '%2b'),
    (',', '%2c'),
    ('/', '%2f'),
    (':', '%3a'),
    (';', '%3b'),
    ('=', '%3d'),
    ('?', '%3f'),
    ('@', '%40'),
    (' ', '%20'),
    ('"', '%22'),
    ('<', '%3c'),
    ('>', '%3e'),
    ('#', '%23'),
    ('%', '%25'),
    ('{', '%7b'),
    ('}', '%7d'),
    ('|', '%7c'),
    ('\\', '%5c'),
    ('^', '%5e'),
    ('~', '%7e'),
    ('[', '%5b'),
    (']', '%5d'),
    ('`', '%60')
]


def url_encode(text: str):
    text = list(text)
    chars = [char[0] for char in sym_lib]
    for i in range(len(text)):
        for j in range(len(chars)):
            if text[i] == chars[j]:
                text[i] = sym_lib[j][1]
    return "".join(text)


def url_decode(text: str):
    text = list(text)
    chars = [char[1] for char in sym_lib]
    for i in range(len(text)):
        for j in range(len(chars)):
            if text[i] == chars[j]:
                text[i] = sym_lib[j][0]
    return "".join(text)
