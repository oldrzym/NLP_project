from natasha import Segmenter, NewsEmbedding, NewsNERTagger, Doc

def natasha(text: str):
    """
    Использует NLP библиотеку Natasha для выявления и маркировки именованных сущностей в тексте.

    Args:
        text (str): Текст для анализа и маскирования.

    Returns:
        tuple: Возвращает кортеж, содержащий словарь масок и маскированный текст.
    """
    segmenter = Segmenter()  # Инициализация сегментатора для деления текста на предложения и токены
    emb = NewsEmbedding()  # Загрузка векторных представлений для русского языка
    ner_tagger = NewsNERTagger(emb)  # Инициализация NER-теггера для распознавания именованных сущностей
    doc = Doc(text)
    doc.segment(segmenter)  # Сегментация документа
    doc.tag_ner(ner_tagger)  # Применение NER-теггинга

    return mask_with_natasha(doc)

def mask_with_natasha(doc: Doc):
    """
    Применяет маскировку к тексту, заменяя именованные сущности специальными плейсхолдерами.

    Args:
        doc (Doc): Объект Doc из библиотеки Natasha, содержащий анализируемый текст и его NER-разметку.

    Returns:
        tuple: Возвращает кортеж, содержащий словарь с плейсхолдерами и маскированным текстом.
    """
    masks = {'PER': 'NAME', 'ORG': 'ORGANIZATION', 'LOC': 'LOCATION'}  # Словарь для замены типов сущностей на плейсхолдеры
    counts = {'PER': 0, 'ORG': 0, 'LOC': 0}  # Счетчики для каждого типа сущности
    masked_text = doc.text  # Начальный текст
    mask_dict = {}

    for span in doc.spans:
        counts[span.type] += 1  # Инкрементируем счетчик для данного типа сущности
        mask = f"{{{masks[span.type]}_{counts[span.type]}}}"  # Создание плейсхолдера для сущности
        masked_text = masked_text.replace(span.text, mask, 1)  # Замена сущности плейсхолдером в тексте
        mask_dict[mask] = span.text  # Запоминаем оригинальный текст сущности

    return mask_dict, masked_text
