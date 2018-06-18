from ._collect import wrap_story
from ._context import Context, validate_arguments
from ._history import History
from ._repr import story_representation
from ._run import run_the_story, tell_the_story


class StoryWrapper(object):
    def __init__(self, cls, obj, name, arguments, collected):
        self.cls = cls
        self.obj = obj
        self.cls_name = cls.__name__
        self.name = name
        self.arguments = arguments
        self.collected = collected

    def __call__(self, *args, **kwargs):
        history = History(self.cls_name, self.name)
        ctx = Context(validate_arguments(self.arguments, args, kwargs), history)
        methods = wrap_story(is_story, self.collected, self.obj, ctx)
        return tell_the_story(ctx, methods)

    def run(self, *args, **kwargs):
        history = History(self.cls_name, self.name)
        ctx = Context(validate_arguments(self.arguments, args, kwargs), history)
        methods = wrap_story(is_story, self.collected, self.obj, ctx)
        return run_the_story(ctx, methods)

    def __repr__(self):
        return story_representation(
            is_story,
            self.cls_name + "." + self.name,
            self.cls,
            self.obj,
            self.collected,
        )


def is_story(attribute):
    return callable(attribute) and type(attribute) is StoryWrapper
