import unittest
from src.htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        """
        Tests that props_to_html correctly converts a dictionary to an HTML attribute string.
        """
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        expected_html = 'href="https://www.google.com"target="_blank"'
        self.assertEqual(node.props_to_html(), expected_html)

    def test_props_to_html_empty(self):
        """
        Tests that an empty props dictionary results in an empty string.
        """
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_none(self):
        """
        Tests that a None props attribute results in an empty string.
        """
        node = HTMLNode(props=None)
        self.assertEqual(node.props_to_html(), "")

    def test_repr(self):
        """
        Tests the __repr__ method for an HTMLNode with all properties.
        """
        node = HTMLNode(
            "p", "This is a paragraph.", children=[], props={"class": "paragraph"}
        )
        self.assertEqual(
            repr(node),
            "HTMLNode(tag=p, value=This is a paragraph., children=[], props={'class': 'paragraph'})",
        )

    def test_repr_none_properties(self):
        """
        Tests the __repr__ method for a node with some None properties.
        """
        node = HTMLNode(tag="div")
        self.assertEqual(
            repr(node), "HTMLNode(tag=div, value=None, children=None, props=None)"
        )

    def test_to_html_raises_error(self):
        """
        Tests that to_html raises a NotImplementedError.
        """
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()


if __name__ == "__main__":
    unittest.main()
