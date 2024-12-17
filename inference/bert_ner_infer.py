from transformers import AutoTokenizer, AutoModelForTokenClassification
import torch
from utils.label_utils import id2entity_label

model_name_or_path = "models/bert_ner_final"
tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, use_fast=True)
model = AutoModelForTokenClassification.from_pretrained(model_name_or_path)
model.eval()

def predict_entities(text):
    # Tokenize the input text
    inputs = tokenizer(text.split(), return_tensors="pt", is_split_into_words=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    predictions = outputs.logits.argmax(dim=-1)
    tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
    entities = []
    for token, pred_id in zip(tokens, predictions[0].numpy()):
        if pred_id != -100:
            label = id2entity_label[pred_id]
            if label != "O":  # "O" is often the label for non-entity tokens
                entities.append((token, label))
    return entities

if __name__ == "__main__":
    sample_text = "Иванов Сергей проживает в г. Москва по ул. Ленина, д. 10"
    entity_preds = predict_entities(sample_text)
    print("Predicted Entities:", entity_preds)
