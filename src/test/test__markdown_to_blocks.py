import unittest
from utils.markdown_to_blocks import markdown_to_blocks


class TestMarkdownToBlock(unittest.TestCase):

    def test_simple_blocks(self):
        """Tests standard markdown with multiple blocks separated by newlines."""
        markdown = "This is block one.\n\nThis is block two."
        expected = ["This is block one.", "This is block two."]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_strips_leading_and_trailing_whitespace(self):
        """Tests that leading and trailing whitespace are stripped from blocks."""
        markdown = "  This is a block.  \n\n\n  Another block.  "
        expected = ["This is a block.", "Another block."]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_handles_single_block_correctly(self):
        """Tests a markdown string containing only a single block."""
        markdown = "This is a single block."
        expected = ["This is a single block."]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_handles_complex_block_structure(self):
        """Tests a complex case with multiple blocks and line breaks within blocks."""
        markdown = """# Heading

This is some regular text.
This is still the same block.

- List item one.
- List item two."""
        expected = [
            "# Heading",
            "This is some regular text.\nThis is still the same block.",
            "- List item one.\n- List item two.",
        ]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_handles_extra_blank_lines_gracefully(self):
        """Tests that multiple blank lines between blocks are handled correctly."""
        markdown = "Block one.\n\n\n\nBlock two."
        expected = ["Block one.", "Block two."]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_empty_input_produces_empty_list(self):
        """Tests that an empty input string produces an empty list."""
        markdown = ""
        expected = []
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_input_with_only_whitespace(self):
        """Tests an input string containing only whitespace."""
        markdown = "     \n\n\n   "
        expected = []
        self.assertEqual(markdown_to_blocks(markdown), expected)


if __name__ == "__main__":
    unittest.main()
