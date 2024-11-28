class_name = input("Class Name: ")

class_attributes={
    "__init__":lambda self,name: (
        setattr(self,"name",name)
    ),
    "test":lambda self:print(self.name)
}

class_instance = type(class_name,(object,),class_attributes)
instacen  =  class_instance("abjay")
instacen.test()

