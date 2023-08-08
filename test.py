import json
import requests
from bs4 import BeautifulSoup
import os


# Выбираем страницу откуда собираем данные

url = 'https://freelance.habr.com/tasks?q=python'
task_name = url.split('=')[-1]




def get_tasks(url, task_name):
    """получаем задачи"""
    task_list = []
    url_list =[]
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    posts = soup.find_all('article')
    for post in posts:
        title = post.find('div', class_='task__title').get('title')
        urls = 'https://freelance.habr.com/' + post.find('div', class_='task__title').find('a').get('href')
        try:
            price = post.find('div', class_='task__price').find('span', class_='count').text
        except:
            price = '___'

        task_list.append({
            'title' : title,
            'urls' : urls,
            'price' : price
        })
        # url_list.append(f'{title}:{price},{urls}')
        url_list.append(urls)
    with open('url_clients.txt', 'a') as file:
        for line in url_list:
            file.write(f'{line}\n')


    # вторая часть чтение всех url заказчиков и парсинг их заказов
    with open('url_clients.txt') as file:

        lines = [line.strip() for line in file.readlines()]


        count = 0
        data_dict = []
        for line in lines:
            q = requests.get(line)
            result = q.content

            soup = BeautifulSoup(result, 'lxml')
            try:
                client = soup.find(class_='fullname').text  # имя заказчика
                client_url = soup.find(class_='fullname').find('a')
                client_tasks = soup.find(class_='task__title').text  # заголовок задания
                content = soup.find(class_='task__description').text  # описание заказа
                stack = soup.find(class_='tags__item_link').text  # на каком ЯП надо выполнить заказ
                files = soup.find(class_='files-list__link')  # сбор файлов для ТЗ
                contacts = soup.find(class_='sidebar-block user_contacts').text  # данные пользователя
                telephone = soup.find(class_='verified', title=True)["title"]  # верификация телефона
                completed_task = soup.find(class_='value').text  # завершенные заказы кол-во

                data = {
                    'client': client,
                    'client_url': client_url,
                    'client_tasks': client_tasks,
                    'content': content,
                    'stack ': stack,
                    'files': files,
                    'contacts': contacts,
                    'telephone': telephone,
                    'completed_task': completed_task,
                }
                count += 1

                # выводим данные для нагляжности
                print(
                    f'Заказчику {client}  {client_url}  нужно сделать  {client_tasks} c пояснением  {content} на ЯП  {stack} (файлы  {files})'
                    f' данные пользователя  {contacts}  {telephone}, завершенные заказы заказчика {completed_task}')

                data_dict.append(data)

                with open('answer.txt', 'a') as file:
                    for line in data_dict:
                        file.write(f'{line}')


            except:
                print("error 404")

    # запись в json
    write_json(task_list, task_name)

def write_json(tasks, task_name):

    """пишем задачи в джейсон файл"""
    if not os.path.exists('reports'):
        os.mkdir('reports')
    with open(f'reports/{task_name}_tasks_habr.json', "w", encoding="utf-8") as file:
        json.dump(tasks[0:], file, indent=4, ensure_ascii=False)

def pars_json():
    with open(f'reports/{task_name}_tasks_habr.json') as f:
        data = json.load(f)

    return data
pars_json()

# def main():
#     urls_to_parse = ['https://freelance.habr.com/tasks?q=python',
#                     # 'https://freelance.habr.com/tasks?q=javascript',
#                     ]
#
#     for url in urls_to_parse:
#         print(url)
#         task_name = url.split('=')[-1]
#         for i in range(1, 4):
#             url = f'https://freelance.habr.com/tasks?page={i}&q={task_name}'
#             job = get_tasks(url, task_name)
#
#         return job
#
#
# if __name__ == '__main__':
#     main()





