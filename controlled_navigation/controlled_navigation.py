"""XBlock for controlled navegation."""

import pkg_resources
from django.utils import translation
from web_fragments.fragment import Fragment
from xblock.core import XBlock
from xblock.fields import Scope, String
from xblock.utils.resources import ResourceLoader
from xblock.utils.studio_editable import StudioContainerWithNestedXBlocksMixin, StudioEditableXBlockMixin

LOCAL_RESOURCE_LOADER = ResourceLoader(__name__)


def _(text):
    """Make '_' a no-op so we can scrape strings."""
    return text


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
        default=_("Content with Controlled Navegation"),
    )

    editable_fields = [
        "display_name",
    ]

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    def author_view(self, context):
        """
        Render the Studio preview by rendering each child so that they can all be seen and edited.
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

    def student_view(self, context):
        """
        View for students to see the blocks in the unit.
        """
        children_contents = []
        fragment = Fragment()

        for child_id in self.children:
            child = self.runtime.get_block(child_id)
            child_fragment = self._render_child_fragment(child, context, "student_view")
            fragment.add_fragment_resources(child_fragment)
            children_contents.append(child_fragment.content)

        render_context = {
            "block": self,
            "children_contents": children_contents,
        }
        render_context.update(context)
        fragment.add_content(
            LOCAL_RESOURCE_LOADER.render_django_template(
                "static/html/children.html", render_context
            )
        )
        return fragment

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
    def _get_statici18n_js_url():  # pragma: no cover
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
