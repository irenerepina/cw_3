import json
from datetime import datetime


def load_and_sort_data():
    """
    Загружает файл с операциями и возвращает отсортированный по дате список
    """
    with open('/Users/mf840/coursework3/src/operations.json', 'r', encoding="utf8") as file:
        data = json.load(file)
        sorted_data = sorted(data, key=lambda x: x.get('date', ''), reverse=True)
    return sorted_data


def format_transactions(sorted_data):
    """
    Получает список, форматирует дату и возвращает 5 последних успешных операций
    """
    executed_list = []
    for s in sorted_data:
        if not s.get('from'):
            continue
        if s.get('state') == 'EXECUTED' and len(executed_list) < 5:
            date_str = s.get('date', '')
            if date_str:
                date = datetime.strptime(s['date'], '%Y-%m-%dT%H:%M:%S.%f')
                formatted_date = date.strftime('%d.%m.%Y')
                executed_list.append({'date': formatted_date,
                                     'description': s.get('description', ''),
                                      'from': s.get('from', ''),
                                      'to': s.get('to', ''),
                                      'operationAmount': s.get('operationAmount', {}).get('amount', ''),
                                      'currency': s.get('operationAmount', {}).get('currency', {}).get('name', '')
                                      })
    return executed_list


def mask_card(executed_list):
    """
    Маскирует счет или карту, выводит на экран готовый список
    """
    for e in executed_list:
        if 'Счет' in e.get('from', ''):
            e['from'] = e.get('from', '')[:5] + '**' + e.get('from', '')[-4:]
        else:
            name = e['from'][:-16]
            nums = e['from'][-16:]
            mask = nums.replace(nums[6:-4], '******')
            n = 4
            chunks = [mask[i:i + n] for i in range(0, len(mask), n)]
            e['from'] = name + ' '.join(chunks)
        if 'Счет' in e.get('to', ''):
            e['to'] = e.get('to', '')[:5] + '**' + e.get('to', '')[-4:]
        else:
            name = e['to'][:-16]
            nums = e['to'][-16:]
            mask = nums.replace(nums[6:-4], '******')
            n = 4
            chunks = [mask[i:i + n] for i in range(0, len(mask), n)]
            e['to'] = name + ' '.join(chunks)
        print(f"{e['date']} {e['description']}\n"
              f"{e['from']} -> {e['to']}\n"
              f"{e['operationAmount']} {e['currency']}\n")
    return executed_list


a = load_and_sort_data()
b = format_transactions(a)
c = mask_card(b)
