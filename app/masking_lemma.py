# import re
# import yaml
# from natasha import Doc, Segmenter, MorphVocab, NewsEmbedding, NewsMorphTagger

# segmenter = Segmenter()
# morph_vocab = MorphVocab()
# emb = NewsEmbedding()
# morph_tagger = NewsMorphTagger(emb)

# def load_phrases(file_path: str):
#     """Загрузка фраз из YAML файла."""
#     with open(file_path, 'r', encoding='utf-8') as file:
#         data = yaml.safe_load(file)
#     return data['phrases']

# def lemmatize_text(text: str, mapping: dict, reverse_mapping: dict):
#     """Лемматизация текста с использованием Natasha."""
#     if not text.strip():
#         print("Предупреждение: Пустой текст для лемматизации.")
#         return text
    
#     doc = Doc(text)
#     doc.segment(segmenter)
#     doc.tag_morph(morph_tagger)
    
#     lemmatized_text = []
#     for token in doc.tokens:
#         original = token.text
#         token.lemmatize(morph_vocab)
#         lemma = token.lemma
#         lemmatized_text.append(lemma)
#         # Сохраняем исходные слова и леммы в словари
#         mapping[original] = lemma
#         reverse_mapping[lemma] = original

#     lemmatized_text = " ".join(lemmatized_text)
#     return lemmatized_text

# def escape_special_characters(text):
#     """Экранирование специальных символов в тексте."""
#     special_chars = ".^$*+?{}[]\\|()"
#     escaped_text = "".join(['\\' + char if char in special_chars else char for char in text])
#     return escaped_text

# def replace_words(text, reverse_mapping):
#     """Замена лемматизированных слов на исходные."""
#     for lemma, original in reverse_mapping.items():
#         escaped_lemma = escape_special_characters(lemma)
#         try:
#             text = re.sub(r'\b{}\b'.format(escaped_lemma), original, text, flags=re.IGNORECASE)
#         except re.error as e:
#             print(f"Ошибка при замене леммы '{lemma}': {e}")
#     return text

# def delemmatize_keys(masks_dict, reverse_mapping):
#     """Функция для восстановления исходных слов в словаре масок."""
#     new_masks_dict = {}
#     for mask, lemmatized_phrase in masks_dict.items():
#         words = lemmatized_phrase.split()
#         delemmatized_words = [reverse_mapping.get(word, word) for word in words]
#         delemmatized_phrase = ' '.join(delemmatized_words)
#         new_masks_dict[mask] = delemmatized_phrase
#     return new_masks_dict

# def remove_extra_spaces(text):
#     """Удаление лишних пробелов перед пунктуацией."""
#     text = re.sub(r'\s+([.,!?;:])', r'\1', text)
#     text = re.sub(r'\s+}', r'}', text)
#     text = re.sub(r'{\s+', r'{', text)
#     return text

# def apply_custom_masking(text: str, phrases_file_path: str):
#     """Основная функция для маскировки текста на основе заданных фраз."""
#     try:
#         phrases = load_phrases(phrases_file_path)
#     except Exception as e:
#         print(f"Ошибка при загрузке фраз: {e}")
#         return {}, text
    
#     mapping = {}
#     reverse_mapping = {}

#     try:
#         lemmatized_phrases = [lemmatize_text(phrase, mapping, reverse_mapping) for phrase in phrases]
#     except Exception as e:
#         print(f"Ошибка при лемматизации фраз: {e}")
#         return {}, text

#     try:
#         lemmatized_text = lemmatize_text(text, mapping, reverse_mapping)
#     except Exception as e:
#         print(f"Ошибка при лемматизации текста: {e}")
#         return {}, text

#     masked_text = lemmatized_text
#     masks_dict = {}
#     counter = 1

#     for lemmatized_phrase in lemmatized_phrases:
#         escaped_phrase = escape_special_characters(lemmatized_phrase)
#         try:
#             pattern = re.compile(escaped_phrase, re.IGNORECASE)
#             matches = list(pattern.finditer(lemmatized_text))
#             if matches:
#                 for match in matches:
#                     mask = f"{{CUSTOM_MASK_{counter}}}"
#                     masked_text = masked_text.replace(match.group(0), mask, 1)
#                     masks_dict[mask] = match.group(0)
#                     counter += 1
#         except re.error as e:
#             print(f"Ошибка при компиляции регулярного выражения для фразы '{lemmatized_phrase}': {e}")

#     try:
#         masked_text = replace_words(masked_text, reverse_mapping)
#     except Exception as e:
#         print(f"Ошибка при замене слов: {e}")
    
#     try:
#         masks_dict = delemmatize_keys(masks_dict, reverse_mapping)
#     except Exception as e:
#         print(f"Ошибка при де-лемматизации ключей: {e}")

#     masked_text = remove_extra_spaces(masked_text)

#     # Преобразование содержимого масок в верхний регистр
#     try:
#         pattern = re.compile(r'(?<={)(.*?)(?=})')
#         masked_text = re.sub(pattern, lambda x: x.group().upper(), masked_text)
#     except Exception as e:
#         print(f"Ошибка при преобразовании содержимого масок: {e}")

#     return masks_dict, masked_text

