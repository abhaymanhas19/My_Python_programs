class A:
  name="abjay"
  
  
  def f(self):
    print(id(self.name))
    self.name="rohit"
    print(id(o.name))
  
    
o=A()
o.f()

print(id(o.name))
print(A.name)
    

