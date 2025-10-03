import unittest
import re
from src.utils.extract_markdown import extract_markdown_images, extract_markdown_links


class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images_with_multiple_matches(self):
        """
        Tests extracting multiple markdown images from a single string.
        """
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_links_with_multiple_matches(self):
        """
        Tests extracting multiple markdown links from a single string.
        """
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        expected = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_extract_markdown_images_single_match(self):
        """
        Tests extracting a single image.
        """
        text = "An image: ![An image](http://example.com/image.png)"
        expected = [("An image", "http://example.com/image.png")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_links_single_match(self):
        """
        Tests extracting a single link.
        """
        text = "A link: [A link](http://example.com/link)"
        expected = [("A link", "http://example.com/link")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_extract_markdown_images_no_match(self):
        """
        Tests a string with no images.
        """
        text = "This is just plain text."
        expected = []
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_links_no_match(self):
        """
        Tests a string with no links.
        """
        text = "This is text with an image ![image](url)."
        expected = []
        self.assertEqual(extract_markdown_links(text), expected)

    def test_extract_markdown_images_empty_text(self):
        """
        Tests an empty string for images.
        """
        text = ""
        expected = []
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_links_empty_text(self):
        """
        Tests an empty string for links.
        """
        text = ""
        expected = []
        self.assertEqual(extract_markdown_links(text), expected)

    def test_extract_markdown_images_edge_case(self):
        """
        Tests an image with empty alt text and empty URL.
        """
        text = "An empty image: ![]()"
        expected = [("", "")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_links_edge_case(self):
        """
        Tests a link with empty link text and empty URL.
        """
        text = "An empty link: []()"
        expected = [("", "")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_extract_markdown_links_combined_with_images(self):
        """
        Tests that `extract_markdown_links` correctly ignores images.
        """
        text = "An image ![image](url) and a link [link](url)"
        expected = [("link", "url")]
        self.assertEqual(extract_markdown_links(text), expected)


if __name__ == "__main__":
    unittest.main()
