import unittest
from blocks import BlockType, block_to_blocktype

class test_blocks(unittest.TestCase):
    def test_block_to_blocktype_heading_1(self):
        md = """# heading        
        """
        block_type = block_to_blocktype(md)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_blocktype_heading_2(self):
        md = """## heading        
        """
        block_type = block_to_blocktype(md)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_blocktype_heading_3(self):
        md = """### heading        
        """
        block_type = block_to_blocktype(md)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_blocktype_heading_4(self):
        md = """#### heading        
        """
        block_type = block_to_blocktype(md)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_blocktype_heading_5(self):
        md = """##### heading        
        """
        block_type = block_to_blocktype(md)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_blocktype_heading_6(self):
        md = """###### heading        
        """
        block_type = block_to_blocktype(md)
        self.assertEqual(block_type, BlockType.HEADING)
        
    def test_block_to_blocktype_code(self):
        md = """```asölfdkj asödlfkj asdfölkj asdfölkj```"""
        block_type = block_to_blocktype(md)
        self.assertEqual(block_type, BlockType.CODE)
        
        md2 = """```asdfölk asödlfkja sdfölkj asdfölkj d"""
        block_type = block_to_blocktype(md2)
        self.assertNotEqual(block_type, BlockType.CODE)
        
    def test_block_to_blocktype_quote(self):
        md = """> hello
> this is a quote
> right?"""
        block_type = block_to_blocktype(md)
        self.assertEqual(block_type, BlockType.QUOTE)
        
        md2 = """> hello
 this is a quote
> right?"""
        block_type = block_to_blocktype(md2)
        self.assertNotEqual(block_type, BlockType.QUOTE)

    def test_block_to_blocktype_unordered_list(self):
        md = """- hello
- this is a quote
- right?"""
        block_type = block_to_blocktype(md)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)
        
        md2 = """- hello
-this is a quote
- right?"""
        block_type = block_to_blocktype(md2)
        self.assertNotEqual(block_type, BlockType.UNORDERED_LIST)
        
    def test_block_to_blocktype_ordered_list(self):
        md = """1. hello
2. this is a quote
3. right?"""
        block_type = block_to_blocktype(md)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)
        
        md2 = """1. hello
2. this is a quote
2. right?"""
        block_type = block_to_blocktype(md2)
        self.assertNotEqual(block_type, BlockType.ORDERED_LIST)
        
    def test_block_to_blocktype_normal(self):
        md = """hello
2. this is a quote
- right?"""
        block_type = block_to_blocktype(md)
        self.assertEqual(block_type, BlockType.PARAGRAPH)