If you want to display snazzy Github participation graphs on your Django-based
web site, this is for you.

This is a small Django app that provides a template tag to allow you to include
sparklines of the 52-week commit history for a project on Github. Think of the
graphs you see down the left-hand side of a Github user's home page -- only, as
I said, snazzy sparklines instead of bar charts. Examples can be found on the
`introductory blog post`_. A `real-world example`_ can be found on the author's
"About" page:

.. _`introductory blog post`: http://www.flother.com/blog/2009/django-github-sparklines/
.. _`real-world example`: http://www.flother.com/about/


Requirements
============

Other than Django itself, no external libraries are required. The sparklines
are generated using Google Charts so no image processing is done locally. The
app has been tested with the latest Subversion trunk version of Django, but
should be quite happy working with older releases too.


Installation
============

You can download the package from PyPI using either PIP or ``easy_install``::

  pip install participationgraphs
  easy_install participationgraphs

Alternatively you can install the latest version from Github::

  pip install -U -e git+git://github.com/flother/participationgraphs.git#egg=participationgraphs

Add the ``participationgraphs`` app to ``INSTALLED_APPS`` in your Django
settings file::

  INSTALLED_APPS = (
      # ...
      'participationgraphs',
  )

If you're been running the development server while you do this, restart it so
Django can find the new template tag library.


Usage
=====

In each template you want to show participation graphs, load the
``githubgraphs`` library::

  {% load githubgraphs %}

This can appear anywhere in your template as long as it comes before the first
use of the ``github_participation_graph`` template tag.

At the point in the template you want to display a participation graph,
include::

  {% github_participation_graph "brosner" "django" %}

This will output an img element for the sparkline, showing the commit history
for the *django* project belonging to the Github user *brosner*. The ``img``
element's ``src`` attribute will point to a dynamically-generated Google Charts
image.

By default the sparkline will be a grey data-line on a white background, 400
pixels wide by 50 pixels high, but if you want to change the colours or
dimensions you can. The following example will display a sparkline 100 pixels
wide by 40 pixels high, with a red data-line on a black background::

  {% github_participation_graph "brosner" "django" "100x40" "ff0000" "000000" %}

There are seven parameters in total; two are mandatory and five are optional:

1. ``username``: Github username (mandatory)
2. ``project_name``: Github project name (mandatory)
3. ``dimensions``: height and width of the image in pixels in the format
   "HxW"
4. ``foreground_colour``: six-digit hex colour of the sparkline data
5. ``background_colour``: six-digit hex colour of the graph background
6. ``fill_colour``: six-digit hex colour of the graph's data fill
7. ``marker_colour``: six-digit hex colour for the final data marker

Caveat emptor
=============

To get the commit data for the graph the template tag makes an HTTP request to
``github.com`` -- so for every sparkline there will be two HTTP requests: one
client-side to a Google server to get the chart image and one server-side to
Github. Although it's optional I highly recommend using Django's built-in
caching to cache either the template or the template fragment.


Licence
=======

All code in this repository is released under the GNU General Public licence
version 2. For details see the LICENCE file in the root directory.

If you'd like to use the code under a different (open-source) licence, contact
me and we'll see what we can do.
