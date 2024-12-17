import os
from transformers import AutoTokenizer, AutoModelForTokenClassification, TrainingArguments, Trainer
from datasets import load_dataset

from utils.label_utils import entity_label2id

# Load our annotated dataset (Hugging Face Datasets format)
dataset = load_dataset("json", data_files={
    "train": "data/train.json",
    "valid": "data/valid.json",
    "test":  "data/test.json"
})

model_name = "bert-base-multilingual-cased"
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
model = AutoModelForTokenClassification.from_pretrained(model_name, num_labels=len(entity_label2id))

def tokenize_and_align_labels(examples):
    tokenized_inputs = tokenizer(examples["text"], truncation=True, is_split_into_words=True)
    labels = []
    for i, words in enumerate(examples["text"]):
        word_ids = tokenized_inputs.word_ids(batch_index=i)
        example_labels = examples["labels"][i]
        aligned_labels = []
        for word_id in word_ids:
            if word_id is None:
                aligned_labels.append(-100)
            else:
                aligned_labels.append(example_labels[word_id])
        labels.append(aligned_labels)
    tokenized_inputs["labels"] = labels
    return tokenized_inputs

tokenized_dataset = dataset.map(tokenize_and_align_labels, batched=True)
tokenized_dataset = tokenized_dataset.remove_columns(["text", "labels"])  # keep only tokenized features and aligned labels

training_args = TrainingArguments(
    output_dir="models/bert_ner",
    evaluation_strategy="steps",
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=5,
    logging_steps=100,
    save_steps=500,
    eval_steps=500,
    learning_rate=5e-5,
    save_total_limit=2,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["valid"],
    tokenizer=tokenizer
)

if __name__ == "__main__":
    trainer.train()
    metrics = trainer.evaluate(tokenized_dataset["test"])
    print("BERT-based NER test metrics:", metrics)
    trainer.save_model("models/bert_ner_final")
    tokenizer.save_pretrained("models/bert_ner_final")
