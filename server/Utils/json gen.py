import random
import json

dict = {}
dict['TG_ID'] = '@Лёлик-алкоголик'

lst = []
for id in range(1, 84+1):
    lst.append({
        'id': id,
        'answer': random.randint(0, 1)
    })

dict['Answers'] = lst
with open('answers.json', 'w') as file:
    json.dump(dict, file, indent=4)