from requests import delete, get, post, put

print('Корректное создание работы')
data_json = {"team_leader": 1, "job": "Hard work",
             "collaborators": "1, 2, 3", "work_size": 90}
print(post('http://localhost:8080/api/jobs', json=data_json).json())

print('Обновление созданной записи')
data_json = {"team_leader": 111, "job": "Easy work",
             "collaborators": "11, 222, 3333", "work_size": 10}
print(put('http://localhost:8080/api/job/1', json=data_json).json())

print('Создание работы без id team_leader-а')
data_json = {"job": "Hard work", "collaborators": "1, 2, 3", "work_size": 90}
print(post('http://localhost:8080/api/jobs', json=data_json).json())

print('Создание работы без work_size')
data_json = {"team_leader": 1, "job": "Hard work", "collaborators": "1, 2, 3"}
print(post('http://localhost:8080/api/jobs', json=data_json).json())

print('Создание работы без job')
data_json = {"team_leader": 1, "collaborators": "1, 2, 3", "work_size": 90}
print(post('http://localhost:8080/api/jobs', json=data_json).json())

print('Создание работы без collaborators')
data_json = {"team_leader": 1, "job": "Hard work", "work_size": 90}
print(post('http://localhost:8080/api/jobs', json=data_json).json())

print("Получение всех записей")
print(get('http://localhost:8080/api/jobs', json=data_json).json())

print("Удаление записи")
print(delete('http://localhost:8080/api/job/1', json=data_json).json())

print("Удаление всех записей")
print(delete('http://localhost:8080/api/jobs', json=data_json).json())

