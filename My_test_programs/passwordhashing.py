fi = {"Participant_1.docx": 261, "Participant_2.docx": 262}
c = {
    "age_group": {
        "male": {"participant_1.docx", "participant_2.docx"},
        "female": {"participant_1.docx", "participant_2.docx"},
    }
}
import json

with open("frequency.json","r") as f:
    data = json.load(f)

from collections import defaultdict
import os

def aggregate_data(entries, file_ids_array , checked_files_categories):

    files_content = defaultdict(str)
    aggregated_data = defaultdict(lambda: {"question": None, "options": []})
    for entry in entries:
        question = entry["theme"]

        if aggregated_data[question]["question"] is None:
            aggregated_data[question]["question"] = entry["theme"]
        for option in entry["frequency"]:
            if option["quotes"]:
                for document_name, value in option["quotes"].items():
                
                    if document_name not in files_content:
                        file_id = file_ids_array.get(document_name)
                        if not file_id:
                            doc_name , extension = os.path.splitext(document_name)
                            doc_name = doc_name + extension.split("(")[0]
                            file_id = file_ids_array.get(doc_name)
                        
                    #     instance = Files.objects.filter(id=file_id).first()
                    #     if not instance:
                    #         continue
                    #     text = file_text(instance.file)
                    #     files_content[document_name] = text
                    # else:
                    #     text = files_content[document_name]
                        
                    # try:
                    #     quotes_existance = check_quote(text, value["quote"], document_name)
                    # except Exception as e:
                    #     print("quotes existance checking error",e)
                    quotes_existance = [],[],True

                    if quotes_existance[2]:
                        result = {
                            "file": document_name,
                            "text": quotes_existance[0],
                            "file_id": file_id,
                            "description": value.get("elaboration"),
                            "category":None,
                            "sub-cat":None
                        }
                        for key , value in checked_files_categories.items():
                            for nested_key , nested_value in value.items():
                                if document_name.lower() in nested_value:
                                    result['category'] = key
                                    result['sub-cat'] = nested_key

                        # Find if the option already exists
                        try:
                            option_exists = False
                            for existing_option in aggregated_data[question]["options"]:
                                if existing_option["option"] == option["topic"]:
                                    
                                    for key , value in checked_files_categories.items():
                                        for nested_key , nested_value in value.items():
                                            if document_name.lower() in nested_value:
                                                existing_option['charts'][key][nested_key]+=1
                                                
                                    existing_option["results"].append(result)       
                                    existing_option["charts"]['overall'] = len(existing_option["results"])
                                    
                                    option_exists = True
                                    break

                            if not option_exists:
                                charts = {
                                    "overall":1
                                }
                                category_charts = {key : {nested_key :int(document_name.lower() in nested_values) for nested_key,nested_values in value.items()}  for key,value in checked_files_categories.items()}
                                charts.update(**category_charts)
                                # Add new option with its first result
                                aggregated_data[question]["options"].append(
                                    {
                                        "option": option.get("topic"),
                                        "description": option.get("elaboration"),
                                        "charts": charts,
                                        "results": [result],
                                    }
                                )
                        except Exception as e :
                            print("Aggreagte data error: ",e)
       
    # Convert the default dict to a regular list of dicts
    final_output = [
        {"question": key, **value} for key, value in aggregated_data.items()
    ]
    return final_output

print(aggregate_data(data,fi,c))