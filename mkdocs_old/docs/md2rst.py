import sys, re


def links(matchobj):
    string = matchobj[0]

    text = re.search(r'(?<=\[).+(?=\])', string)[0]
    link = re.search(r'(?<=\().+(?=\))', string)[0]
    
    if string[0] == '!':
        return f'.. image:: {link}\n    :alt: {text}\n'
    return f'`{text} <{link}>`_'


def titles(matchobj):
    string = matchobj[0]

    sep = '-' if string.count('#') > 2 else '='
    name = re.search(rf'(?<={"#" * string.count("#")} ).+', string)[0]

    return f'{name}\n{sep * len(name)}\n'


def code_blocks(matchobj):
    string = matchobj[0]

    name = re.search(r'(?<=```).+', string)[0]
    content = re.search(rf'(?<=```{name}\n)(.|\n)+(?=```)', string)[0]
    content_tabbed = ''
    for line in content.split('\n'):
        content_tabbed += f'\t{line}\n'

    return f'.. code:: {name}\n\n{content_tabbed}\n'


def main():
    md_file = sys.argv[1]
    rst_file = f'{md_file[:-2]}rst' if len(sys.argv) < 3 else sys.argv

    with open(md_file, 'r') as f:
        data = f.read()

    data = re.sub(r'(?<!`)`(?!`)', r'``', data)                  # replace backticks
    data = re.sub(r'!?\[.+?\]\(.+?\)', links, data)              # links / images
    data = re.sub(r'```\w+(.|\n)+?```\n', code_blocks, data)     # code blocks (explicit)
    data = re.sub(r'(?<=.):(?=\n+\t)', '::', data)               # code blocks (implicit)
    data = re.sub(r'(?<=\n)#{1,4} .+\n?', titles, data)          # titles  

    with open(rst_file, 'w') as f:
        f.write(data)


if __name__ == '__main__':
    main()
