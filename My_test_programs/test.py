# import polars as pl
# import requests

# # df = pl.scan_csv("workshop.csv")
# # df = df.collect()
# # for i in df.iter_rows(named=True):
# payload ={
#     "email":"maria.ghazzaoui@gmail.com",
#     "password":"P@ssword123",
#     "confirm_password":"P@ssword123"
# }
# url = "https://ai.ailyze.com/api/register-user/"
# response = requests.post(url=url,json=payload)
# if response.status_code == 201:
#     print("Successfully created user with email %s")
# else:
#     print("Failed to create user with email %s")




def migrate_categories(old_categories,new_categories):
    import copy
    old_map = {category['name'] : category for category in old_categories}
    to_add = []

    for new_category in new_categories:
        if new_category['name'] in old_map:
            existing = old_map[new_category['name']]

            sub_map = {sub_cat['name'] : sub_cat for sub_cat in existing['category']}
            
            for sub_cat in new_category['category']:
                if sub_cat['name'] in sub_map:
                    sub_map[sub_cat['name']]['files'].extend(sub_cat['files'])
                    
                else:
                    existing['category'].append(copy.deepcopy(sub_cat))

        else:
            to_add.append(copy.deepcopy(new_category))
    merged = list(old_map.values())
    merged.extend(to_add)
    return merged
  

data = [
  {
    "name": "gender",
    "category": [
      {
        "name": "male",
        "files": [
          {
            "id": 3936,
            "name": "23.docx",
            "checked": True,
            "disabled": True
          },
          {
            "id": 3982,
            "name": "23.docx",
            "checked": True,
            "disabled": True
          }
        ]
      },
      {
        "name": "female",
        "files": [
          
          {
            "id": 3936,
            "name": "23.docx",
            "checked": True,
            "disabled": True
          },
          {
            "id": 3982,
            "name": "23.docx",
            "checked": True,
            "disabled": True
          }
        ]
      }
    ]
  }
]
data1 = [
  {
    "name": "giender",
    "category": [
      {
        "name": "jmale",
        "files": [
          {
            "id": 3936,
            "name": "23.docx",
            "checked": True,
            "disabled": True
          },
          {
            "id": 3982,
            "name": "23.docx",
            "checked": True,
            "disabled": True
          }
        ]
      },
      {
        "name": "female",
        "files": [
          
          {
            "id": 3936,
            "name": "23.docx",
            "checked": True,
            "disabled": True
          },
          {
            "id": 3982,
            "name": "23.docx",
            "checked": True,
            "disabled": True
          }
        ]
      }
    ]
  }
]
result = migrate_categories(data,data1)
print(result)