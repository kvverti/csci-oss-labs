'''
Test markdown.py with unittest
To run tests:
    python test_markdown_unittest.py
'''

import unittest
from markdown_adapter import run_markdown

class TestMarkdownPy(unittest.TestCase):

    def setUp(self):
        pass

    def test_non_marked_lines(self):
        '''
        Non-marked lines should only get 'p' tags around all input
        '''
        self.assertEqual( 
                run_markdown('this line has no special handling'), 
                '<p>this line has no special handling</p>')

    def test_em(self):
        '''
        Lines surrounded by asterisks should be wrapped in 'em' tags
        '''
        self.assertEqual( 
                run_markdown('*this should be wrapped in em tags*'),
                '<p><em>this should be wrapped in em tags</em></p>')

    def test_strong(self):
        '''
        Lines surrounded by double asterisks should be wrapped in 'strong' tags
        '''
        self.assertEqual( 
                run_markdown('**this should be wrapped in strong tags**'),
                '<p><strong>this should be wrapped in strong tags</strong></p>')

    def test_header(self):
        self.assertEqual(run_markdown('# Header 1'), '<h1>Header 1</h1>')
        self.assertEqual(run_markdown('## Header 2'), '<h2>Header 2</h2>')
        self.assertEqual(run_markdown('### Header 3'), '<h3>Header 3</h3>')

    def test_blockquote(self):
        self.assertEqual(
               run_markdown(
'''Hello there
> This is a blockquote
> It has many letters
This is not a block quote'''),
'''<p>Hello there</p> <blockquote><p>This is a blockquote</p> <p>It has many letters</p> </blockquote><p>This is not a block quote</p>''')

if __name__ == '__main__':
    unittest.main()

