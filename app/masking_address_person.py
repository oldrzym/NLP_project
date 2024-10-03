# from pullenti.ner.ProcessorService import ProcessorService
# from pullenti.ner.SourceOfAnalysis import SourceOfAnalysis
# from pullenti.Sdk import Sdk


# def pullenti_address_person(txt: str, type_mask: str, pullenti_dict: dict, address_counter: int, person_counter: int, char_counter: int = 0):
#     with ProcessorService.create_processor() as proc:
#         ar = proc.process(SourceOfAnalysis(txt), None, None)
#         for e0_ in ar.entities:
#             if e0_.type_name == type_mask:
#                 for i in e0_.occurrence:
#                     replacement = f'{{ADDRESS_{address_counter}}}' if type_mask == 'ADDRESS' else f'{{PERSON_{person_counter}}}'
#                     pullenti_dict[replacement] = txt[i.begin_char - char_counter:i.end_char + 1 - char_counter]
#                     txt = txt[:i.begin_char - char_counter] + replacement + txt[i.end_char - char_counter + 1:]
#                     char_counter += (i.end_char - i.begin_char + 1) - len(replacement)
#                     address_counter += 1 if type_mask == 'ADDRESS' else 0
#                     person_counter += 1 if type_mask == 'PERSON' else 0
#     return txt, pullenti_dict, address_counter, person_counter


# def masking_address_person(txt: str, address_counter: int = 1, person_counter: int = 1):
#     Sdk.initialize_all()
#     pullenti_dict = {}
#     types_mask = ["ADDRESS", "PERSON"]

#     for type_mask in types_mask:
#         txt, pullenti_dict, address_counter, person_counter = pullenti_address_person(txt, type_mask, pullenti_dict, address_counter, person_counter)
    
#     return pullenti_dict, txt
from pullenti.ner.ProcessorService import ProcessorService
from pullenti.ner.SourceOfAnalysis import SourceOfAnalysis
from pullenti.Sdk import Sdk


def pullenti_address_person(txt: str, type_mask: str, pullenti_dict: dict, address_counter: int, person_counter: int, char_counter: int = 0):
    try:
        with ProcessorService.create_processor() as proc:
            ar = proc.process(SourceOfAnalysis(txt), None, None)
            if ar is None:
                raise ValueError("Analysis result is None")
            if ar.entities is None:
                raise ValueError("Entities are None")

            for e0_ in ar.entities:
                if e0_.type_name == type_mask:
                    if not e0_.occurrence:
                        continue
                    for i in e0_.occurrence:
                        replacement = f'{{ADDRESS_{address_counter}}}' if type_mask == 'ADDRESS' else f'{{PERSON_{person_counter}}}'
                        pullenti_dict[replacement] = txt[i.begin_char - char_counter:i.end_char + 1 - char_counter]
                        txt = txt[:i.begin_char - char_counter] + replacement + txt[i.end_char - char_counter + 1:]
                        char_counter += (i.end_char - i.begin_char + 1) - len(replacement)
                        address_counter += 1 if type_mask == 'ADDRESS' else 0
                        person_counter += 1 if type_mask == 'PERSON' else 0
    except Exception as e:
        print(f"Error processing text for type {type_mask}: {e}")
    return txt, pullenti_dict, address_counter, person_counter


def masking_address_person(txt: str, address_counter: int = 1, person_counter: int = 1):
    try:
        Sdk.initialize_all()
        pullenti_dict = {}
        types_mask = ["ADDRESS", "PERSON"]

        for type_mask in types_mask:
            txt, pullenti_dict, address_counter, person_counter = pullenti_address_person(txt, type_mask, pullenti_dict, address_counter, person_counter)
        
        return pullenti_dict, txt
    except Exception as e:
        print(f"Error in masking_address_person: {e}")
        return {}, txt


