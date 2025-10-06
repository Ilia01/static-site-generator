import unittest
from utils.extract_title import extract_title


class TestExtractTitle(unittest.TestCase):
    # --- Positive Test Cases ---

    def test_basic_header(self):
        """Test with a simple, valid # header."""
        markdown = "# My Title\n\nSome body text."
        self.assertEqual(extract_title(markdown), "My Title")

    def test_header_with_trailing_spaces(self):
        """Test a header with trailing spaces on the line."""
        markdown = "# My Title   \n\nSome body text."
        self.assertEqual(extract_title(markdown), "My Title")

    def test_header_with_leading_spaces(self):
        """Test a header with leading spaces before the hash mark."""
        markdown = "   # My Title\n\nSome body text."
        self.assertEqual(extract_title(markdown), "My Title")

    def test_no_extra_content_on_line(self):
        """Test a header with no extra content."""
        markdown = "# A\n"
        self.assertEqual(extract_title(markdown), "A")

    # --- Negative Test Cases ---

    def test_no_header(self):
        """Test markdown that contains no header."""
        markdown = "Some body text.\nNo header here."
        with self.assertRaisesRegex(Exception, "There's no header in markdown"):
            extract_title(markdown)

    def test_multi_line_header(self):
        """Test markdown with a valid header on a different line."""
        markdown = "Intro text\n# My Title"
        with self.assertRaisesRegex(Exception, "There's no header in markdown"):
            extract_title(markdown)

    def test_no_header_empty_string(self):
        """Test with an empty string as input."""
        markdown = ""
        with self.assertRaisesRegex(Exception, "There's no header in markdown"):
            extract_title(markdown)

    # --- Edge Cases ---

    def test_no_space_after_hash(self):
        """Test a header without a space after the hash."""
        markdown = "#Title\nBody."
        self.assertEqual(extract_title(markdown), "Title")

    def test_multiple_hashes_raises_exception(self):
        """Test that a multiple-hash header raises an exception."""
        markdown = "## My Subtitle\nBody text."
        with self.assertRaisesRegex(Exception, "There's no header in markdown"):
            extract_title(markdown)

    def test_header_after_body_text_still_fails(self):
        """Test that the exception is still raised if header isn't on the first line."""
        markdown = "Body text...\n# Title"
        with self.assertRaisesRegex(Exception, "There's no header in markdown"):
            extract_title(markdown)

    def test_unicode_characters(self):
        """Test with a header containing Unicode characters."""
        markdown = "# Hér er titill\n"
        self.assertEqual(extract_title(markdown), "Hér er titill")


if __name__ == "__main__":
    unittest.main(argv=["first-arg-is-ignored"], exit=False)
