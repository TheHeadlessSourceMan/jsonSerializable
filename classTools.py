"""
Useful tools for tampering with classes and objects
"""
import typing


def classMethodAdder(
    clazz:typing.Type,
    fn:typing.Callable
    )->None:
    """
    Add a new method to a class.

    Example:
    def extraFunction(self:MyClass,s:str):
        print(f'{s} {self.member}')

    classMethodAdder(MyClass,extraFunction)
    obj=MyClass('Sam')
    obj.extraFunction("Hello")
    """
    setattr(clazz,fn.__name__,fn)


def classParentsAdder(
    clazz:typing.Type,
    parents:typing.Union[typing.Type,typing.Iterable[typing.Type]]
    )->None:
    """
    Add parents to a class after-the-fact.

    NOTE: will not add any constructor calls, so beware of that!

    Example:
    class Parent:
        def hi(self):
            print("hi")

    class Child:
        pass

    classParentsAdder(Child,Parent)
    c=Child()
    c.hi()
    """
    baseTypes=list(clazz.__bases__)
    if isinstance(parents,object):
        baseTypes.append(parents)
    else:
        baseTypes=baseTypes.extend(parents)
    clazz.__bases__=tuple(baseTypes)
