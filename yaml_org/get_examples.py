#!/usr/bin/env python
# coding=utf-8
import re
from collections import namedtuple
from textwrap import dedent

from bs4 import BeautifulSoup
from cache_requests import Session

from pureyaml.exceptions import YAMLUnknownSyntaxError, YAMLSyntaxError, YAMLCastTypeError
from pureyaml.parser import YAMLParser
from tests.utils import serialize_nodes

parser = YAMLParser()
Example = namedtuple('Example', ['name', 'data', 'nodes'])


def get_html():
    requests = Session(ex=3600)
    response = requests.get('http://yaml.org/spec/1.2/spec.html')
    return response.text


def clean_pre_block(block):
    stack = []
    for string in block.strings:
        has_previous_br = any([  # :off
            string.parent.previous.name == 'br',
            string.previous.name == 'br'
        ])  # :on
        if has_previous_br:
            stack.append('\n')
        cleaned = ''.join(i if ord(i) < 128 else ' ' for i in string)
        stack.append(cleaned)
    return ''.join(stack)


def get_examples(html_text):
    soup = BeautifulSoup(html_text, "html.parser")

    examples = soup.find_all('div', class_='example')

    for example in examples:
        title = example.find('p', class_='title')
        title_text = title.get_text(' ', strip=True)
        table = example.find('table', class_='simplelist')
        try:
            table_td = table.find_all('td')
            codeblock_yaml, codeblock_nodes = table_td[0].pre, table_td[1].pre
        except (AttributeError, TypeError, IndexError):
            continue


        yield Example(title_text, clean_pre_block(codeblock_yaml), clean_pre_block(codeblock_nodes))


def write(examples, f):
    file_header = dedent("""
        #!/usr/bin/env python
        # coding=utf-8
        from textwrap import dedent

        from pureyaml.nodes import *  # noqa
        from pureyaml.parser import YAMLParser
        from tests.utils import serialize_nodes

        parser = YAMLParser(debug=True)

    """)[1:]

    f.write(file_header)

    def indent_text(text, indent=0):
        indent_width = indent * 4 + 1
        return text.replace('\n', '\n'.ljust(indent_width)).rstrip('\n')

    for example in examples:
        function_name_pre = re.sub(r'\W', '_', example.name.lower(), flags=re.U)
        function_name = re.sub(r'__+', '__', function_name_pre)
        inline_key = re.sub(r'\s', ' ', example.name)
        indented_data = indent_text(example.data, indent=2)
        indented_hint = indent_text(example.nodes, indent=2)
        expected_line = "expected = None"
        encoding = ''

        if '\\N' in example.data or '\\xq-' in example.data:
            encoding = 'r'

        try:
            nodes = parser.parse(example.data)
            serialized = serialize_nodes(nodes)
            expected_line = indent_text(serialized, indent=1)
        except (YAMLUnknownSyntaxError, YAMLSyntaxError):
            pass
        except (YAMLCastTypeError, AttributeError):
            # TODO, investigate
            pass

        template = dedent("""
            def test_{function_name}():
                \"\"\"
                {inline_key}

                Expected:
                    {indented_hint}
                \"\"\"

                text = dedent({encoding}\"\"\"
                    {indented_data}
                \"\"\")[1:-1]

                {expected_line}

                nodes = parser.parse(text)
                print(serialize_nodes(nodes))

                assert nodes == expected
        """).format_map(vars())

        f.write(template)
        yield


def report(writer):
    print('Writing', end='')
    for _ in writer:
        print('.', end='')
    print('done!')


if __name__ == '__main__':
    html = get_html()
    examples = get_examples(html)
    with open('examples.py', 'w') as f:
        report(write(examples, f))
