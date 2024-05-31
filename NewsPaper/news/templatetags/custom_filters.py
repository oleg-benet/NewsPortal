from django import template


register = template.Library()

class CensorException(Exception):
    pass

spec_symb = ['!', ',', '.', '?', '-', '"', '(', ')', '[', ']', '…']

@register.filter()
def censor(text):
    try:
        if isinstance(text, str):
            list_txt = text.split()
            result = []
            for word in list_txt:
                censor_word = word[0]
                if word[0] == word[0].upper() and not word[0].isdigit():
                    censor_word = word[0]
                    for i in range(1, len(word)):
                        if word[i] not in spec_symb:
                            censor_word = censor_word + '*'
                        else:
                            censor_word = censor_word + word[i]
                else:
                    censor_word = word
                result.append(censor_word)
            return (' '.join(result))
        else:
            raise CensorException
    except CensorException:
        print("Фильтр censor применен не к строковой величине" )
