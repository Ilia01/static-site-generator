import unittest
from unittest.mock import patch, MagicMock

from utils.markdown_to_htmlnode import (
    markdown_to_html_node,
    _paragraph_to_html,
    _heading_to_html,
    _code_to_html,
    _quote_to_html,
    _unordered_list_to_html,
    _ordered_list_to_html,
)
from parentnode import ParentNode
from blocktype import BlockType
from leafnode import LeafNode


class TestHtmlNodeConversion(unittest.TestCase):
    """Test suite for HTML node conversion helper functions."""

    def test_paragraph_to_html(self):
        """Tests that a paragraph block is correctly converted to a ParentNode with a <p> tag."""
        with patch(" utils.markdown_to_htmlnode.text_to_textnodes") as mock_t2t, patch(
            " utils.markdown_to_htmlnode.text_node_to_html_node",
            side_effect=lambda n: n,
        ):
            mock_node = MagicMock()
            mock_t2t.return_value = [mock_node]
            result = _heading_to_html("### This is a heading.")
            self.assertEqual(result.tag, "h3")
            self.assertEqual(result.children, [mock_node])
        mock_t2t.assert_called_once_with("This is a heading.")

    def test_code_to_html(self):
        """Tests that a code block is correctly converted, with no inline parsing."""
        block = "```\ndef func():\n  return 'code'\n```"
        result = _code_to_html(block)
        self.assertIsInstance(result, ParentNode)
        self.assertEqual(result.tag, "pre")
        self.assertEqual(len(result.children), 1)
        self.assertIsInstance(result.children[0], ParentNode)
        self.assertEqual(result.children[0].tag, "code")
        self.assertEqual(len(result.children[0].children), 1)
        self.assertIsInstance(result.children[0].children[0], LeafNode)
        self.assertEqual(
            result.children[0].children[0].value, "def func():\n  return 'code'"
        )

    def test_quote_to_html(self):
        """Tests that a quote block is correctly converted to a <blockquote> tag."""
        block = "> This is a quote.\n> Spanning two lines."
        with patch(" utils.markdown_to_htmlnode.text_to_textnodes") as mock_t2t, patch(
            " utils.markdown_to_htmlnode.text_node_to_html_node",
            side_effect=lambda n: n,
        ):
            mock_child = MagicMock()
            mock_t2t.return_value = [mock_child]
            result = _quote_to_html(block)
            self.assertEqual(result.tag, "blockquote")
            self.assertEqual(result.children, [mock_child])
            mock_t2t.assert_called_once_with("This is a quote.\nSpanning two lines.")

    def test_unordered_list_to_html(self):
        """Tests that an unordered list is correctly converted to a <ul> tag with <li> children."""
        block = "- First item\n- Second item"
        with patch(
            " utils.text_textnodes.text_to_textnodes",
            side_effect=lambda t: [LeafNode(tag=None, value=t)],
        ) as mock_text_to_textnodes:
            result = _unordered_list_to_html(block)
            self.assertIsInstance(result, ParentNode)
            self.assertEqual(result.tag, "ul")
            self.assertEqual(len(result.children), 2)
            self.assertEqual(result.children[0].tag, "li")
            self.assertEqual(result.children[0].children[0].value, "First item")
            self.assertEqual(result.children[1].tag, "li")
            self.assertEqual(result.children[1].children[0].value, "Second item")

    def test_ordered_list_to_html(self):
        """Tests that an ordered list is correctly converted to an <ol> tag with <li> children."""
        block = "1. First item\n2. Second item"
        with patch(
            " utils.text_textnodes.text_to_textnodes",
            side_effect=lambda t: [LeafNode(tag=None, value=t)],
        ) as mock_text_to_textnodes:
            result = _ordered_list_to_html(block)
            self.assertIsInstance(result, ParentNode)
            self.assertEqual(result.tag, "ol")
            self.assertEqual(len(result.children), 2)
            self.assertEqual(result.children[0].tag, "li")
            self.assertEqual(result.children[0].children[0].value, "First item")
            self.assertEqual(result.children[1].tag, "li")
            self.assertEqual(result.children[1].children[0].value, "Second item")


class TestMarkdownToHtmlNode(unittest.TestCase):
    """Test suite for the main markdown_to_html_node function, using mocks for dependencies."""

    @patch(" utils.markdown_to_htmlnode.markdown_to_blocks")
    @patch(" utils.markdown_to_htmlnode.block_to_block_type")
    @patch(" utils.markdown_to_htmlnode._paragraph_to_html")
    @patch(" utils.markdown_to_htmlnode._heading_to_html")
    def test_markdown_to_html_node_precedence(
        self,
        mock_heading_handler,
        mock_paragraph_handler,
        mock_block_to_block_type,
        mock_markdown_to_blocks,
    ):
        """Tests that markdown_to_html_node calls the correct handlers in sequence."""
        markdown = "## Heading\n\nParagraph"
        mock_markdown_to_blocks.return_value = ["## Heading", "Paragraph"]

        mock_block_to_block_type.side_effect = [
            BlockType.HEADING,
            BlockType.PARAGRAPH,
        ]

        mock_heading_handler.return_value = ParentNode("h2", [])
        mock_paragraph_handler.return_value = ParentNode("p", [])

        result = markdown_to_html_node(markdown)

        self.assertIsInstance(result, ParentNode)
        self.assertEqual(result.tag, "div")
        self.assertEqual(len(result.children), 2)

        mock_markdown_to_blocks.assert_called_once_with(markdown)
        mock_block_to_block_type.assert_any_call("## Heading")
        mock_block_to_block_type.assert_any_call("Paragraph")
        mock_heading_handler.assert_called_once_with("## Heading")
        mock_paragraph_handler.assert_called_once_with("Paragraph")

    @patch(" utils.markdown_to_blocks.markdown_to_blocks")
    @patch(" utils.block_to_block_type.block_to_block_type")
    def test_markdown_to_html_node_full_conversion(
        self, mock_block_to_block_type, mock_markdown_to_blocks
    ):
        """Tests the full conversion flow with a simple, integrated test."""
        markdown = "# H1\n\n- list item"
        mock_markdown_to_blocks.return_value = ["# H1", "- list item"]
        mock_block_to_block_type.side_effect = [
            BlockType.HEADING,
            BlockType.UNORDERED_LIST,
        ]

        with patch(
            " utils.text_textnodes.text_to_textnodes",
            side_effect=lambda text: [LeafNode(tag=None, value=text)],
        ):
            result = markdown_to_html_node(markdown)

            self.assertIsInstance(result, ParentNode)
            self.assertEqual(result.tag, "div")
            self.assertEqual(len(result.children), 2)
            self.assertEqual(result.children[0].tag, "h1")
            self.assertEqual(result.children[0].children[0].value, "H1")
            self.assertEqual(result.children[1].tag, "ul")
            self.assertEqual(result.children[1].children[0].tag, "li")
            self.assertEqual(
                result.children[1].children[0].children[0].value, "list item"
            )


if __name__ == "__main__":
    unittest.main()
