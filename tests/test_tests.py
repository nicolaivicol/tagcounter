from tagcounter.udf import html_tags, word_frequency


def test_html_tags():
    x = """<!DOCTYPE html><html><body><h1>x</h1><p>x</p></body></html>"""
    assert html_tags(x) == ['html', 'body', 'h1', 'p']


def test_word_frequency():
    x = ['a', 'a', 'h', 'b', 'a', 'b']
    assert word_frequency(x) == {'a': 3, 'b': 2, 'h': 1}