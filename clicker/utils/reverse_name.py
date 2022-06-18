def reverse_name(name):
    """Luis Alejandro Ladino Gaspar is transformed into Ladino Gaspar Luis Alejandro"""
    full_name = name.split()
    last_names = full_name[-2:]
    first_names = full_name[:-2 or None]
    full_name = last_names + first_names
    return full_name
