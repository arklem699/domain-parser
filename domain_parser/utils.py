import subprocess
import re
import xlsxwriter
import datetime


# Получение дат окончания регистрации доменов и составление списка словарей
def data_domains(domains, data):

    for domain in domains:

        try:
            # Вызов команды whois
            process = subprocess.Popen(['C:/Users/Administrator/Downloads/WhoIs/whois', domain], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = process.communicate()

            if process.returncode == 0:
                text_file = output.decode('utf-8')

                # Парсим у доменов Registry Expiry Date. Если достали значит домен занят
                try:
                    registry_expiry_date = re.findall( r'Registry Expiry Date:\s+(.*)\n|Expires:\s+(.*)|Expiry date:\s+(.*)|expire:\s+(.*)|Registrar Registration Expiration Date:\s+(.*)', text_file )[0]

                    # Парсим Expires несколькими регулярками. Выбираем один вариант
                    for item in registry_expiry_date:
                        if len(item) != 0:
                            registry_expiry_date = item.strip()
                            break
                    
                    # Приводим дату в нормальный формат
                    try:
                        date_obj = datetime.datetime.strptime(registry_expiry_date, '%Y-%m-%dT%H:%M:%SZ')
                    except:
                        try:
                            date_obj = datetime.datetime.strptime(registry_expiry_date, '%d-%b-%Y')
                        except:
                            print(domain, registry_expiry_date)
                            
                    date_expiry = date_obj.strftime('%d.%m.%Y')
                    print(domain, date_expiry)

                    item = {
                        'domain': domain,
                        'date_expiry': date_expiry
                    }

                    data.append(item)

                # Если registry_expiry_date распарсить не получилось, домен скорее всего свободен
                except Exception as e:
                    print(domain, e)

                    item = {
                        'domain': domain,
                        'date_expiry': 'Узнать дату окончания не получилось (Вероятно домен свободен)'
                    }

                    data.append(item)

            else:
                print(domain, error.decode('utf-8'))

        except Exception as e:
            print(domain, e)


# Запись полученных данных в excel
def dump_to_xlsx(filename, data):
    
    with xlsxwriter.Workbook(filename) as workbook:

        # Создаём таблицу и добавляем жирные заголовки
        ws = workbook.add_worksheet()
        bold = workbook.add_format({'bold': True})
        headers = ['Домен', 'Дата окончания']

        for col, h in enumerate(headers):
            ws.write_string(0, col, h, cell_format=bold)

        # Это надо, чтобы подкрашивать строки с доменами, дата окончания которых близка
        today = datetime.date.today()
        two_weeks_later = today + datetime.timedelta(weeks=2)
        one_month_later = today + datetime.timedelta(days=30)

        # Устанавливаем длину столбца "Домен" чуть большую, чем элемент максимальной длины в столбце
        max_domain_length = max(len(item['domain']) for item in data)
        ws.set_column(0, 0, max_domain_length + 1)

        # Устанавливаем длину столбца "Дата окончания" чуть большую, чем элемент максимальной длины в столбце
        max_date_expiry_length = max(len(item['date_expiry']) for item in data)
        ws.set_column(1, 1, max_date_expiry_length + 1)

        # Заполняем таблицу
        for row, item in enumerate(data, start=1):

            # Пробуем перевести строку в формат даты
            try:
                expiry_date = datetime.datetime.strptime(item['date_expiry'], '%d.%m.%Y').date()
                cell_format = None

                # Выьираем вариант подкраски (или её отсутствие)
                if expiry_date <= two_weeks_later:
                    cell_format = workbook.add_format({'bg_color': '#FF8000'})
                elif two_weeks_later < expiry_date <= one_month_later:
                    cell_format = workbook.add_format({'bg_color': '#FFFF00'})
                else:
                    cell_format = None

            # Не получится перевести, если мы не смогли раннее распарсить дату из домена
            except:
                cell_format = workbook.add_format({'bg_color': '#FF0000'})

            # Фактическая запись данных с выделением нужным цветом
            ws.write_string(row, 0, item['domain'], cell_format)
            ws.write_string(row, 1, item['date_expiry'], cell_format)