# # Пример использования
# if __name__ == "__main__":
#     text_path = 'path_to_your_text_file.txt'
#     phrases_file_path = 'path_to_your_phrases_yaml.yaml'
#     try:
#         with open(text_path, 'r', encoding='utf-8') as file:
#             input_text = file.read()
#         result = apply_custom_masking(input_text, phrases_file_path)
#         print("Словарь масок:", result[0])
#         print("Маскированный текст:", result[1])
#     except Exception as e:
#         print(f"Ошибка при чтении или обработке файла: {e}")
import re
import yaml
from natasha import Doc, Segmenter, MorphVocab, NewsEmbedding, NewsMorphTagger

segmenter = Segmenter()
morph_vocab = MorphVocab()
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)

def load_phrases(file_path: str):
    """Загрузка фраз из YAML файла."""
    with open(file_path, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
    return data['phrases']

def lemmatize_text(text: str, mapping: dict, reverse_mapping: dict):
    """Лемматизация текста с использованием Natasha."""
    if not text.strip():
        print("Предупреждение: Пустой текст для лемматизации.")
        return text
    
    doc = Doc(text)
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)
    
    lemmatized_text = []
    for token in doc.tokens:
        original = token.text
        token.lemmatize(morph_vocab)
        lemma = token.lemma
        lemmatized_text.append(lemma)
        mapping[original] = lemma
        reverse_mapping[lemma] = original

    lemmatized_text = " ".join(lemmatized_text)
    return lemmatized_text

def escape_special_characters(text):
    """Экранирование специальных символов в тексте."""
    special_chars = ".^$*+?{}[]\\|()"
    escaped_text = "".join(['\\' + char if char in special_chars else char for char in text])
    return escaped_text

def replace_words(text, reverse_mapping):
    """Замена лемматизированных слов на исходные."""
    for lemma, original in reverse_mapping.items():
        escaped_lemma = escape_special_characters(lemma)
        try:
            text = re.sub(r'\b{}\b'.format(escaped_lemma), original, text, flags=re.IGNORECASE)
        except re.error as e:
            print(f"Ошибка при замене леммы '{lemma}': {e}")
    return text

def delemmatize_keys(masks_dict, reverse_mapping):
    """Функция для восстановления исходных слов в словаре масок."""
    new_masks_dict = {}
    for mask, lemmatized_phrase in masks_dict.items():
        words = lemmatized_phrase.split()
        delemmatized_words = [reverse_mapping.get(word, word) for word in words]
        delemmatized_phrase = ' '.join(delemmatized_words)
        new_masks_dict[mask] = delemmatized_phrase
    return new_masks_dict

def remove_extra_spaces(text):
    """Удаление лишних пробелов перед пунктуацией."""
    text = re.sub(r'\s+([.,!?;:])', r'\1', text)
    text = re.sub(r'\s+}', r'}', text)
    text = re.sub(r'{\s+', r'{', text)
    return text

def apply_custom_masking(text: str, phrases_file_path: str):
    """Основная функция для маскировки текста на основе заданных фраз."""
    try:
        phrases = load_phrases(phrases_file_path)
    except Exception as e:
        print(f"Ошибка при загрузке фраз: {e}")
        return {}, text
    
    mapping = {}
    reverse_mapping = {}

    try:
        lemmatized_phrases = [lemmatize_text(phrase, mapping, reverse_mapping) for phrase in phrases]
    except Exception as e:
        print(f"Ошибка при лемматизации фраз: {e}")
        return {}, text

    try:
        lemmatized_text = lemmatize_text(text, mapping, reverse_mapping)
    except Exception as e:
        print(f"Ошибка при лемматизации текста: {e}")
        return {}, text

    masked_text = lemmatized_text
    masks_dict = {}
    counter = 1

    for lemmatized_phrase in lemmatized_phrases:
        escaped_phrase = escape_special_characters(lemmatized_phrase)
        try:
            pattern = re.compile(escaped_phrase, re.IGNORECASE)
            matches = list(pattern.finditer(lemmatized_text))
            if matches:
                for match in matches:
                    mask = f"{{CUSTOM_MASK_{counter}}}"
                    masked_text = masked_text.replace(match.group(0), mask, 1)
                    masks_dict[mask] = match.group(0)
                    counter += 1
        except re.error as e:
            print(f"Ошибка при компиляции регулярного выражения для фразы '{lemmatized_phrase}': {e}")

    try:
        masked_text = replace_words(masked_text, reverse_mapping)
    except Exception as e:
        print(f"Ошибка при замене слов: {e}")
    
    try:
        masks_dict = delemmatize_keys(masks_dict, reverse_mapping)
    except Exception as e:
        print(f"Ошибка при де-лемматизации ключей: {e}")

    masked_text = remove_extra_spaces(masked_text)

    # Преобразование содержимого масок в верхний регистр
    try:
        pattern = re.compile(r'{([^ ]+)}')
        masked_text = re.sub(pattern, lambda x: "{" + x.group(1).upper() + "}", masked_text)
    except Exception as e:
        print(f"Ошибка при преобразовании содержимого масок: {e}")

    return masks_dict, masked_text

# Пример использования
if __name__ == "__main__":
    text_path = 'path_to_your_text_file.txt'
    phrases_file_path = 'path_to_your_phrases_yaml.yaml'
    try:
        with open(text_path, 'r', encoding='utf-8') as file:
            input_text = file.read()
        result = apply_custom_masking(input_text, phrases_file_path)
        print("Словарь масок:", result[0])
        print("Маскированный текст:", result[1])
    except Exception as e:
        print(f"Ошибка при чтении или обработке файла: {e}")
