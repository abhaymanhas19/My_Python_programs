import argparse
import pandas as pd
import openpyxl
import re
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  
c_handler = logging.StreamHandler()
logger.addHandler(c_handler)


def price_pattern():
    price_pattern = r'\$\d{1,3}(?:,\d{3})*(?:\.\d+)?(?:\s*millon(?:es)?)?'
    return price_pattern

def clean_prices(prices):
    cleaned_prices = [float(price.replace('$',"").split("millones")[0].replace(",", "")) if "millones" in price else float(price.replace("$","").replace(",", "")) for price in prices]
    return cleaned_prices
    
    
def preapre_data(values_object):
    max_length = 1 
    data = []
    for value in values_object.values():
        if isinstance(value, list):
            if len(value) > max_length:
                max_length = len(value)
                
    for key, value in values_object.items():
        if isinstance(value, list):
            clean_values = clean_prices(value)
            padded_values = clean_values + [pd.NA] * (max_length - len(value))
            
            row = [key] + padded_values
        data.append(row)
    value_columns = [f'Value{i+1}' for i in range(max_length+1)]
    return data, value_columns

def create_output_file(values_object):
    try:

        data , values_columns  = preapre_data(values_object)
        df = pd.DataFrame(data, columns=values_columns)
        
        df.to_excel('output.xlsx', sheet_name='sheet1', index=False,header=False  )
        logger.info(f"Data has been successfully exported without column headers.")
    except Exception as e:
        logger.error("error occoured while exporting file {}".format(str(e)))
        
        
    
def main(file_path):
    try:
        df = pd.read_excel(file_path,engine="openpyxl")
        values_object = defaultdict(list)

        for i , row in df.iterrows():
            text = row['Mensaje']
            prices = re.findall(price_pattern(), text, re.IGNORECASE)
            text = re.sub("\n\n","",text)
            values_object[text]= prices
        create_output_file(values_object)
    except Exception as e:
        logger.error("error occoured while reading file {}".format(str(e)))
        
        
    
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, help="Excel file path")     
    args = parser.parse_args()
    main(file_path=args.path)
    