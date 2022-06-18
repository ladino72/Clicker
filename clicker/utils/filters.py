
# https://stackoverflow.com/questions/21739773/how-do-i-register-filters-for-dynamically-generated-jinja2-templates-in-flask
# Registering Filter in __init__.py as
# app.jinja_env.filters['upper'] = caps
# the name I gave is upper and can be used in any template. Thus, in save_grades_pdf is used as name|upper
# See also https://kyletk.com/post/3
# There is another way to declare filters as is explained in
# https://stackoverflow.com/questions/12288454/how-to-import-custom-jinja2-filters-from-another-file-and-using-flask

def caps(text):
    """capitalize all letters of a string."""
    return text.upper()

def title(text):
    """capitalize first letter of each word of a string."""
    return text.title()

def half_name(name):
    """Luis Alejandro Ladino Gaspar is transformed into Ladino Gaspar Luis Alejandro"""
    full_name = name.split()
    first_names = full_name[:-2 or None]
    return ' '.join(first_names)
