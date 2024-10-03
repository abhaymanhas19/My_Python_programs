from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

# Load Meta fine-tuned model and tokenizer
model_name = "meta-fine-tuned-model"  # Replace with your model name
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=8)

# Prepare training data
train_encodings = tokenizer(train_data["ingredients"], return_tensors="pt", max_length=512, padding="max_length", truncation=True)
train_labels = torch.tensor(train_data["label"])

# Train model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
criterion = nn.CrossEntropyLoss()
optimizer = AdamW(model.parameters(), lr=1e-5)

for epoch in range(5):
    model.train()
    total_loss = 0
    for batch in train_encodings:
        input_ids = batch["input_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)
        labels = batch["labels"].to(device)
        optimizer.zero_grad()
        outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    print(f"Epoch {epoch+1}, Loss: {total_loss / len(train_encodings)}")


# Evaluate model on testing data
test_data = pd.read_csv("your_test_data.csv")
test_encodings = tokenizer(test_data["ingredients"], return_tensors="pt", max_length=512, padding="max_length", truncation=True)
test_labels = torch.tensor(test_data["label"])

model.eval()
test_loss = 0
correct = 0
with torch.no_grad():
    for batch in test_encodings:
        input_ids = batch["input_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)
        labels = batch["labels"].to(device)
        outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
        loss = criterion(outputs, labels)
        test_loss += loss.item()
        _, predicted = torch.max(outputs.scores, dim=1)
        correct += (predicted == labels).sum().item()

accuracy = correct / len(test_data)
print(f"Test Accuracy: {accuracy:.4f}")

# Evaluate model on testing data
test_encodings = tokenizer(test_data["text"], return_tensors="pt", max_length=512, padding="max_length", truncation=True)
test_labels = torch.tensor(test_data["label"])

model.eval()
test_loss = 0
correct = 0
with torch.no_grad():
    for batch in test_encodings:
        input_ids = batch["input_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)
        labels = batch["labels"].to(device)
        outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
        loss = criterion(outputs, labels)
        test_loss += loss.item()
        _, predicted = torch.max(outputs.scores, dim=1)
        correct += (predicted == labels).sum().item()

accuracy = correct / len(test_data)
print(f"Test Accuracy: {accuracy:.4f}")


# Save trained model and tokenizer
model.save_pretrained("your_model_directory")
tokenizer.save_pretrained("your_tokenizer_directory")



# Load saved model and tokenizer
model = AutoModelForSequenceClassification.from_pretrained("your_model_directory")
tokenizer = AutoTokenizer.from_pretrained("your_tokenizer_directory")

# Use model for inference
input_text = "Your input text here"
input_ids = tokenizer.encode(input_text, return_tensors="pt")
outputs = model(input_ids)