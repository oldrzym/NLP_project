
from pullenti.ner.ProcessorService import ProcessorService
from pullenti.ner.SourceOfAnalysis import SourceOfAnalysis


def pullenti_address(txt: str, type_mask: str, address_dict: dict, address_counter: int, char_counter: int = 0):
    with ProcessorService.create_processor() as proc:
        ar = proc.process(SourceOfAnalysis(txt), None, None)
        for e0_ in ar.entities:
            if e0_.type_name == type_mask:
                for i in e0_.occurrence:
                    replacement = f'{{ADDRESS_{address_counter}}}'
                    address_dict[replacement] = txt[i.begin_char - char_counter:i.end_char + 1 - char_counter]
                    txt = txt[:i.begin_char - char_counter] + replacement + txt[i.end_char - char_counter + 1:]
                    char_counter += (i.end_char - i.begin_char + 1) - len(replacement)
                    address_counter += 1
    return txt, address_dict, address_counter


def masking_address_(txt: str, address_counter: int = 1):
    address_dict = {}
    types_mask = ["ADDRESS"]

    for type_mask in types_mask:
        txt, address_dict, address_counter = pullenti_address(txt, type_mask, address_dict, address_counter)

    return address_dict, txt

