#!/usr/bin/env python
# coding=utf-8
import re
from collections import OrderedDict
from textwrap import dedent

from bs4 import BeautifulSoup
from cache_requests import Session

requests = Session(ex=3600)
# ns = {'xhtml': 'http://www.w3.org/1999/xhtml'}
response = requests.get('http://yaml.org/spec/1.2/spec.html')
soup = BeautifulSoup(response.text, "html.parser")

examples = soup.find_all('div', class_='example')
examples_dict = OrderedDict()
for example in examples:
    title = example.find('p', class_='title')
    title_text = title.get_text(' ', strip=True)
    table = example.find('table', class_='simplelist')
    try:
        codeblock = table.pre
        stack = []
        for string in codeblock.strings:
            if string.parent.previous.name == 'br':
                stack.append('\n')
            cleaned = ''.join(i if ord(i) < 128 else ' ' for i in string)
            stack.append(cleaned)
        examples_dict[title.get_text(' ', strip=True)] = ''.join(stack)
    except AttributeError:
        continue

print("""
#!/usr/bin/env python
# coding=utf-8
from textwrap import dedent

from pureyaml.nodes import *  # noqa
from pureyaml.parser import YAMLParser
from tests.utils import serialize_nodes

pureyaml_parser = YAMLParser(debug=True)

"""[1:])

for key, value in examples_dict.items():
    function_name_pre = re.sub(r'\W', '_', key.lower(),flags=re.U)
    function_name = re.sub(r'__+', '__', function_name_pre)
    inline_key = re.sub(r'\s', ' ', key)
    indented_value = value.replace('\n', '\n'.ljust(9)).rstrip('\n', )
    template = dedent("""
        def test_{function_name}():
            \"\"\"{inline_key}\"\"\"

            text = dedent(\"\"\"
                {indented_value}
            \"\"\")[1:-1]

            expected = None

            nodes = pureyaml_parser.parse(text)
            print(serialize_nodes(nodes))

            assert nodes == expected
    """).format_map(vars())

    print(template)
