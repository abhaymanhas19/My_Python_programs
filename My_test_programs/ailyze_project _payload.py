# Online Python compiler (interpreter) to run Python online.
# Write Python 3 code in this online editor and run it.
request_data = {}
request_data["files_ids"] = [107073, 107076, 107069, 107071, 107074, 107072, 107070, 107075]

# for summary data gathering..
request_data["get_summary"] = True

# for ai themes and user themes data gathering ..
request_data["thematic_analys_ischecked"] = True
request_data["ai_themes"] = True
request_data["user_themes"] = False
request_data["user_themes_payload"] = []

# for research question data gathering ..
request_data["research_question_ischecked"] = True
request_data["user_questions"] =[
  "what skills and competencies each school is focused on as communicated by the educators at each school and how they differ between the 2 schools",
  "how each school zeroes in on the development of these skills and competencies in their students, meaning if they use any particular specific frameworks and/or language, what kinds of experiences, activities, and guidance they engage their students in in support of the development of these identified/targeted skills and competencies, and in particular differences in all of these between the schools",
  "what other activities, mindsets, structures, practices, and experiences they employ in support of their students' growth and development, and the differences between the two schools",
  
]

# for frequency analysis data gathering ..
request_data["frequency_analysis_ischecked"] = False
request_data["theme_and_research_question_frequency"] = True
request_data["other_question_frequency"] = False
request_data["other_question_frequency_payload"] = []

# for compare viewpoint analysis data gethering
request_data["compareviewpoints_isChecked"] = True
request_data["file_category_values"] =[
  {
    "name": "Educator viewpoints from each school",
    "category": [
      {
        "name": "Da Vinci Educators",
        "files": [
          {
            "id": 107073,
            "name": "Da Vinci – Educator focus group 2 11-20-24_otter_ai.docx",
            "checked": True,
            "disabled": True
          },
          {
            "id": 107076,
            "name": "Da Vinci – Educator focus group 1 11-18-24_otter_ai.docx",
            "checked": True,
            "disabled": True
          },
          {
            "id": 107069,
            "name": "Oliver – Gibson Ek Educator 12-19-24_otter_ai.docx",
            "checked": False,
            "disabled": True
          },
          {
            "id": 107071,
            "name": "Oliver – Gibson Ek Educator 11-14-24_otter_ai.docx",
            "checked": False,
            "disabled": True
          },
          {
            "id": 107074,
            "name": "Jef – Gibson Ek Educator 12-11-24_otter_ai.docx",
            "checked": False,
            "disabled": True
          },
          {
            "id": 107072,
            "name": "Jef – Gibson Ek Educator 11-13-24_otter_ai.docx",
            "checked": False,
            "disabled": True
          },
          {
            "id": 107070,
            "name": "Colin – Gibson Ek Educator 12-10-24_otter_ai.docx",
            "checked": False,
            "disabled": True
          },
          {
            "id": 107075,
            "name": "Colin – Gibson Ek Educator 11-12-24_otter_ai.docx",
            "checked": False,
            "disabled": True
          }
        ]
      },
      {
        "name": "Gibson Ek Educators",
        "files": [
          {
            "id": 107073,
            "name": "Da Vinci – Educator focus group 2 11-20-24_otter_ai.docx",
            "checked": False,
            "disabled": True
          },
          {
            "id": 107076,
            "name": "Da Vinci – Educator focus group 1 11-18-24_otter_ai.docx",
            "checked": False,
            "disabled": True
          },
          {
            "id": 107069,
            "name": "Oliver – Gibson Ek Educator 12-19-24_otter_ai.docx",
            "checked": True,
            "disabled": True
          },
          {
            "id": 107071,
            "name": "Oliver – Gibson Ek Educator 11-14-24_otter_ai.docx",
            "checked": True,
            "disabled": True
          },
          {
            "id": 107074,
            "name": "Jef – Gibson Ek Educator 12-11-24_otter_ai.docx",
            "checked": True,
            "disabled": True
          },
          {
            "id": 107072,
            "name": "Jef – Gibson Ek Educator 11-13-24_otter_ai.docx",
            "checked": True,
            "disabled": True
          },
          {
            "id": 107070,
            "name": "Colin – Gibson Ek Educator 12-10-24_otter_ai.docx",
            "checked": True,
            "disabled": True
          },
          {
            "id": 107075,
            "name": "Colin – Gibson Ek Educator 11-12-24_otter_ai.docx",
            "checked": True,
            "disabled": True
          }
        ]
      }
    ]
  }
]
      
         
     
request_data["compare_view_categories"] = [
  {
    "name": "Educator viewpoints from each school",
    "theme_and_research_question_compare_viewpoint": True,
    "other_question_compare_viewpoint_payload": [
      
    ],
    "other_question_compare_viewpoint": False
  },
]
# other instruction gathering input by user
request_data["summary_instruction"] = ""
request_data["theme_instruction"] = ""
request_data["research_question_instruction"] = ""
request_data["selected_language"] = "English"
request_data["user_timezone"] = "UTC"
request_data["user"] = 559
# request_data["project_id"]=3821
import json

print(request_data)