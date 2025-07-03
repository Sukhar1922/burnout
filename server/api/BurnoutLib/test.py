def test_print_question(object_hq, Phase_id, Symptom_id, Question_id):
    print('____________________________________________________')
    print()
    if Phase_id == 1:
        print("Фаза: PhaseVoltage")
        print()
        print("Статус фазы:", object_hq.PhaseVoltage.status)
        print(f"Статус симптома №{object_hq.PhaseVoltage.Symptom(Symptom_id).symptomNumber}:",
              object_hq.PhaseVoltage.Symptom(Symptom_id).status)
        print()
        print("ID:", object_hq.PhaseVoltage.Symptom(Symptom_id).Question(Question_id).id)
        print("Вопрос:", object_hq.PhaseVoltage.Symptom(Symptom_id).Question(Question_id).text)
        print("Правильный ответ:", object_hq.PhaseVoltage.Symptom(Symptom_id).Question(Question_id).trueAnswer)
        print("Баллы за правильный ответ:",
              object_hq.PhaseVoltage.Symptom(Symptom_id).Question(Question_id).truePoints)
        print()
        print("Пользовательский ответ:",
              object_hq.PhaseVoltage.Symptom(Symptom_id).Question(Question_id).userAnswer)
        print("Пользовательский балл за вопрос:",
              object_hq.PhaseVoltage.Symptom(Symptom_id).Question(Question_id).userPoints)
    elif Phase_id == 2:
        print("Фаза: PhaseResistance")
        print()
        print("Статус фазы:", object_hq.PhaseResistance.status)
        print(f"Статус симптома №{object_hq.PhaseResistance.Symptom(Symptom_id).symptomNumber}:",
              object_hq.PhaseResistance.Symptom(Symptom_id).status)
        print()
        print("ID:", object_hq.PhaseResistance.Symptom(Symptom_id).Question(Question_id).id)
        print("Вопрос:", object_hq.PhaseResistance.Symptom(Symptom_id).Question(Question_id).text)
        print("Правильный ответ:", object_hq.PhaseResistance.Symptom(Symptom_id).Question(Question_id).trueAnswer)
        print("Баллы за правильный ответ:",
              object_hq.PhaseResistance.Symptom(Symptom_id).Question(Question_id).truePoints)
        print()
        print("Пользовательский ответ:",
              object_hq.PhaseResistance.Symptom(Symptom_id).Question(Question_id).userAnswer)
        print("Пользовательский балл за вопрос:",
              object_hq.PhaseResistance.Symptom(Symptom_id).Question(Question_id).userPoints)
    elif Phase_id == 3:
        print("Фаза: PhaseExhaustion")
        print()
        print("Статус фазы:", object_hq.PhaseExhaustion.status)
        print(f"Статус симптома №{object_hq.PhaseExhaustion.Symptom(Symptom_id).symptomNumber}:",
              object_hq.PhaseExhaustion.Symptom(Symptom_id).status)
        print()
        print("ID:", object_hq.PhaseExhaustion.Symptom(Symptom_id).Question(Question_id).id)
        print("Вопрос:", object_hq.PhaseExhaustion.Symptom(Symptom_id).Question(Question_id).text)
        print("Правильный ответ:", object_hq.PhaseExhaustion.Symptom(Symptom_id).Question(Question_id).trueAnswer)
        print("Баллы за правильный ответ:",
              object_hq.PhaseExhaustion.Symptom(Symptom_id).Question(Question_id).truePoints)
        print()
        print("Пользовательский ответ:",
              object_hq.PhaseExhaustion.Symptom(Symptom_id).Question(Question_id).userAnswer)
        print("Пользовательский балл за вопрос:",
              object_hq.PhaseExhaustion.Symptom(Symptom_id).Question(Question_id).userPoints)
    else:
        print("Не тот номер фазы")
    print()
    print('____________________________________________________')
    print()

def test_summary_answers(object_hq):
    print('____________________________________________________')
    print()
    print("Общий балл тестирования:", object_hq.points)
    print()
    print('____________________________________________________')
    print()
    print("Сумма баллов для PhaseVoltage:", object_hq.PhaseVoltage.points)
    for i in range(1, len(object_hq.PhaseVoltage.symptoms()) + 1):
        print(f"PhaseVoltage: Сумма баллов симптома №{object_hq.PhaseVoltage.Symptom(i).symptomNumber}:",
              object_hq.PhaseVoltage.Symptom(i).points)
    print()
    print('____________________________________________________')
    print()
    print("Сумма баллов для PhaseResistance:", object_hq.PhaseResistance.points)
    for i in range(1, len(object_hq.PhaseResistance.symptoms()) + 1):
        print(f"PhaseResistance: Сумма баллов симптома №{object_hq.PhaseResistance.Symptom(i).symptomNumber}:",
              object_hq.PhaseResistance.Symptom(i).points)
    print()
    print('____________________________________________________')
    print()
    print("Сумма баллов для PhaseExhaustion:", object_hq.PhaseExhaustion.points)
    for i in range(1, len(object_hq.PhaseExhaustion.symptoms()) + 1):
        print(f"PhaseExhaustion: Сумма баллов симптома №{object_hq.PhaseExhaustion.Symptom(i).symptomNumber}:",
              object_hq.PhaseExhaustion.Symptom(i).points)
    print('____________________________________________________')
    print()

def generate_test_list_answers():
    import random
    list_answers = []
    for i in range(1, 85):
        dict_answer = {"id": i, "answer": random.randint(0, 1)}
        list_answers.append(dict_answer)
    print()
    print("Готовый массив:")
    print(list_answers)
    print()
    return list_answers