import unittest
from unittest.mock import patch, Mock

from textnode import TextType, TextNode
from utils.text_textnodes import text_to_textnodes


class TestTextToTextNodes(unittest.TestCase):

    @patch(" utils.split_nodes.split_nodes_delimiter")
    @patch(" utils.split_nodes.split_nodes_link")
    @patch(" utils.split_nodes.split_nodes_image")
    def test_text_to_textnodes_basic(
        self, mock_split_image, mock_split_link, mock_split_delimiter
    ):
        """Test a simple text with no markdown."""
        text = "This is a simple text."
        initial_node = TextNode(text, TextType.TEXT)

        mock_split_image.return_value = [initial_node]
        mock_split_link.return_value = [initial_node]
        mock_split_delimiter.return_value = [initial_node]

        result = text_to_textnodes(text)

        self.assertEqual(result, [initial_node])

    @patch(" utils.split_nodes.split_nodes_delimiter")
    @patch(" utils.split_nodes.split_nodes_link")
    @patch(" utils.split_nodes.split_nodes_image")
    def test_text_to_textnodes_with_image(
        self, mock_split_image, mock_split_link, mock_split_delimiter
    ):
        """Test text containing an image."""
        text = "Text with ![image](url)"
        image_node = TextNode("image", TextType.IMAGE, "url")
        text_node = TextNode("Text with ", TextType.TEXT)

        mock_split_image.return_value = [text_node, image_node]
        mock_split_link.return_value = [text_node, image_node]
        mock_split_delimiter.return_value = [text_node, image_node]

        result = text_to_textnodes(text)

        self.assertEqual(result, [text_node, image_node])

    @patch(" utils.split_nodes.split_nodes_delimiter")
    @patch(" utils.split_nodes.split_nodes_link")
    @patch(" utils.split_nodes.split_nodes_image")
    def test_text_to_textnodes_with_link(
        self, mock_split_image, mock_split_link, mock_split_delimiter
    ):
        """Test text containing a link."""
        text = "Text with [link](url)"
        link_node = TextNode("link", TextType.LINK, "url")
        text_node = TextNode("Text with ", TextType.TEXT)

        mock_split_image.return_value = [text_node, link_node]
        mock_split_link.return_value = [text_node, link_node]
        mock_split_delimiter.return_value = [text_node, link_node]

        result = text_to_textnodes(text)

        self.assertEqual(result, [text_node, link_node])

    @patch(" utils.split_nodes.split_nodes_delimiter")
    @patch(" utils.split_nodes.split_nodes_link")
    @patch(" utils.split_nodes.split_nodes_image")
    def test_text_to_textnodes_with_bold(
        self, mock_split_image, mock_split_link, mock_split_delimiter
    ):
        """Test text containing bold formatting."""
        text = "Text with **bold** text."
        bold_node = TextNode("bold", TextType.BOLD)
        text_node1 = TextNode("Text with ", TextType.TEXT)
        text_node2 = TextNode(" text.", TextType.TEXT)

        mock_split_image.return_value = [text_node1, bold_node, text_node2]
        mock_split_link.return_value = [text_node1, bold_node, text_node2]
        mock_split_delimiter.return_value = [text_node1, bold_node, text_node2]

        result = text_to_textnodes(text)

        self.assertEqual(result, [text_node1, bold_node, text_node2])

    @patch(" utils.split_nodes.split_nodes_delimiter")
    @patch(" utils.split_nodes.split_nodes_link")
    @patch(" utils.split_nodes.split_nodes_image")
    def test_text_to_textnodes_full_monty(
        self, mock_split_image, mock_split_link, mock_split_delimiter
    ):
        """Test a complex text with all markdown types."""
        text = "Text **with** a [link](url), an ![image](url2), and `code`."

        final_nodes = [
            TextNode("Text ", TextType.TEXT),
            TextNode("with", TextType.BOLD),
            TextNode(" a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url"),
            TextNode(", an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "url2"),
            TextNode(", and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(".", TextType.TEXT),
        ]

        # Configure mocks to simulate the correct order of operations
        mock_split_image.return_value = [
            TextNode("Text **with** a [link](url), an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "url2"),
            TextNode(", and `code`.", TextType.TEXT),
        ]
        mock_split_link.return_value = [
            TextNode("Text **with** a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url"),
            TextNode(", an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "url2"),
            TextNode(", and `code`.", TextType.TEXT),
        ]
        mock_split_delimiter.side_effect = [
            # First delimiter pass (Code)
            [
                TextNode("Text **with** a [link](url), an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "url2"),
                TextNode(", and ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(".", TextType.TEXT),
            ],
            # Second delimiter pass (Italic)
            [
                TextNode("Text **with** a [link](url), an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "url2"),
                TextNode(", and ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(".", TextType.TEXT),
            ],
            # Third delimiter pass (Bold)
            final_nodes,
        ]

        result = text_to_textnodes(text)
        self.assertEqual(result, final_nodes)


if __name__ == "__main__":
    unittest.main()
