"""Decorator to enforce that a class is a singleton."""


def Singleton(class_):
    """Helper class for creating a singleton."""
    instances = {}

    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        else:
            print "Warning: tried to create multiple instances of singleton " + class_.__name__
        return instances[class_]
    return get_instance

