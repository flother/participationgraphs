import urllib2

from django.utils.html import escape
from django.utils.translation import ugettext as _


def get_github_participation_chart_img(username, project_name, width, height,
        foreground_colour, background_colour, fill_colour, marker_colour):
    """
    Return an <img /> element referencing a Google Charts sparkline
    displaying the number of commits in the last 52 weeks for a given
    project of a given user on Github.  Commits are grouped by week.

    Arguments:
        ``username``: Github username
        ``project_name``: Github project name
        ``width``: width of the image in pixels
        ``height``: height of the image in pixels
        ``foreground_colour``: 6-digit hex colour of the sparkline data
        ``background_colour``: 6-digit hex colour of the graph background
        ``fill_colour``: 6-digit hex colour of the graph's data fill
        ``marker_colour``: 6-digit hex colour for the final data marker
    """
    src = get_google_chart_url(username, project_name, width,
        height, foreground_colour, background_colour, fill_colour, marker_colour)
    attributes = {
        'src': src,
        'alt': escape(_("52-week participation on the Github project '%s'" % project_name)),
        'width': width,
        'height': height,
    }
    return '<img alt="%(alt)s" height="%(height)s" src="%(src)s" width="%(width)s" />' % attributes


def get_google_chart_url(username, project_name, width, height,
        foreground_colour, background_colour, fill_colour='ffffff',
        marker_colour='333333'):
    """
    Generate a URL for a sparkline using the Google Charts API.
    """
    data = text_to_data(get_github_participation_data(username,
        project_name)['project_commits'])
    base_url = 'http://chart.apis.google.com/chart?%s'
    max_value = max(data)
    chart_options = {
        'chs': '%sx%s' % (width, height),  # Dimensions (width by height).
        'chco': foreground_colour,  # Line (data) colour.
        'chf': 'bg,s,%s' % background_colour,  # Graph background colour.
        'chm': 'B,%s,0,0,0|o,%s,0,51,4' % (fill_colour, marker_colour),  # Data fill and end marker.
        'chxp': '0,%0.1f' % ((100 / len(data)) * data[-1]),  # End marker position.
        'chxl': '0:|%s' % data[-1],  # Use the last data point as a marker.
        'chxt': 'r',  # Put the marker on the right-hand y-axis.
        'cht': 'ls',  # Chart type (here it's a sparkline).
        'chds': '%s,%s' % (0, max_value),  # Minimum and maximum data values.
        'chd': 't:%s' % ','.join([str(i) for i in data])  # Actual chart data.
    }
    return base_url % '&amp;'.join(['%s=%s' % (k, v)
        for k, v in chart_options.items()])


def get_github_participation_data(username, project_name):
    """
    Get the participation data (i.e. number of commits per week) for a
    given project for a given user on Github.
    """
    data_url = 'http://github.com/cache/participation_graph/%s/%s' % (
        username, project_name)
    try:
        response = urllib2.urlopen(data_url)
    except (urllib2.HTTPError, urllib2.URLError):
        # If retrieving the data from Github fails it's likely to be
        # because of a mis-spelled username or project name.  Re-raise
        # a ValueError here so it can be caught by the template tag.
        raise ValueError, "no data for user '%s' and project '%s'" % (username,
            project_name)
    data = response.read()
    commits = data.splitlines()
    return {'project_commits': commits[0], 'user_commits': commits[1]}


def text_to_data(text):
    """
    Convert a string containing only characters in the range
    [A-Za-z0-9!-] to a list of numerical data points, as specified by
    the Google Charts simple encoding format.

    http://code.google.com/apis/chart/formats.html#simple
    """
    data = []
    for char in range(0, len(text), 2):
        try:
            char1 = ord(text[char])
            char2 = ord(text[char + 1])
        except IndexError:
            raise ValueError, 'Text data must be an even length'
        data.append(char_to_int_data(char1) * 64 + char_to_int_data(char2))
    return data


def char_to_int_data(char):
    """
    Convert a character in the range [A-Za-z0-9!-] from plain text into
    an integer based on the Google Charts simple encoding.

    http://code.google.com/apis/chart/formats.html#simple
    """
    if (char >= 65) and (char <= 90):
        return char - 65  # A = 0 up to Z = 25.
    elif (char >= 97 ) and (char <= 122):
        return char - 97 + 26  # a = 26 up to z = 51.
    elif (char >= 48) and (char <= 57):
        return char - 48 + 52  # 0 = 52 up to 9 = 61.
    elif char == 33:
        return 62  # Exclamation mark.
    elif char == 45:
        return 63  # Minus/hyphen sign.
    raise ValueError, 'Unsupported character'
