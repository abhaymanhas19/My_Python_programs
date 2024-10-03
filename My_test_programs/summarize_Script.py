import pandas as pd
import openai
import json

class Summarizer:
    def __init__(self:object,file_path:str,title,description:str):
        self.file_path:str=file_path
        self.description_column_name:str=description
        self.title_column_name:str=title
        self.df:pd.DataFrame=None
        self.refined_data=[]
    
    def _read_file(self:object):
        self.df = pd.read_excel(self.file_path)
   
    def _read_column(self:object):
        return self.df[[self.title_column_name,self.description_column_name]]
 
    def __summarize_text(self,title,meta_description):
       response = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type":"json_object"},
            messages=[{"role":"system", 
            "content":""" You are an expert SEO content optimizer. Your task is to take the user's provided title and meta description and rewrite them to be concise, keyword-rich, and optimized for search engines,while also being compelling to users. Avoid any vague or ambiguous language"""
            },          
            {"role":"user","content":f"""My title is '{title}' and my meta description is '{meta_description}'.
             
             ###
             
             JSON Output Template:
             {{
                 "Title":"Title value",
                 "Meta Description":"Descripiton value"
             }}
             
             ###
             
             JSON OUTPUT"""}],
            temperature=0.2,
        )
       return json.loads(response.choices[0].message.content)
   
    def _process_columns_values(self,columns_values):
        for value in columns_values.itertuples():
            response = self.__summarize_text(value[1],value[2])
            self.refined_data.append(response)
            print("**"*10)
            print("Title : ",response.get("Title"))
            print("Meta Description : ",response.get("Meta Description"))
            
    def _make_df(self):
        df=pd.DataFrame(self.refined_data)
        df.to_excel('optimized_excel_file.xlsx', index=False)
        
    def process_text(self):
       self._read_file()
       columns_values=self._read_column()
       self._process_columns_values(columns_values)
       self._make_df()

       
instance=Summarizer("Nihsamah_Shopify_Product_Title..xlsx","Title","Meta Descriptions")
instance.process_text()
       
        
    
        
    
    
    
    