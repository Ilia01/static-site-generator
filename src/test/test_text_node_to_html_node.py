import unittest
from unittest.mock import Mock, patch

from leafnode import LeafNode
from textnode import TextNode, TextType


from utils.node_to_html import text_node_to_html_node


class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_TEXT_text(self):
        """
        Tests the conversion of a TEXT TextNode to an HTML LeafNode.
        """
        text_node = TextNode("This is TEXT text", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is TEXT text")

    def test_bold_text(self):
        """
        Tests the conversion of a bold TextNode.
        """
        text_node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")

    def test_italic_text(self):
        """
        Tests the conversion of an italic TextNode.
        """
        text_node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")

    def test_code_text(self):
        """
        Tests the conversion of a code TextNode.
        """
        text_node = TextNode("Code block", TextType.CODE)
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "Code block")

    def test_link_text(self):
        """
        Tests the conversion of a link TextNode.
        """
        text_node = TextNode("Link to Google", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Link to Google")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})

    def test_image_text(self):
        """
        Tests the conversion of an image TextNode.
        """
        text_node = TextNode(
            "An image", TextType.IMAGE, "https://example.com/image.jpg"
        )
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")  # Value should be empty for images
        self.assertEqual(
            html_node.props, {"src": "https://example.com/image.jpg", "alt": "An image"}
        )

    def test_unknown_type_raises_error(self):
        """
        Tests that an unknown text type raises a ValueError.
        You'll need a case for this in your match statement, or a separate test.
        """
        with self.assertRaises(Exception):
            text_node_to_html_node(
                Mock(text_type=Mock(value="unknown_type"), text="test")
            )


if __name__ == "__main__":
    unittest.main()
