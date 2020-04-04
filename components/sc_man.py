import re

short_codes_library = [
    r'\[CODE=\"(php|java|c#|javascript|html|json|python)\"\](.*?)\[/CODE\]',
    r'\[LINK=\"(.+?)\"\](.*?)\[/LINK\]'
]


def strip_tags(html: str, ignore_quot=False):
    result = html.replace("&", "&amp;") \
        .replace("<", "&lt;") \
        .replace(">", "&gt;")
    return result if ignore_quot else result.replace('"', "&quot;")


def short_code_parser(html: str):
    result = re.sub(short_codes_library[0], r'<code data-language="\1">\2</code>', html, flags=re.IGNORECASE)
    result = re.sub(short_codes_library[1], r'<a href="\1" target="_blank">\2</a>', result, flags=re.IGNORECASE)
    return result
