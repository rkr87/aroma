class Observable:
    _listeners = None

    def listen(self, name, observer):
        if not self._listeners:
            self._listeners = []
        self._listeners.append((name, observer))

    def changed(self):
        if not self._listeners:
            return
        for name, listener in self._listeners:
            listener.state_changed(name, self)


def mutating(method):
    def _wrapper(self, *args, **kwargs):
        result = method(self, *args, **kwargs)
        self.changed()
        return result

    return _wrapper


class Binding:
    def __init__(self, state, instance):
        self.state = state
        self.instance = instance

    @property
    def value(self):
        return self.instance.__dict__[self.state.name]

    @value.setter
    def value(self, new_value):
        self.state.__set__(self.instance, new_value)

    def __bool__(self):
        return bool(self.value)


class State:
    def __init__(self, python_type=None, default=None):
        self.python_type = python_type
        self.name = None
        self.default = default

    def __get__(self, instance, owner=None):
        if not instance:
            return self
        if self.name not in instance.__dict__:
            value = self.get_default()
            if isinstance(value, Observable):
                # If the state's value is Observable, listen for changes to trigger
                # instance.state_changed.
                value.listen(self.name, instance)
            # Set the default value the first time it's accessed, so it's not changing
            # on every access.
            instance.__dict__[self.name] = self.check_value(instance, value)
            # TODO: firing the state_changed for default values seems unnecessary?
            # self.__set__(instance, value)
        if isinstance(instance.__dict__[self.name], Observable):
            # No need for Bindings if the state is Observable. It triggers state_changed
            # as necessary.
            return instance.__dict__[self.name]
        return Binding(self, instance)

    def __set__(self, instance, value):
        instance.__dict__[self.name] = self.check_value(instance, value)
        instance.state_changed(self.name, value)

    def __set_name__(self, owner, name):
        self.name = name

    def get_default(self):
        return self.default() if callable(self.default) else self.default

    def check_value(self, instance, value):
        if (
            value is None
            or self.python_type is None
            or isinstance(value, self.python_type)
        ):
            return value
        raise AttributeError(
            "{}.{} must be of type {} (got {})".format(
                instance.__class__.__name__,
                self.name,
                self.python_type.__name__,
                value.__class__.__name__,
            )
        )
