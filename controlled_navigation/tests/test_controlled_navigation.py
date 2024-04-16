""" This module contains the tests for the controlled_navigation XBlock. """

from unittest.mock import Mock, patch

from django.test import TestCase
from opaque_keys.edx.keys import UsageKey
from xblock.fields import ScopeIds

from controlled_navigation.controlled_navigation import XBlockControlledNavigation


class TestXblockControlledNavegation(TestCase):
    """Tests for XBlockControlledNavegation class."""

    def setUp(self) -> None:
        """Set up the test suite."""
        self.runtime = Mock()
        self.child_block = Mock(
            render=Mock(
                return_value=Mock(
                    content="MyXBlock: count is now 0",
                    resources=[],
                ),
            ),
        )
        self.block = XBlockControlledNavigation(
            runtime=self.runtime,
            field_data={},
            scope_ids=ScopeIds("1", "2", "3", "4"),
        )
        self.block.randomness = False
        self.block.randomized_children_ids = []
        self.block.current_child_id = ""
        self.block.forward_navigation_only = True
        self.block._render_child_fragment = Mock()  # pylint: disable=protected-access
        self.block.render_template = Mock(return_value="Test render")

    def test_author_view_root(self):
        """Render the author view with the root block.
        Expected result: a div with the children content.
        """
        self.block.location = "root"
        self.block.children = ["child1"]
        self.runtime.get_block = Mock(return_value=self.child_block)
        self.runtime.service = Mock(
            return_value=Mock(
                render_template=Mock(
                    return_value='<div class="controlled_navigation_block"> MyXBlock: count is now 0 </div>',
                ),
            ),
        )

        fragment = self.block.author_view({"root_xblock": self.block})

        self.assertEqual(
            fragment.content.replace("\n", "").replace(" ", ""),
            '<divclass="controlled_navigation_block">MyXBlock:countisnow0</div>',
        )

    def test_author_view(self):
        """Render the author view without the root block.
        Expected result: an empty div.
        """
        fragment = self.block.author_view({})

        self.assertEqual(
            fragment.content.replace("\n", "").replace(" ", ""),
            "",
        )

    @patch.object(UsageKey, "from_string")
    @patch("controlled_navigation.controlled_navigation.Fragment")
    def test_student_view_with_context(self, _, usage_key_mock: Mock):
        """
        Test `student_view` method with a provided context.
        Expected result: A Fragment with the child content and the provided context.
        """
        self.block.children = ["child1", "child2"]
        usage_key_mock.return_value = "child1-usage-key"
        self.runtime.get_block = Mock(return_value=self.child_block)
        self.block._render_child_fragment = Mock(  # pylint: disable=protected-access
            return_value=Mock(content="child_content")
        )
        expected_context = {
            "block": self.block,
            "child_content": "child_content",
            "is_first_child": True,
            "is_last_child": False,
        }

        self.block.student_view({})

        self.block.render_template.assert_called_once_with(
            "public/html/controlled_navigation.html", expected_context
        )

    def test_get_children_ids_no_randomness(self):
        """
        Test `get_children_ids` method when randomness is False.
        """
        self.block.get_parsed_children_ids = Mock(return_value=["child1", "child2"])

        children_ids = self.block.get_children_ids()

        self.assertEqual(children_ids, ["child1", "child2"])

    def test_get_children_ids_with_randomness_no_randomized_ids(self):
        """
        Test `get_children_ids` method when randomness is `True` and randomized_children_ids is empty.
        """
        self.block.randomness = True
        self.block.generate_randomized_children_ids = Mock()

        self.block.get_children_ids()

        self.block.generate_randomized_children_ids.assert_called_once()

    def test_get_children_ids_with_randomness_and_randomized_ids(self):
        """
        Test `get_children_ids` method when randomness is `True` and randomized_children_ids is not empty.
        """
        self.block.randomness = True
        self.block.randomized_children_ids = ["child2", "child1"]

        children_ids = self.block.get_children_ids()

        self.assertEqual(children_ids, ["child2", "child1"])

    def test_get_current_child_id_no_current_child_id_no_children_ids(self):
        """
        Test `get_current_child_id` method when current_child_id is not set and children_ids is not provided.

        Expected result: The first child id from the block's children.
        """
        self.block.get_children_ids = Mock(return_value=["child1", "child2"])

        current_child_id = self.block.get_current_child_id()

        self.assertEqual(current_child_id, "child1")

    def test_get_current_child_id_no_current_child_id_with_children_ids(self):
        """
        Test `get_current_child_id` method when current_child_id is not set and children_ids is provided.

        Expected result: The first child id from the provided children_ids.
        """
        current_child_id = self.block.get_current_child_id(["child3", "child4"])

        self.assertEqual(current_child_id, "child3")

    def test_get_current_child_id_with_current_child_id_no_children_ids(self):
        """
        Test `get_current_child_id` method when current_child_id is set and children_ids is not provided.

        Expected result: The current child id from the block.
        """
        self.block.current_child_id = "child1"

        current_child_id = self.block.get_current_child_id()

        self.assertEqual(current_child_id, "child1")

    def test_get_current_child_id_with_current_child_id_with_children_ids(self):
        """
        Test `get_current_child_id` method when current_child_id is set and children_ids is provided.

        Expected result: The current child id from the block, ignoring the provided children_ids.
        """
        self.block.current_child_id = "child1"

        current_child_id = self.block.get_current_child_id(["child3", "child4"])

        self.assertEqual(current_child_id, "child1")

    def test_is_first_child_true(self):
        """
        Test `is_first_child` method when the current child is the first one.
        """
        self.block.current_child_id = "child1"
        children_ids = ["child1", "child2"]

        result = self.block.is_first_child(children_ids)

        self.assertTrue(result)

    def test_is_first_child_false(self):
        """
        Test `is_first_child` method when the current child is not the first one.
        """
        self.block.current_child_id = "child2"
        children_ids = ["child1", "child2"]

        result = self.block.is_first_child(children_ids)

        self.assertFalse(result)

    def test_is_last_child_true(self):
        """
        Test `is_last_child` method when the current child is the last one.
        """
        self.block.current_child_id = "child2"
        children_ids = ["child1", "child2"]

        result = self.block.is_last_child(children_ids)

        self.assertTrue(result)

    def test_is_last_child_false(self):
        """
        Test `is_last_child` method when the current child is not the last one.
        """
        self.block.current_child_id = "child1"
        children_ids = ["child1", "child2"]

        result = self.block.is_last_child(children_ids)

        self.assertFalse(result)
