import unittest
from unittest.mock import patch

from utils.split_nodes import split_nodes_image, split_nodes_link
from textnode import TextType, TextNode


class TestSplitNodes(unittest.TestCase):

    # --- Tests for split_nodes_image ---

    @patch(" utils.split_nodes.extract_markdown_images")
    def test_split_nodes_image_single(self, mock_extract_images):
        """Test splitting a single node with one image."""
        mock_extract_images.return_value = [("img", "url")]
        old_nodes = [TextNode("text with image ![img](url) at the end", TextType.TEXT)]
        expected = [
            TextNode("text with image ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "url"),
            TextNode(" at the end", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_image(old_nodes), expected)

    @patch(" utils.split_nodes.extract_markdown_images")
    def test_split_nodes_image_multiple(self, mock_extract_images):
        """Test splitting a single node with multiple images."""
        mock_extract_images.return_value = [("img1", "url1"), ("img2", "url2")]
        old_nodes = [TextNode("![img1](url1) text ![img2](url2)", TextType.TEXT)]
        expected = [
            TextNode("img1", TextType.IMAGE, "url1"),
            TextNode(" text ", TextType.TEXT),
            TextNode("img2", TextType.IMAGE, "url2"),
        ]
        self.assertEqual(split_nodes_image(old_nodes), expected)

    @patch(" utils.split_nodes.extract_markdown_images")
    def test_split_nodes_image_no_image(self, mock_extract_images):
        """Test a node with no image markdown."""
        mock_extract_images.return_value = []
        old_nodes = [TextNode("text with no images", TextType.TEXT)]
        expected = [TextNode("text with no images", TextType.TEXT)]
        self.assertEqual(split_nodes_image(old_nodes), expected)

    @patch(" utils.split_nodes.extract_markdown_images")
    def test_split_nodes_image_multiple_nodes(self, mock_extract_images):
        """Test splitting a list of nodes where some have images."""
        mock_extract_images.side_effect = [[("img1", "url1")], [], [("img2", "url2")]]
        old_nodes = [
            TextNode("This has ![img1](url1)", TextType.TEXT),
            TextNode("This does not.", TextType.TEXT),
            TextNode("This has ![img2](url2) at the end.", TextType.TEXT),
        ]
        expected = [
            TextNode("This has ", TextType.TEXT),
            TextNode("img1", TextType.IMAGE, "url1"),
            TextNode("This does not.", TextType.TEXT),
            TextNode("This has ", TextType.TEXT),
            TextNode("img2", TextType.IMAGE, "url2"),
            TextNode(" at the end.", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_image(old_nodes), expected)

    @patch(" utils.split_nodes.extract_markdown_images")
    def test_split_nodes_image_existing_node(self, mock_extract_images):
        """Test that non-text nodes are passed through unchanged."""
        mock_extract_images.side_effect = [[("img", "url")], [], []]
        old_nodes = [
            TextNode("Text with ![img](url)", TextType.TEXT),
            TextNode("Already bold", TextType.BOLD),
            TextNode("Plain text", TextType.TEXT),
        ]
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "url"),
            TextNode("Already bold", TextType.BOLD),
            TextNode("Plain text", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_image(old_nodes), expected)

    # --- Tests for split_nodes_link ---

    @patch(" utils.split_nodes.extract_markdown_links")
    def test_split_nodes_link_single(self, mock_extract_links):
        """Test splitting a single node with one link."""
        mock_extract_links.return_value = [("link", "url")]
        old_nodes = [TextNode("text with a [link](url)", TextType.TEXT)]
        expected = [
            TextNode("text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url"),
        ]
        self.assertEqual(split_nodes_link(old_nodes), expected)

    @patch(" utils.split_nodes.extract_markdown_links")
    def test_split_nodes_link_multiple(self, mock_extract_links):
        """Test splitting a single node with multiple links."""
        mock_extract_links.return_value = [("link1", "url1"), ("link2", "url2")]
        old_nodes = [TextNode("[link1](url1) text [link2](url2)", TextType.TEXT)]
        expected = [
            TextNode("link1", TextType.LINK, "url1"),
            TextNode(" text ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "url2"),
        ]
        self.assertEqual(split_nodes_link(old_nodes), expected)

    @patch(" utils.split_nodes.extract_markdown_links")
    def test_split_nodes_link_no_link(self, mock_extract_links):
        """Test a node with no link markdown."""
        mock_extract_links.return_value = []
        old_nodes = [TextNode("text with no links", TextType.TEXT)]
        expected = [TextNode("text with no links", TextType.TEXT)]
        self.assertEqual(split_nodes_link(old_nodes), expected)

    @patch(" utils.split_nodes.extract_markdown_links")
    def test_split_nodes_link_multiple_nodes(self, mock_extract_links):
        """Test splitting a list of nodes where some have links."""
        mock_extract_links.side_effect = [[("link1", "url1")], [], [("link2", "url2")]]
        old_nodes = [
            TextNode("This has [link1](url1)", TextType.TEXT),
            TextNode("This does not.", TextType.TEXT),
            TextNode("This has [link2](url2) at the end.", TextType.TEXT),
        ]
        expected = [
            TextNode("This has ", TextType.TEXT),
            TextNode("link1", TextType.LINK, "url1"),
            TextNode("This does not.", TextType.TEXT),
            TextNode("This has ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "url2"),
            TextNode(" at the end.", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_link(old_nodes), expected)

    @patch(" utils.split_nodes.extract_markdown_links")
    def test_split_nodes_link_existing_node(self, mock_extract_links):
        """Test that non-text nodes are passed through unchanged."""
        mock_extract_links.side_effect = [[("link", "url")], [], []]
        old_nodes = [
            TextNode("Text with [link](url)", TextType.TEXT),
            TextNode("Already bold", TextType.BOLD),
            TextNode("Plain text", TextType.TEXT),
        ]
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url"),
            TextNode("Already bold", TextType.BOLD),
            TextNode("Plain text", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_link(old_nodes), expected)

    # --- Additional Tests for Edge Cases ---

    @patch(" utils.split_nodes.extract_markdown_images")
    def test_split_nodes_image_multiple_interleaved(self, mock_extract_images):
        """Test multiple interleaved images."""
        mock_extract_images.return_value = [
            ("img1", "url1"),
            ("img2", "url2"),
            ("img3", "url3"),
        ]
        old_nodes = [
            TextNode(
                "before ![img1](url1) mid ![img2](url2) end ![img3](url3)",
                TextType.TEXT,
            )
        ]
        expected = [
            TextNode("before ", TextType.TEXT),
            TextNode("img1", TextType.IMAGE, "url1"),
            TextNode(" mid ", TextType.TEXT),
            TextNode("img2", TextType.IMAGE, "url2"),
            TextNode(" end ", TextType.TEXT),
            TextNode("img3", TextType.IMAGE, "url3"),
        ]
        self.assertEqual(split_nodes_image(old_nodes), expected)

    @patch(" utils.split_nodes.extract_markdown_links")
    def test_split_nodes_link_multiple_interleaved(self, mock_extract_links):
        """Test multiple interleaved links."""
        mock_extract_links.return_value = [
            ("link1", "url1"),
            ("link2", "url2"),
            ("link3", "url3"),
        ]
        old_nodes = [
            TextNode(
                "before [link1](url1) mid [link2](url2) end [link3](url3)",
                TextType.TEXT,
            )
        ]
        expected = [
            TextNode("before ", TextType.TEXT),
            TextNode("link1", TextType.LINK, "url1"),
            TextNode(" mid ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "url2"),
            TextNode(" end ", TextType.TEXT),
            TextNode("link3", TextType.LINK, "url3"),
        ]
        self.assertEqual(split_nodes_link(old_nodes), expected)

    @patch(" utils.split_nodes.extract_markdown_images")
    def test_split_nodes_image_no_match_returns_same_object(self, mock_extract_images):
        """Test that if no match is found, the original node object is returned."""
        mock_extract_images.return_value = []
        node = TextNode("text with no images", TextType.TEXT)
        old_nodes = [node]
        result = split_nodes_image(old_nodes)
        self.assertEqual(result, [node])
        self.assertIs(result[0], node)

    @patch(" utils.split_nodes.extract_markdown_links")
    def test_split_nodes_link_no_match_returns_same_object(self, mock_extract_links):
        """Test that if no match is found, the original node object is returned."""
        mock_extract_links.return_value = []
        node = TextNode("text with no links", TextType.TEXT)
        old_nodes = [node]
        result = split_nodes_link(old_nodes)
        self.assertEqual(result, [node])
        self.assertIs(result[0], node)


if __name__ == "__main__":
    unittest.main()
