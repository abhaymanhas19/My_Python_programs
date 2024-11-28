class_name=input("enter your class name: ")
base_classes = (object,)
class_attributes={
    "__init__":lambda self:print("i'm a constrator"),
    "demo":lambda self: print("this is a demo function "),
    "classmethodexample":classmethod(lambda cls: print("this is a class method")),
    "staticmethodexample":staticmethod(lambda:print("this is a static mehthos"))
}   


class_attributes={
    "__init__":lambda self,name: (
        setattr(self,"name",name)
    ),
    "test":lambda self:print(self.name)
}

class_instance = type(class_name,(object,),class_attributes)
instacen  =  class_instance("abjay")
instacen.test()


Dynamicclass=type(class_name,base_classes,class_attributes)
instance=Dynamicclass()
instance.demo()
Dynamicclass.classmethodexample()
Dynamicclass.staticmethodexample()    
