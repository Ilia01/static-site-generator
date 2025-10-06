import unittest
from unittest.mock import patch, MagicMock
from utils.block_to_block_type import (
    block_to_block_type,
    is_code_block,
    is_heading,
    is_ordered_list,
    is_quote,
    is_unordered_list,
)
from blocktype import BlockType


class TestBlockAnalyzer(unittest.TestCase):
    """
    Test suite for the block_to_block_type function, with mocking.
    """

    # --- Test cases for block_to_block_type using mock helpers ---

    @patch(" utils.block_to_block_type.is_heading", return_value=True)
    def test_block_to_block_type_heading_precedence(self, mock_is_heading):
        """Test that is_heading is checked first and returns HEADING."""
        block = "### A heading that could also be a paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        mock_is_heading.assert_called_once_with(block)

    @patch(" utils.block_to_block_type.is_heading", return_value=False)
    @patch(" utils.block_to_block_type.is_code_block", return_value=True)
    def test_block_to_block_type_code_precedence(
        self, mock_is_code_block, mock_is_heading
    ):
        """Test that is_code_block is checked after is_heading."""
        block = "```code block```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        mock_is_heading.assert_called_once_with(block)
        mock_is_code_block.assert_called_once_with(block)

    @patch(" utils.block_to_block_type.is_heading", return_value=False)
    @patch(" utils.block_to_block_type.is_code_block", return_value=False)
    @patch(" utils.block_to_block_type.is_quote", return_value=True)
    def test_block_to_block_type_quote_precedence(
        self, mock_is_quote, mock_is_code_block, mock_is_heading
    ):
        """Test that is_quote is checked after code."""
        block = "> A quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        mock_is_heading.assert_called_once_with(block)
        mock_is_code_block.assert_called_once_with(block)
        mock_is_quote.assert_called_once_with(block)

    @patch(" utils.block_to_block_type.is_heading", return_value=False)
    @patch(" utils.block_to_block_type.is_code_block", return_value=False)
    @patch(" utils.block_to_block_type.is_quote", return_value=False)
    @patch(" utils.block_to_block_type.is_unordered_list", return_value=True)
    def test_block_to_block_type_unordered_list_precedence(
        self, mock_is_unordered_list, mock_is_quote, mock_is_code_block, mock_is_heading
    ):
        """Test that is_unordered_list is checked after quote."""
        block = "- An item"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        mock_is_heading.assert_called_once_with(block)
        mock_is_code_block.assert_called_once_with(block)
        mock_is_quote.assert_called_once_with(block)
        mock_is_unordered_list.assert_called_once_with(block)

    @patch(" utils.block_to_block_type.is_heading", return_value=False)
    @patch(" utils.block_to_block_type.is_code_block", return_value=False)
    @patch(" utils.block_to_block_type.is_quote", return_value=False)
    @patch(" utils.block_to_block_type.is_unordered_list", return_value=False)
    @patch(" utils.block_to_block_type.is_ordered_list", return_value=True)
    def test_block_to_block_type_ordered_list_precedence(
        self,
        mock_is_ordered_list,
        mock_is_unordered_list,
        mock_is_quote,
        mock_is_code_block,
        mock_is_heading,
    ):
        """Test that is_ordered_list is checked after unordered list."""
        block = "1. An item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        mock_is_heading.assert_called_once_with(block)
        mock_is_code_block.assert_called_once_with(block)
        mock_is_quote.assert_called_once_with(block)
        mock_is_unordered_list.assert_called_once_with(block)
        mock_is_ordered_list.assert_called_once_with(block)

    @patch(" utils.block_to_block_type.is_heading", return_value=False)
    @patch(" utils.block_to_block_type.is_code_block", return_value=False)
    @patch(" utils.block_to_block_type.is_quote", return_value=False)
    @patch(" utils.block_to_block_type.is_unordered_list", return_value=False)
    @patch(" utils.block_to_block_type.is_ordered_list", return_value=False)
    def test_block_to_block_type_paragraph_default(
        self,
        mock_is_ordered_list,
        mock_is_unordered_list,
        mock_is_quote,
        mock_is_code_block,
        mock_is_heading,
    ):
        """Test that a block with no matches falls back to a paragraph."""
        block = "A simple paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        mock_is_heading.assert_called_once_with(block)
        mock_is_code_block.assert_called_once_with(block)
        mock_is_quote.assert_called_once_with(block)
        mock_is_unordered_list.assert_called_once_with(block)
        mock_is_ordered_list.assert_called_once_with(block)

    # --- Test cases for individual helper functions (no mocking needed) ---

    def test_is_heading_valid(self):
        """Test that is_heading works for valid heading syntax."""
        for i in range(1, 7):
            self.assertTrue(is_heading(f"{'#' * i} A heading"))

    def test_is_heading_invalid(self):
        """Test that is_heading correctly identifies invalid syntax."""
        self.assertFalse(is_heading("####### Too many hashes"))
        self.assertFalse(is_heading("#No space after hash"))
        self.assertFalse(is_heading("Not a heading"))

    def test_is_code_block_valid(self):
        """Test that is_code_block works for valid code block syntax."""
        self.assertTrue(is_code_block("```code block```"))
        self.assertTrue(is_code_block("```\nmulti-line\ncode\n```"))

    def test_is_code_block_invalid(self):
        """Test that is_code_block correctly identifies invalid syntax."""
        self.assertFalse(is_code_block("`single backtick`"))
        self.assertFalse(is_code_block("```no closing backticks"))
        self.assertFalse(is_code_block("no opening backticks```"))

    def test_is_quote_valid(self):
        """Test that is_quote works for valid quote syntax."""
        self.assertTrue(is_quote("> A single line quote"))
        self.assertTrue(is_quote("> A multi-line\n> quote"))

    def test_is_quote_invalid(self):
        """Test that is_quote correctly identifies invalid syntax."""
        self.assertFalse(is_quote("Not a > quote"))
        self.assertFalse(is_quote("> This is fine\nNot a quote"))

    def test_is_unordered_list_valid(self):
        """Test that is_unordered_list works for valid list syntax."""
        self.assertTrue(is_unordered_list("- Item 1\n- Item 2"))
        self.assertTrue(is_unordered_list("- Single item"))

    def test_is_unordered_list_invalid(self):
        """Test that is_unordered_list correctly identifies invalid syntax."""
        self.assertFalse(is_unordered_list("* Not a valid character"))
        self.assertFalse(is_unordered_list("- First item\n* Second item"))
        self.assertFalse(is_unordered_list("1. Not an unordered list"))

    def test_is_ordered_list_valid(self):
        """Test that is_ordered_list works for valid list syntax."""
        self.assertTrue(is_ordered_list("1. Item 1\n2. Item 2"))
        self.assertTrue(is_ordered_list("1. Single item"))

    def test_is_ordered_list_invalid(self):
        """Test that is_ordered_list correctly identifies invalid syntax."""
        self.assertFalse(is_ordered_list("1. Item 1\n3. Item 2"))
        self.assertFalse(is_ordered_list("2. Item 1"))
        self.assertFalse(is_ordered_list("- Not an ordered list"))


if __name__ == "__main__":
    unittest.main()
