Controlled Navigation XBlock
############################

|status-badge| |license-badge| |ci-badge|


Purpose
*******

Controlled Navigation XBlock allows course authors to create a sequence of
components that learners will navigate through in a controlled manner. The
course author can configure the order of the components, and the learner will
be able to navigate through them using the navigation buttons.

This XBlock has been created as an open source contribution to the Open
edX platform and has been funded by **Unidigital** project from the Spanish
Government - 2023.


Enabling the XBlock in a course
*******************************

Once the XBlock has been installed in your Open edX installation, you can
enable it in a course from Studio through the **Advanced Settings**.

1. Go to Studio and open the course to which you want to add the XBlock.
2. Go to **Settings** > **Advanced Settings** from the top menu.
3. Search for **Advanced Module List** and add ``"controlled_navigation"``
   to the list.
4. Click **Save Changes** button.


Adding a Controlled Navigation Component to a course unit
*********************************************************

From Studio, you can add the Controlled Navigation Component to a course unit.

1. Click on the **Advanced** button in **Add New Component**.

   .. image:: https://github.com/eduNEXT/xblock-controlled-navigation/assets/64033729/1b52b5fa-88ca-4bae-b141-19b9c1e4063f
      :alt: Open Advanced Components

2. Select **Content With Controlled Navigation** from the list.

   .. image:: https://github.com/eduNEXT/xblock-controlled-navigation/assets/64033729/b2b29313-feb3-40b4-80c7-c2b868d75304
      :alt: Select Controlled Navigation Component

3. Configure the component as needed.


View from the Learning Management System (CMS)
**********************************************

The **Controlled Navigation** component has a set of settings that can be
configured by the course author.

.. image:: https://github.com/eduNEXT/xblock-controlled-navigation/assets/64033729/ebcc1f59-f7b6-4b9c-8a94-8c216d959431
    :alt: Settings for the Controlled Navigation component

The **Controlled Navigation** component has the following settings:

- **Randomness**: If enabled, the children components will be displayed in a
  random order. This randomization is unique to each learner. If disabled, the
  children components will be displayed in the order they were added to the
  Controlled Navigation component.
- **Subset Size**: If the **Randomness** setting is enabled, this setting
  allows the course author to specify the number of children components that
  will be displayed to the learner. By default, it is disabled (0), and all the
  children components will be displayed.
- **Forward Navigation Only**: If enabled, the learner will only be able to
  navigate to the next component. If disabled, the learner will be able to
  navigate to the next and previous components. By default, it is enabled.
- **Next Button Text**: The text that will be displayed in the button that
  allows the learner to navigate to the next component.
- **Previous Button Text**: The text that will be displayed in the button that
  allows the learner to navigate to the previous component.

Here is how the **Controlled Navigation** component looks in the
**Author View**:

.. image:: https://github.com/eduNEXT/xblock-controlled-navigation/assets/64033729/e87a233a-757a-44b4-bbe2-5080fbdc9400
    :alt: Author view for component

When accessing the component by selecting the **VIEW ➔** button, you will see
the list of children components that are part of the Controlled Navigation
component.

.. image:: https://github.com/eduNEXT/xblock-controlled-navigation/assets/64033729/b30221b8-e6ee-4584-95fc-72eaf75a4b1d
    :alt: View of the component

Here is an example of a Controlled Navigation component with a **Problem**
component as a child:

.. image:: https://github.com/eduNEXT/xblock-controlled-navigation/assets/64033729/4101cef0-c172-41be-9596-630c106155db
    :alt: Example of a Controlled Navigation component with a Problem component as a child


View from the Learning Management System (LMS)
**********************************************

When a learner accesses the course, they will see the children components of
the Controlled Navigation component one by one. The learner will be able to
navigate to the next component by clicking the **Next** button, and to the
previous component by clicking the **Previous** button.

.. image:: https://github.com/eduNEXT/xblock-controlled-navigation/assets/64033729/6ed1627f-f7fc-4006-a489-63f39523241c
    :alt: View of the component in the LMS


Experimenting with this XBlock in the Workbench
************************************************

`XBlock`_ is the Open edX component architecture for building custom learning
interactive components.

You can see the Controlled Navigation component in action in the XBlock
Workbench. Running the Workbench requires having docker running.

.. code::

    git clone git@github.com:eduNEXT/xblock-controlled-navigation
    virtualenv venv/
    source venv/bin/activate
    cd xblock-controlled-navigation
    make upgrade
    make install
    make dev.run

Once the process is done, you can interact with the Controlled Navigation
XBlock in the Workbench by navigating to http://localhost:8000

For details regarding how to deploy this or any other XBlock in the Open edX
platform, see the `installing-the-xblock`_ documentation.

.. _XBlock: https://openedx.org/r/xblock
.. _installing-the-xblock: https://edx.readthedocs.io/projects/xblock-tutorial/en/latest/edx_platform/devstack.html#installing-the-xblock


Getting Help
*************

If you're having trouble, the Open edX community has active discussion forums
available at https://discuss.openedx.org where you can connect with others in
the community.

Also, real-time conversations are always happening on the Open edX community
Slack channel. You can request a `Slack invitation`_, then join the
`community Slack workspace`_.

For anything non-trivial, the best path is to open an `issue`_ in this
repository with as many details about the issue you are facing as you can
provide.

For more information about these options, see the `Getting Help`_ page.

.. _Slack invitation: https://openedx.org/slack
.. _community Slack workspace: https://openedx.slack.com/
.. _issue: https://github.com/eduNEXT/xblock-controlled-navigation/issues
.. _Getting Help: https://openedx.org/getting-help


License
*******

The code in this repository is licensed under the AGPL-3.0 unless otherwise
noted.

Please see `LICENSE.txt <LICENSE.txt>`_ for details.


Contributing
************

Contributions are very welcome.

This project is currently accepting all types of contributions, bug fixes,
security fixes, maintenance work, or new features.  However, please make sure
to have a discussion about your new feature idea with the maintainers prior to
beginning development to maximize the chances of your change being accepted.
You can start a conversation by creating a new issue on this repo summarizing
your idea.

Translations
============

This Xblock is initially available in English and Spanish. You can help by
translating this component to other languages. Follow the steps below:

1. Create a folder for the translations in ``locale/``, eg:
   ``locale/fr_FR/LC_MESSAGES/``, and create your ``text.po``
   file with all the translations.
2. Run ``make compile_translations``, this will generate the ``.mo`` file.
3. Create a pull request with your changes.


Reporting Security Issues
*************************

Please do not report a potential security issue in public. Please email
security@edunext.co.


.. |ci-badge| image:: https://github.com/eduNEXT/xblock-controlled-navigation/actions/workflows/ci.yml/badge.svg?branch=main
    :target: https://github.com/eduNEXT/xblock-controlled-navigation/actions
    :alt: CI

.. |license-badge| image:: https://img.shields.io/github/license/eduNEXT/xblock-controlled-navigation.svg
    :target: https://github.com/eduNEXT/xblock-controlled-navigation/blob/main/LICENSE.txt
    :alt: License

.. |status-badge| image:: https://img.shields.io/badge/Status-Maintained-brightgreen
