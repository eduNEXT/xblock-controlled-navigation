"""XBlock for controlled navegation."""

import random
from typing import List, Optional

import pkg_resources
from django.utils import translation
from opaque_keys.edx.keys import UsageKey
from web_fragments.fragment import Fragment
from xblock.core import XBlock
from xblock.fields import Boolean
from xblock.fields import List as ListField
from xblock.fields import Scope, String
from xblock.utils.resources import ResourceLoader
from xblock.utils.studio_editable import StudioContainerWithNestedXBlocksMixin, StudioEditableXBlockMixin

from controlled_navigation.utils import _


class XBlockControlledNavigation(
    StudioContainerWithNestedXBlocksMixin, StudioEditableXBlockMixin, XBlock
):
    """
    XBlock for controlled navigation that can be applied to the child content.
    """

    CATEGORY = "controlled_navigation"

    display_name = String(
        display_name=_("Display Name"),
        help=_("The display name for this component."),
        scope=Scope.settings,
        default=_("Content with Controlled Navigation"),
    )

    randomness = Boolean(
        display_name=_("Randomness"),
        help=_("When enabled, the children of the component will be displayed in a random order."),
        scope=Scope.settings,
        default=False,
    )

    next_button_text = String(
        display_name=_("Next Button Text"),
        help=_("Text for the next button used to navigate forward through the components' children."),
        scope=Scope.settings,
        default=_("Next Question"),
    )

    prev_button_text = String(
        display_name=_("Previous Button Text"),
        help=_("Text for the previous button used to navigate back through the components' children."),
        scope=Scope.settings,
        default=_("Previous Question"),
    )

    randomized_children_ids = ListField(
        display_name=_("Randomized Children IDs"),
        help=_("List of randomized children ids for each student."),
        scope=Scope.user_state,
        default=[],
    )

    current_child_id = String(
        display_name=_("Current Child ID"),
        help=_("Current child id for the student."),
        scope=Scope.user_state,
        default="",
    )

    editable_fields = [
        "display_name",
        "randomness",
        "next_button_text",
        "prev_button_text",
    ]

    def resource_string(self, path: str) -> str:
        """
        Handy helper for getting resources from our kit.

        Args:
            path (str): Path to the resource.

        Returns:
            str: The resource content.
        """
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    def render_template(
        self, template_path: str, context: Optional[dict] = None
    ) -> str:
        """
        Render a template with the given context.

        The template is translated according to the user's language.

        Args:
            template_path (str): The path to the template
            context(dict, optional): The context to render in the template

        Returns:
            str: The rendered template
        """
        return self.loader.render_django_template(
            template_path, context, i18n_service=self.runtime.service(self, "i18n")
        )

    def author_view(self, context: dict) -> Fragment:
        """
        Render the Studio preview by rendering each child so that they can all be seen and edited.

        Args:
            context (dict): Context for the author view.

        Returns:
            Fragment: The fragment with the children content.
        """
        fragment = Fragment()
        root_xblock = context.get("root_xblock")
        is_root = (
            root_xblock
            and root_xblock.location == self.location  # pylint: disable=no-member
        )
        if is_root:
            # User has clicked the "View" link. Show a preview of all possible children:
            self.render_children(context, fragment, can_reorder=True, can_add=True)
        # else: When shown on a unit page, don't show any sort of preview -
        # just the status of this block in the validation area.

        return fragment

    def student_view(self, context: dict) -> Fragment:
        """
        View for students to navigate through the children.

        Each child will be rendered and the student can navigate through them.

        Args:
            context (dict): Context for the student view.

        Returns:
            Fragment: The fragment with the child content.
        """
        fragment = Fragment()

        children_ids = self.get_children_ids()

        if not children_ids:
            return fragment

        child_usage_key = UsageKey.from_string(self.get_current_child_id(children_ids))
        child = self.runtime.get_block(child_usage_key)
        child_fragment = self._render_child_fragment(child, context, "student_view")
        fragment.add_fragment_resources(child_fragment)

        render_context = {
            "block": self,
            "child_content": child_fragment.content,
            "is_first_child": self.is_first_child(children_ids),
            "is_last_child": self.is_last_child(children_ids),
            **context,
        }

        fragment.add_content(
            self.render_template(
                "public/html/controlled_navigation.html", render_context
            )
        )
        fragment.add_javascript(
            self.resource_string("public/js/src/controlled_navigation.js")
        )
        fragment.add_css(self.resource_string("public/css/controlled_navigation.css"))
        fragment.initialize_js("XBlockControlledNavigation")

        return fragment

    def get_current_child_id(self, children_ids: Optional[List[str]] = None) -> str:
        """
        Return the current child id.

        Optionally receive a list of children to use.
        If not provided, it will get the children from the block.

        Args:
            children_ids (Optional[List[str]], optional):
                Children of the block. Defaults to None.

        Returns:
            str: The current child id.
        """
        if not self.current_child_id:
            children = children_ids or self.get_children_ids()
            if children:
                self.current_child_id = children[0]
        return self.current_child_id

    def get_children_ids(self) -> List[str]:
        """
        Return the children ids of the XBlock.

        Returns:
            List[str]: List of children ids.
        """
        if self.randomness:
            if not self.randomized_children_ids:
                self.generate_randomized_children_ids()
            return self.randomized_children_ids
        return self.get_parsed_children_ids()

    def generate_randomized_children_ids(self) -> None:
        """
        Generate a randomized list of children ids.
        """
        self.randomized_children_ids = [str(child) for child in self.children]
        random.shuffle(self.randomized_children_ids)

    def get_parsed_children_ids(self) -> List[str]:
        """
        Get the parsed children of this block.

        `self.children` is a list of the children's UsageKeys. This method returns
        a list of the children's IDs, converting each UsageKey to a string.

        Returns:
            List[str]: List of children ids.
        """
        return [str(child) for child in self.children]

    def is_first_child(self, children_ids: List[str]) -> bool:
        """
        Check if the current child is the first one.

        Args:
            children_ids (List[str]): List of children ids.

        Returns:
            bool: If the current child is the first one.
        """
        return self.current_child_id == str(children_ids[0])

    def is_last_child(self, children_ids: List[str]) -> bool:
        """
        Check if the current child is the last one.

        Args:
            children_ids (List[str]): List of children ids.

        Returns:
            bool: If the current child is the last one.
        """
        return self.current_child_id == str(children_ids[-1])

    @XBlock.json_handler
    def next_child(
        self, data: dict, suffix: str = ""  # pylint: disable=unused-argument
    ) -> dict:
        """
        Render the next child of the XBlock.

        Args:
            data (dict): Optional data.
            suffix (str, optional): Suffix. Defaults to "".

        Returns:
            dict: If the request was successful.
        """
        children = self.get_children_ids()
        current_index = children.index(self.get_current_child_id())
        if current_index == len(children) - 1:
            return {"result": "error"}
        self.current_child_id = children[current_index + 1]
        return {"result": "success"}

    @XBlock.json_handler
    def prev_child(
        self, data: dict, suffix: str = ""  # pylint: disable=unused-argument
    ) -> dict:
        """
        Render the previous child of the XBlock.

        Args:
            data (dict): Optional data.
            suffix (str, optional): Suffix. Defaults to "".

        Returns:
            dict: If the request was successful.
        """
        children = self.get_children_ids()
        current_index = children.index(self.get_current_child_id())
        if current_index == 0:
            return {"result": "error"}
        self.current_child_id = children[current_index - 1]
        return {"result": "success"}

    @staticmethod
    def workbench_scenarios():  # pragma: no cover
        """Create canned scenario for display in the workbench."""
        return [
            (
                "XblockControlledNavigation",
                """<controlled_navigation/>
             """,
            ),
            (
                "Multiple XblockControlledNavigation",
                """<vertical_demo>
                <controlled_navigation/>
                <controlled_navigation/>
                <controlled_navigation/>
                </vertical_demo>
             """,
            ),
        ]

    @staticmethod
    def _get_statici18n_js_url() -> Optional[str]:  # pragma: no cover
        """
        Return the Javascript translation file for the currently selected language, if any.

        Defaults to English if available.
        """
        locale_code = translation.get_language()
        if locale_code is None:
            return None
        text_js = "public/js/translations/{locale_code}/text.js"
        lang_code = locale_code.split("-")[0]
        for code in (locale_code, lang_code, "en"):
            loader = ResourceLoader(__name__)
            if pkg_resources.resource_exists(
                loader.module_name, text_js.format(locale_code=code)
            ):
                return text_js.format(locale_code=code)
        return None

    @staticmethod
    def get_dummy():
        """
        Generate initial i18n with dummy method.
        """
        return translation.gettext_noop("Dummy")
