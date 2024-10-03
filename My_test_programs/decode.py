# import base64

# encoded_string="Q2F0ZWdvcnksU3ViLUNhdGVnb3J5LENvdW50ClNpZ25pZmljYW50IFllYXJzLDIwMDBzLDgzClNpZ25pZmljYW50IFllYXJzLDE5ODBzLDg1ClNpZ25pZmljYW50IFllYXJzLDE5OTBzLDEzNQpTaWduaWZpY2FudCBZZWFycywxOTcwcywxMzgKU2lnbmlmaWNhbnQgWWVhcnMsMTk2MHMsMTQyCg=="


# decoded_string=base64.b64decode(encoded_string).decode('utf-8')

# with open("demo.csv",'w') as f:
#     f.write(decoded_string)
from dataclasses import dataclass
from pydantic import BaseModel,validator


class user(BaseModel):
    name:str
    
    @validator("name")
    @classmethod
    def validate_nms_dmo(cls, value):
        if value!="abhay":
            raise ValueError("The value should be abhay")
        return value
    
    
    
u=user(name="abhay")
print(u.name)
