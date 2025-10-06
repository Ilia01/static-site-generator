import unittest
from utils.split_nodes import split_nodes_delimiter
from textnode import TextType, TextNode


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_single_node_bold(self):
        """Test a single node with a bold delimiter."""
        input_nodes = [TextNode("This is a **bold** node.", TextType.TEXT)]
        delimiter = "**"
        text_type = TextType.BOLD
        expected_nodes = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" node.", TextType.TEXT),
        ]
        result_nodes = split_nodes_delimiter(input_nodes, delimiter, text_type)
        self.assertEqual(result_nodes, expected_nodes)

    def test_single_node_italic(self):
        """Test a single node with an italic delimiter."""
        input_nodes = [TextNode("This is an *italic* node.", TextType.TEXT)]
        delimiter = "*"
        text_type = TextType.ITALIC
        expected_nodes = [
            TextNode("This is an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" node.", TextType.TEXT),
        ]
        result_nodes = split_nodes_delimiter(input_nodes, delimiter, text_type)
        self.assertEqual(result_nodes, expected_nodes)

    def test_multiple_nodes_mixed_delimiter(self):
        """Test multiple nodes with different delimiters."""
        input_nodes = [
            TextNode("Some `code` here.", TextType.TEXT),
            TextNode("More *italic* text.", TextType.TEXT),
        ]
        delimiter = "`"
        text_type = TextType.CODE
        expected_nodes = [
            TextNode("Some ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" here.", TextType.TEXT),
            TextNode("More *italic* text.", TextType.TEXT),
        ]
        result_nodes = split_nodes_delimiter(input_nodes, delimiter, text_type)
        self.assertEqual(result_nodes, expected_nodes)

    def test_delimiter_at_start(self):
        """Test when the delimiter is at the beginning of the text."""
        input_nodes = [TextNode("**Bold** at the start.", TextType.TEXT)]
        delimiter = "**"
        text_type = TextType.BOLD
        expected_nodes = [
            TextNode("Bold", TextType.BOLD),
            TextNode(" at the start.", TextType.TEXT),
        ]
        result_nodes = split_nodes_delimiter(input_nodes, delimiter, text_type)
        self.assertEqual(result_nodes, expected_nodes)

    def test_delimiter_at_end(self):
        """Test when the delimiter is at the end of the text."""
        input_nodes = [TextNode("Bold at the end **bold**", TextType.TEXT)]
        delimiter = "**"
        text_type = TextType.BOLD
        expected_nodes = [
            TextNode("Bold at the end ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
        ]
        result_nodes = split_nodes_delimiter(input_nodes, delimiter, text_type)
        self.assertEqual(result_nodes, expected_nodes)

    def test_multiple_delimiters_in_one_node(self):
        """Test splitting multiple times within a single node."""
        input_nodes = [TextNode("Some **bold** and **more bold**.", TextType.TEXT)]
        delimiter = "**"
        text_type = TextType.BOLD
        expected_nodes = [
            TextNode("Some ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("more bold", TextType.BOLD),
            TextNode(".", TextType.TEXT),
        ]
        result_nodes = split_nodes_delimiter(input_nodes, delimiter, text_type)
        self.assertEqual(result_nodes, expected_nodes)

    def test_invalid_syntax_exception(self):
        """Test that an exception is raised for odd-numbered delimiters."""
        input_nodes = [TextNode("Text with **bold", TextType.TEXT)]
        delimiter = "**"
        text_type = TextType.BOLD
        with self.assertRaisesRegex(
            Exception, "No pair delimiter found, invalid syntax"
        ):
            split_nodes_delimiter(input_nodes, delimiter, text_type)

    def test_no_delimiter_match(self):
        """Test that nodes without delimiters are returned unchanged."""
        input_nodes = [TextNode("No special formatting here.", TextType.TEXT)]
        delimiter = "**"
        text_type = TextType.BOLD
        expected_nodes = [TextNode("No special formatting here.", TextType.TEXT)]
        result_nodes = split_nodes_delimiter(input_nodes, delimiter, text_type)
        self.assertEqual(result_nodes, expected_nodes)

    def test_unaffected_node_types(self):
        """Test that non-TEXT nodes are not processed by the function."""
        input_nodes = [
            TextNode("Text with **bold**.", TextType.TEXT),
            TextNode("A link", TextType.LINK, url="https://example.com"),
        ]
        delimiter = "**"
        text_type = TextType.BOLD
        expected_nodes = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(".", TextType.TEXT),
            TextNode("A link", TextType.LINK, url="https://example.com"),
        ]
        result_nodes = split_nodes_delimiter(input_nodes, delimiter, text_type)
        self.assertEqual(result_nodes, expected_nodes)


if __name__ == "__main__":
    unittest.main()
