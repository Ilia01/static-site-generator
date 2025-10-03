import unittest
from src.leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_to_html_with_props(self):
        """
        Tests the conversion to HTML for a standard LeafNode with properties.
        """
        node = LeafNode("p", "This is a paragraph.", {"class": "paragraph"})
        self.assertEqual(
            node.to_html(), '<p class="paragraph">This is a paragraph.</p>'
        )

    def test_to_html_without_props(self):
        """
        Tests the conversion to HTML for a LeafNode with no properties.
        """
        node = LeafNode("span", "Just a span.")
        self.assertEqual(node.to_html(), "<span>Just a span.</span>")

    def test_to_html_no_tag_value(self):
        """
        Tests the case where a LeafNode has no tag (should return only its value).
        """
        node = LeafNode(None, "This is TEXT text.")
        self.assertEqual(node.to_html(), "This is TEXT text.")

    def test_to_html_raises_error_no_value(self):
        """
        Tests that to_html raises a ValueError if the value is None.
        """
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_with_multiple_props(self):
        """
        Tests conversion for a node with multiple properties.
        """
        props = {"href": "https://example.com", "target": "_blank"}
        node = LeafNode("a", "Click me!", props)
        expected_html = '<a href="https://example.com"target="_blank">Click me!</a>'
        self.assertEqual(node.to_html(), expected_html)

    def test_to_html_with_special_characters(self):
        """
        Tests that the value containing special HTML characters is rendered correctly.
        """
        node = LeafNode("p", "Text with > and < symbols.")
        self.assertEqual(node.to_html(), "<p>Text with > and < symbols.</p>")

    def test_repr(self):
        """
        Tests the __repr__ method for a LeafNode.
        """
        node = LeafNode("h1", "Title", {"id": "main-title"})
        self.assertEqual(
            repr(node),
            "HTMLNode(tag=h1, value=Title, children=None, props={'id': 'main-title'})",
        )


if __name__ == "__main__":
    unittest.main()
