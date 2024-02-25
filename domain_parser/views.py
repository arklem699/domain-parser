from django.shortcuts import render, HttpResponse
from .utils import data_domains, dump_to_xlsx


# Начальная страница
def hello(request):
    return render(request, 'index.html')


# Добавление доменов в список из формы
def adding_domains(request, domains):

    domain_list = request.POST.get('domain_list', '').strip()  # Получаем список доменов из формы
    domain_list = domain_list.split('\n')  # Разбиваем список на отдельные домены

    for domain in domain_list:
        domain = domain.strip()  # Удаляем все пробелы в начале и в конце

        if domain:  # Проверяем, что строка не пустая
            domains.append(domain)


def download(request):
    data = []
    domains = []

    adding_domains(request, domains)
    data_domains(domains, data)
    dump_to_xlsx('domain_expiry_date.xlsx', data)

    with open('domain_expiry_date.xlsx', 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=domain_expiry_date.xlsx'
        return response