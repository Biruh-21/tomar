from django import template
import readtime


def estimated_read_time(content):
    """Calculate the estimated time in minutes to read the post."""
    return readtime.of_html(content)


register = template.Library()
register.filter("readtime", estimated_read_time)
