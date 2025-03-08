import pandas as pd
from transformers import pipeline

# Load your Excel file
file_path = "/home/jarvis/Downloads/Python_Django Interview!Try Every question at your best. (1-78).xlsx"
df = pd.read_excel(file_path, engine='openpyxl')

# Initialize AI detector (this will download the model on first run)
ai_detector = pipeline(
    'text-classification',
    model='roberta-base-openai-detector'
)

def is_human_content(text, threshold=0.5):
    """
    Determine if text is human-written using AI detection model
    Returns True if human-written, False if AI-generated
    """
    if pd.isna(text) or len(str(text).strip()) == 0:
        return False
    
    # Truncate text to model's max length (512 tokens ~ 2000 characters)
    truncated_text = str(text)[:2000]
    
    try:
        result = ai_detector(truncated_text)[0]
        return result['label'] == 'Real' and result['score'] >= threshold
    except:
        return False

# Find human-written content IDs
# human_content_ids = []

for index, row in df.iterrows():
    email = row[8]
    ID =  row[0]
    print(row)
    try:
        if is_human_content(row['content']):  # Replace 'content' with your text column name
            human_content_ids.append(row['id'])  # Replace 'id' with your ID column name
    except KeyError as e:
        print(f"Error: Column not found - {e}")
        exit()

# Display results
# print(f"\nTotal rows analyzed: {len(df)}")
# print(f"Potential human-written content IDs ({len(human_content_ids)}):")
# print(human_content_ids)

# Optional: Save results to a text file
# with open('human_content_ids.txt', 'w') as f:
#     f.write('\n'.join(map(str, human_content_ids)))