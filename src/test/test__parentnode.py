import unittest
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    def test_to_html_single_level(self):
        """
        Tests to_html for a ParentNode with simple LeafNode children.
        """
        children = [
            LeafNode("span", "child 1"),
            LeafNode("span", "child 2"),
        ]
        parent = ParentNode("div", children)
        expected_html = "<div><span>child 1</span><span>child 2</span></div>"
        self.assertEqual(parent.to_html(), expected_html)

    def test_to_html_nested(self):
        """
        Tests to_html for a ParentNode with nested ParentNode children.
        """
        # Inner parent node
        inner_children = [
            LeafNode("b", "inner child 1"),
            LeafNode("i", "inner child 2"),
        ]
        inner_parent = ParentNode("p", inner_children)

        # Outer parent node
        outer_children = [
            LeafNode("a", "outer child 1"),
            inner_parent,
            LeafNode("span", "outer child 2"),
        ]
        outer_parent = ParentNode("div", outer_children)

        expected_html = "<div><a>outer child 1</a><p><b>inner child 1</b><i>inner child 2</i></p><span>outer child 2</span></div>"
        self.assertEqual(outer_parent.to_html(), expected_html)

    def test_to_html_with_props(self):
        """
        Tests to_html for a ParentNode with properties.
        """
        children = [LeafNode("p", "A child node.")]
        parent = ParentNode("div", children, props={"class": "container"})
        expected_html = '<div class="container"><p>A child node.</p></div>'
        self.assertEqual(parent.to_html(), expected_html)

    def test_to_html_no_tag_raises_error(self):
        """
        Tests that to_html raises a ValueError if the tag is None.
        """
        parent = ParentNode(None, [LeafNode("p", "Child.")])
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_to_html_no_children_raises_error(self):
        """
        Tests that to_html raises a ValueError if children is None.
        """
        parent = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_to_html_empty_children_list(self):
        """
        Tests that an empty children list results in an empty tag.
        """
        parent = ParentNode("ul", [])
        self.assertEqual(parent.to_html(), "<ul></ul>")

    def test_repr(self):
        """
        Tests the __repr__ method for a ParentNode.
        """
        children = [LeafNode("p", "Child.")]
        parent = ParentNode("div", children, props={"id": "main"})
        expected_repr_start = "HTMLNode(tag=div, value=None, children=["
        expected_repr_end = "], props={'id': 'main'})"
        self.assertTrue(repr(parent).startswith(expected_repr_start))
        self.assertTrue(repr(parent).endswith(expected_repr_end))


if __name__ == "__main__":
    unittest.main()
