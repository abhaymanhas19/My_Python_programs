from multipledispatch import dispatch
from typing import Any

class DemoClass:
    
    @dispatch(object, object, object)
    def demo(self, a: Any, b: Any, c: Any):
        print("This is a function for any type:", a, b, c)
    
    @dispatch(str, list, float)
    def demo(self, a: str, b: list, c: float):
        print("This is a function for str, list, and float:", a, b, c)

    @dispatch(str, int, float)
    def demo(self, a: str, b: int, c: float):
        print("This is a function for str, int, and float:", a, b, c)


demo_instance = DemoClass()

demo_instance.demo("1", 90, "Ar")   
demo_instance.demo("example", {}, 3.14) 
demo_instance.demo("example", 42, 2.718)  



# from functools import singledispatch ,singledispatchmethod

# @singledispatch
# def demo(a:Any,b:Any):
#     print("default method executed")

# @demo.register
# def _(a:str,n:int):
#     print("this is int",a ,n)

# @demo.register
# def _(a:str):
#     print("this is str")


# demo(34,"35")