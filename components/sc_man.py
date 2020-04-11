import re
import base64

short_codes_library = [
    r'\[CODE=\"(php|java|csharp|javascript|html|json|python)\"\](.*?)\[/CODE\]',
    r'\[LINK=\"(.+?)\"\](.*?)\[/LINK\]',
    r'\[IMG=\"(.+?)\"\]',
    r'\[b\](.*?)\[/b\]',
    r'\[i\](.*?)\[/i\]',
    r'\[u\](.*?)\[/u\]',
    r'\[quote\](.*?)\[/quote\]'
]


def strip_tags(html: str):
    result = html.replace("&", "&amp;") \
        .replace("<", "&lt;") \
        .replace(">", "&gt;")
    return result


def repl(m):
    return f'<pre><code data-language="{m[1]}">{m[2].replace("<br>", "")}</code></pre>'


def short_code_parser(html: str):
    html = strip_tags(html)
    result = re.sub(r"\r?\n", "<br>\n", html)

    for key, val in enumerate(short_codes_library[3:]):
        if key == 0:
            match = r"<strong>\1</strong>"
        elif key == 1:
            match = r"<i>\1</i>"
        elif key == 2:
            match = r'<span style="text-decoration: underline;">\1</span>'
        else:
            match = r'<blockquote>\1</blockquote>'
        result = re.sub(val, match, result,
                        flags=re.I | re.M | re.S)
    result = re.sub(short_codes_library[0], repl, result,
                    flags=re.I | re.M | re.S)
    result = re.sub(short_codes_library[1], r'<a href="\1" target="_blank">\2</a>', result,
                    flags=re.I | re.M)
    result = re.sub(short_codes_library[2], r'<a href="\1" target="_blank"><img class="post-image" '
                                            r'alt="Image" src="\1"></a>',
                    result,
                    flags=re.I | re.M)
    return result
