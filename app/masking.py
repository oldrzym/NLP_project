import re
from .regex_loader import regex_patterns, masking_order
from .natasha_masking import natasha
from .masking_address_person import masking_address_person
from pullenti.Sdk import Sdk
from .masking_lemma import apply_custom_masking
from .mask_text_numbers import mask_text_numbers

def mask_with_regex(text: str, pattern_info: dict, masks_dict: dict, counters: dict) -> tuple[str, dict]:
    if "masking_patterns" not in pattern_info or not pattern_info["masking_patterns"]:
        print("Masking patterns are missing or empty.")
        return masks_dict, text

    pattern_info = pattern_info["masking_patterns"][0]

    prefix = pattern_info["prefix"]
    for regex in pattern_info["regex"]:
        matches = re.finditer(regex, text)
        for match in matches:
            counters[prefix] = counters.get(prefix, 0) + 1
            mask_id = f"{prefix}_{counters[prefix]}"
            mask_placeholder = f"{{{mask_id}}}"
            if mask_placeholder not in masks_dict:
                masks_dict[mask_placeholder] = match.group()
                text = re.sub(regex, mask_placeholder, text, count=1)
            else:
                print(f"Duplicate mask {mask_placeholder} found. Skipping...")
    return masks_dict, text


def apply_masking(text: str):
    masked_text = text
    masks_dict = {}
    counters = dict()

    natasha_dict = {}  
    pullenti_masks = {}  
    lemma_masks = {}  
    number_masks = {}  
    regex_masks = {}

    for pattern_name in masking_order:
        if pattern_name == "natasha":
            natasha_dict, masked_text = natasha(masked_text)
        elif pattern_name == "pullenti":
            pullenti_masks, masked_text = masking_address_person(masked_text)
        elif pattern_name == "custom_lemmatization":
            lemma_masks, masked_text = apply_custom_masking(masked_text, 'app/config/phrases.yaml')
        elif pattern_name == "mask_text_numbers":
            number_masks, masked_text = mask_text_numbers(masked_text)
        else:
            pattern_info = regex_patterns.get(pattern_name, {})
            if "masking_patterns" in pattern_info:  
                regex_masks, masked_text = mask_with_regex(masked_text, pattern_info, masks_dict, counters)
            else:
                print(f"No masking patterns found for {pattern_name}")

        print(f"Current text after {pattern_name}: {masked_text}")

    masks_dict = {**natasha_dict, **pullenti_masks, **lemma_masks, **number_masks, **regex_masks}

    # masks_dict = {**natasha_dict, **pullenti_masks, **regex_masks}
    return {
        "text": text,
        "masked_text": masked_text,
        "masks_dict": masks_dict
    }


