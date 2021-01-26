def get_centre(stat):    # Получить центр между примерно равными суммами
    length = sum([pare[1] for pare in stat])    # Сумма вхождений всех символов
    new_length = 0    # Новая сумма
    diff = length    # Разница между новой и старой суммами
    for index, (symbol, amount) in enumerate(stat):    # Цикл по списку символов и их вхождений
        length -= amount    # Обновление старой суммы
        new_length += amount    # Обновление новой суммы
        if abs(length - new_length) >= diff:    # Если модуль разницы очередных сумм меньше разницы предыдущих сумм
            return index    # Вернуть индекс очередной итерации
        else:
            diff = abs(length - new_length)    # Обновить значение разницы сумм


def get_codes(stat, code=''):    # Получить коды символов
    if len(stat) <= 1:    # Если длинна списка символов и их вхождений равна 1
        return {stat[0][0]: code}    # Вернкть словарь с символом и его кодом
    centre = get_centre(stat)    # Получить центр между примерно равными суммами
    left_codes = get_codes(stat[0:centre], code + '0')    # Получить коды символов слева от центра
    right_codes = get_codes(stat[centre: len(stat)], code + '1')    # Получить коды символов справа от центра
    left_codes.update(right_codes)    # Соединить словари с ливыми и правыми кодами
    return left_codes    # Вернуть итоговый словарь с кодами


def decode_symbol(table, code, index=0):    # Раскодировать символ
    if len(table) <= 1:    # Если длинна списка символов и их вхождений равна 1
        return table[0][0]    # Вернуть единственный символ символ
    centre = get_centre(table)    # Получить центр между примерно равными суммами
    if code[index] == '0':    # Если очередной символ равен 0
        return decode_symbol(table[0:centre], code, index + 1)    # Рекурентный вызов для символов слева от центра
    else:    # Если очередной символ равен 1
        return decode_symbol(table[centre: len(table)], code, index + 1)    # Рекурентный вызов для символов справа от центра


def main():
    phrase = ''    # Пустая фраза

    with open('../../OneDrive/AOD/phrase.txt', 'r') as file:    # Открыть файл
        for line in file:    # Цикл по файлу
            phrase += line    # Добавить строку к фразу

    stat = {}    # Пустой словарь вхождений символов

    for symbol in phrase:    # Цикл по фразе
        if symbol in stat:    # Если очередной символ есть в словаре
            stat[symbol] += 1
        else:    # Если очередного символа нет в словаре
            stat[symbol] = 1

    stat_list = list(stat.items())    # Сортировка словаря вхождений
    stat_list.sort(key=lambda x: x[1], reverse=True)
    sorted_stat = dict(stat_list)
    print(sorted_stat)
    
    code_table = get_codes(list(sorted_stat.items()))    # Таблица с кодами символов

    for symbol, code in code_table.items():    # Вывод кодов символов на экран
        print(f'{symbol}: {code}')

    encoded_phrase = ''    # Пустая строка закодированной фразы
    for symbol in phrase:    # Цикл по фразе
        encoded_phrase += code_table[symbol]    # Добавить к закодированной фразе код символа

    print(f'Закодированная фраза: {encoded_phrase}')
    print(f'Объём - {len(encoded_phrase)} бит')
    index = 0
    decoded_phrase = ''    # Пустая строка раскодированной фразы

    while index < len(encoded_phrase):    # Цикл для индекса от 0 до длины закодированной фразы
        current = decode_symbol(list(sorted_stat.items()), encoded_phrase, index)    # Расшифровать очередной символ
        decoded_phrase += current    # Добавить его в результат
        index += len(code_table[current])    # Перейти на следующий

    print('Расшифрованная фраза: ', decoded_phrase)
    print(f'Объём - {len(decoded_phrase) * 8} бит')


if __name__ == '__main__':
    main()
