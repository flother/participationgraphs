from django import template

from participationgraphs.utils.github import get_github_participation_chart_img


register = template.Library()


@register.simple_tag
def github_participation_graph(username, project_name, dimensions='400x50',
        foreground_colour='999999', background_colour='ffffff',
        fill_colour='ffffff', marker_colour='333333'):
    """
    Return an <img /> element referencing a Google Charts sparkline
    displaying the number of commits in the last 52 weeks for a given
    project of a given user on Github.  Commits are grouped by week.

    Note: there is no caching on this tag, so it will make a request to
    github.com each time you call it, so be sure to use Django's
    built-in caching.

    If an error occurs while retrieving the data form Github (for
    example if the user or project doesn't exist) an empty string will
    be returned.

    Mandatory arguments:
        ``username``: Github username
        ``project_name``: Github project name

    Optional arguments:
        ``dimensions``: A string in the format 400x50 (width by height)
        ``foreground_colour``: 6-digit hex colour of the sparkline data
        ``background_colour``: 6-digit hex colour of the graph background
        ``fill_colour``: 6-digit hex colour of the graph's data fill
        ``marker_colour``: 6-digit hex colour for the final data marker
    """
    try:
        (width, height) = dimensions.split('x')
    except ValueError:
        raise template.TemplateSyntaxError, 'github_participation_graph: third\
            argument must be in the form WxH, e.g. "400x50"'
    try:
        return get_github_participation_chart_img(username, project_name,
            width, height, foreground_colour, background_colour, fill_colour,
            marker_colour)
    except (ValueError, IndexError):
        return ""
