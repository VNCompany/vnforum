def make_list(max_page: int):
    if max_page <= 1:
        return [[1]]
    r = list(range(1, max_page + 1))
    result = []
    for i in range(0, len(r) // 9):
        result.append(r[9 * i:9 * i + 9])

    append = max_page - (len(r) // 9) * 9
    if append > 0:
        j = 0
        if len(result) > 0:
            j += result[-1][-1]
        result.append(list(range(1 + j, j + append + 1)))
    return result


def make_pagination(max_page, pos: int):
    if pos > max_page:
        pos = max_page
    li = make_list(max_page)
    j = pos // 9
    p = li[j]
    if pos >= 9:
        p.insert(0, 1)
        p.insert(1, -1)
    if pos < max_page - 9:
        p.append(-1)
        p.append(max_page)
    return p


def html_pagination(max_page, pos: int, link: str):
    pagination = make_pagination(max_page, pos)
    result = '<div class="pagination"><ul>'
    for n in pagination:
        selected = 'class="p-selected"' if n == pos else ""
        l = f'href="{link.replace("{id}", str(n))}"' if n != -1 or n == pos else ""
        text = str(n) if n != -1 else "..."

        result += f"<li {selected}><a {l}>{text}</a></li>"
    result += "</ul></div>"
    return result
