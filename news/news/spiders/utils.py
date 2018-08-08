# coding=utf-8
import codecs

def parse_js(expr):
    """
    解析非标准JSON的Javascript字符串，等同于json.loads(JSON str)
    :param expr:非标准JSON的Javascript字符串
    :return:Python字典
    """
    import ast
    m = ast.parse(expr)
    a = m.body[0]

    def parse(node):
        if isinstance(node, ast.Expr):
            return parse(node.value)
        elif isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.Str):
            return node.s
        elif isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Dict):
            return dict(zip(map(parse, node.keys), map(parse, node.values)))
        elif isinstance(node, ast.List):
            return map(parse, node.elts)
        else:
            raise NotImplementedError(node.__class__)

    return parse(a)


def parse_js_1(expr):
    """
    解析非标准JSON的Javascript字符串，等同于json.loads(JSON str)
    :param expr:非标准JSON的Javascript字符串
    :return:Python字典
    """
    obj = eval(expr, type('Dummy', (dict,), dict(__getitem__=lambda s, n: n))())
    return obj


if __name__ == '__main__':
    test_file_path = "/Users/wind/Desktop/test.txt"
    with codecs.open(test_file_path, 'r', 'utf-8') as f:
        test_file = f.read().replace('.replace(/<br \/>/ig, '')', '')

    print(test_file)

    import yaml

    aa = yaml.load(test_file)
    print(aa)