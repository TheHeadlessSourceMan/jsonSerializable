# jsonSerializable
Useful and more seamless ways of serializing python classes to/from json.

There are many different levels you can operate at, from:
- simply using JsonDict for more correct typing
- to using getJsonFloatArray(jsonDict,name,[]) for easier and more robust reading
- to deriving from JsonSerializable to create a class that can load/save json data from any file or url!

## history

This is a merger of several JSON features that seemed to keep getting coppied/reimplemented
in many different projects.  Instead of constantly re-inventing the wheel it only made sense
to amalgamate the best features of all of them into one.