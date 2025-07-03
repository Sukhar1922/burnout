import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class QuestionPrototype:
    def __init__(self, id: int) -> None:
        """
            Инициализатор объекта класса прототипа вопроса.
            Хранит в себе данные вопроса, правильный ответ и балл. Так же хранятся пользовательские данные.
            :return: Ничего не возвращает
        """

        self.id = id
        self.text = None
        self.trueAnswer = None
        self.truePoints = None

        self.userAnswer = None
        self.userPoints = None

    def clear(self) -> None:
        """
            Очищает пользовательские данные в данном вопросе

            :return: Ничего не возвращает
        """

        self.userAnswer = None
        self.userPoints = None

class SymptomPrototype:
    def __init__(self, number: int) -> None:
        """
            Инициализатор объекта класса прототипа симптома выгораний
            :return: Ничего не возвращает
        """

        self._points = 0
        self._keys = None
        self._questions = None
        self.DictTrueAnswers = None
        self.symptomNumber = number

    @property
    def keys(self) -> list[int]:
        """
            Возвращает список ключей от вопросов привязанных к данному симптому.

            :return: Список ключей
            :rtype: list[int]
        """

        return self._keys

    @property
    def points(self) -> int:
        """
            Самостоятельно просуммирует баллы в своём объекте и вернёт их

            :return: Возвращает сумму баллов в выбранном симптоме
            :rtype: int
        """

        self._points = sum(list(map(lambda x: x.userPoints, self.questions())))
        return self._points

    @points.setter
    def points(self, value: int) -> None:
        """
            Нужно исключительно для тестов со стороны администратора. Функционал в обработке не несёт.

            :param value: Количество баллов для симптома
            :type value: int
        """

        self._points = value

    def Question(self, number: int) -> QuestionPrototype:
        """
            Возвращает объект вопроса по указанному номеру.

            **Правила использования:**

            :param number: Номер вопроса в соответствии с присвоенным ключом к конкретному симптому
            :type number: int
            :return: Объект запрошенного вопроса
            :rtype: QuestionPrototype
        """

        if number in self._questions:
            return self._questions[number]
        else:
            return None

    @keys.setter
    def keys(self, list_keys: list[int]) -> None:
        """
            Используется для добавления нового списка ключей. Работает динамически

            :param list_keys: Список ключей
            :type list_keys: list[int]
        """

        self._keys = list_keys
        self._questions = dict(zip(list_keys, list(map(lambda x: QuestionPrototype(x), list_keys))))

    def questions(self) -> list[QuestionPrototype]:
        """
            :return: Возвращает список объектов каждого вопроса
            :rtype: list[QuestionPrototype]
        """

        list_questions = list(map(lambda x: self._questions[x], self._questions.keys()))
        return list_questions


class PhasePrototype:
    def __init__(self) -> None:
        """
            Инициализатор объекта класса прототипа фаз формирований выгорания
            :return: Ничего не возвращает
        """

        self._symptoms_points_summary = None
        self._symptoms = [SymptomPrototype(1), SymptomPrototype(2), SymptomPrototype(3), SymptomPrototype(4)]

    def Symptom(self, number: int) -> SymptomPrototype:
        """
            Возвращает объект симптома по указанному номеру.

            **Правила использования:**

            :param number: Номер симптома в диапазоне от 1 до 4 включительно
            :type number: int
            :return: Объект запрошенного симптома
            :rtype: SymptomPrototype
            :raises ValueError: Если номер симптома вне диапазона 1-4
        """

        if not 0 < number <= len(self._symptoms):
            raise ValueError("Номер симптома должен быть от 1 до 4")
        else:
            return self._symptoms[number - 1]

    @property
    def points(self) -> int:
        """
            Самостоятельно просуммирует баллы в своём объекте и вернёт их

            :return: Возвращает сумму баллов отдельной фазы выгорания
            :rtype: int
        """

        self._symptoms_points_summary = sum(list(map(lambda x: x.points, self.symptoms())))
        return self._symptoms_points_summary

    def symptoms(self) -> list[SymptomPrototype]:
        """
            :return: Возвращает список объектов каждого симптома
            :rtype: list[SymptomPrototype]
        """

        return self._symptoms


class PhaseVoltage(PhasePrototype):
    def __init__(self) -> None:
        """
            Инициализатор объекта класса фазы формирования выгорания - НАПРЯЖЕНИЕ
            :return: Ничего не возвращает
        """

        super().__init__()
        self.Symptom(1).keys = [1, 13, 25, 37, 49, 61, 73]
        self.Symptom(2).keys = [2, 14, 26, 38, 50, 62, 74]
        self.Symptom(3).keys = [3, 15, 27, 39, 51, 63, 75]
        self.Symptom(4).keys = [4, 16, 28, 40, 52, 64, 76]

class PhaseResistance(PhasePrototype):
    def __init__(self) -> None:
        """
            Инициализатор объекта класса фазы формирования выгорания - РЕЗИСТЕНЦИЯ
            :return: Ничего не возвращает
        """

        super().__init__()
        self.Symptom(1).keys = [5, 17, 29, 41, 53, 65, 77]
        self.Symptom(2).keys = [6, 18, 30, 42, 54, 66, 78]
        self.Symptom(3).keys = [7, 19, 31, 43, 55, 67, 79]
        self.Symptom(4).keys = [8, 20, 32, 44, 56, 68, 80]

class PhaseExhaustion(PhasePrototype):
    def __init__(self) -> None:
        """
            Инициализатор объекта класса фазы формирования выгорания - ИСТОЩЕНИЕ
            :return: Ничего не возвращает
        """

        super().__init__()
        self.Symptom(1).keys = [9, 21, 33, 45, 57, 69, 81]
        self.Symptom(2).keys = [10, 22, 34, 46, 58, 70, 82]
        self.Symptom(3).keys = [11, 23, 35, 47, 59, 71, 83]
        self.Symptom(4).keys = [12, 24, 36, 48, 60, 72, 84]

class HandlerQuestions:
    def __init__(self) -> None:
        """
            Инициализатор объекта класса для общей обработки ответов тестирования
            :return: Ничего не возвращает
        """

        self._summary = None
        self.PhaseVoltage = PhaseVoltage()
        self.PhaseResistance = PhaseResistance()
        self.PhaseExhaustion = PhaseExhaustion()

        # Вызов json кеша в котором хранятся правильные ответы из БД
        json_path = os.path.join(BASE_DIR, "TruePointsAnswersQuestions.json")
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)["questions"]

        # Настройка обработчика. Загрузка правильных ответов и баллов
        for item_data in data:
            check_id = True
            for symptom in self.PhaseVoltage.symptoms():
                if item_data["id"] in symptom.keys:
                    symptom.Question(item_data["id"]).text = item_data["text"]
                    if item_data["points_yes"] != 0:
                        symptom.Question(item_data["id"]).trueAnswer = 1
                        symptom.Question(item_data["id"]).truePoints = item_data["points_yes"]
                    else:
                        symptom.Question(item_data["id"]).trueAnswer = 0
                        symptom.Question(item_data["id"]).truePoints = item_data["points_no"]
                    check_id = False
            if check_id:
                for symptom in self.PhaseResistance.symptoms():
                    if item_data["id"] in symptom.keys:
                        symptom.Question(item_data["id"]).text = item_data["text"]
                        if item_data["points_yes"] != 0:
                            symptom.Question(item_data["id"]).trueAnswer = 1
                            symptom.Question(item_data["id"]).truePoints = item_data["points_yes"]
                        else:
                            symptom.Question(item_data["id"]).trueAnswer = 0
                            symptom.Question(item_data["id"]).truePoints = item_data["points_no"]
                        check_id = False
            if check_id:
                for symptom in self.PhaseExhaustion.symptoms():
                    if item_data["id"] in symptom.keys:
                        symptom.Question(item_data["id"]).text = item_data["text"]
                        if item_data["points_yes"] != 0:
                            symptom.Question(item_data["id"]).trueAnswer = 1
                            symptom.Question(item_data["id"]).truePoints = item_data["points_yes"]
                        else:
                            symptom.Question(item_data["id"]).trueAnswer = 0
                            symptom.Question(item_data["id"]).truePoints = item_data["points_no"]

    def handle_answers(self, data: list[dict[int, int]]) -> list[int]:
        """
            Данный метод служит для обработки пользовательских ответов. Возвращает список баллов для каждого симптома

            **Правила использования:**

            :param data: Список словарей с пользовательскими данными [id - номер вопроса, answer - пользовательский ответ]
            :type data: list[dict[int, int]]
            :return: Список суммы баллов каждого симптома
            :rtype: list[int]
        """

        for item_data in data:
            check_id = True
            for symptom in self.PhaseVoltage.symptoms():
                if item_data["id"] in symptom.keys:
                    if symptom.Question(item_data["id"]).trueAnswer == item_data["answer"]:
                        symptom.Question(item_data["id"]).userAnswer = symptom.Question(item_data["id"]).trueAnswer
                        symptom.Question(item_data["id"]).userPoints = symptom.Question(item_data["id"]).truePoints
                    else:
                        symptom.Question(item_data["id"]).userAnswer = item_data["answer"]
                        symptom.Question(item_data["id"]).userPoints = 0
                    check_id = False
            if check_id:
                for symptom in self.PhaseResistance.symptoms():
                    if item_data["id"] in symptom.keys:
                        if symptom.Question(item_data["id"]).trueAnswer == item_data["answer"]:
                            symptom.Question(item_data["id"]).userAnswer = symptom.Question(item_data["id"]).trueAnswer
                            symptom.Question(item_data["id"]).userPoints = symptom.Question(item_data["id"]).truePoints
                        else:
                            symptom.Question(item_data["id"]).userAnswer = item_data["answer"]
                            symptom.Question(item_data["id"]).userPoints = 0
                        check_id = False
            if check_id:
                for symptom in self.PhaseExhaustion.symptoms():
                    if item_data["id"] in symptom.keys:
                        if symptom.Question(item_data["id"]).trueAnswer == item_data["answer"]:
                            symptom.Question(item_data["id"]).userAnswer = symptom.Question(item_data["id"]).trueAnswer
                            symptom.Question(item_data["id"]).userPoints = symptom.Question(item_data["id"]).truePoints
                        else:
                            symptom.Question(item_data["id"]).userAnswer = item_data["answer"]
                            symptom.Question(item_data["id"]).userPoints = 0

        # Сборка суммы баллов каждого симптома в списке
        list_symptoms = []
        for i in range(1, len(self.PhaseVoltage.symptoms()) + 1):
            list_symptoms.append(self.PhaseVoltage.Symptom(i).points)
        for i in range(1, len(self.PhaseResistance.symptoms()) + 1):
            list_symptoms.append(self.PhaseResistance.Symptom(i).points)
        for i in range(1, len(self.PhaseExhaustion.symptoms()) + 1):
            list_symptoms.append(self.PhaseExhaustion.Symptom(i).points)
        return list_symptoms

    @property
    def points(self) -> int:
        """
            Самостоятельно просуммирует баллы в своём объекте и вернёт их

            :return: Возвращает сумму баллов всех фаз выгорания
            :rtype: int
        """

        self._summary = self.PhaseVoltage.points + self.PhaseResistance.points + self.PhaseExhaustion.points
        return self._summary


if __name__ == "__main__":
    from test import test_print_question, test_summary_answers, generate_test_list_answers

    hq = HandlerQuestions()

    # test 1: Проверка вопросов на загрузку значений
    phase_id, symptom_id, question_id = 1, 1, 1
    test_print_question(hq, phase_id, symptom_id, question_id)

    # Готовый массив данных
    user_answers = [{'id': 1, 'answer': 1}, {'id': 2, 'answer': 0}, {'id': 3, 'answer': 1}, {'id': 4, 'answer': 0}, {'id': 5, 'answer': 1}, {'id': 6, 'answer': 1}, {'id': 7, 'answer': 0}, {'id': 8, 'answer': 0}, {'id': 9, 'answer': 1}, {'id': 10, 'answer': 1}, {'id': 11, 'answer': 0}, {'id': 12, 'answer': 1}, {'id': 13, 'answer': 1}, {'id': 14, 'answer': 1}, {'id': 15, 'answer': 0}, {'id': 16, 'answer': 1}, {'id': 17, 'answer': 1}, {'id': 18, 'answer': 1}, {'id': 19, 'answer': 1}, {'id': 20, 'answer': 0}, {'id': 21, 'answer': 1}, {'id': 22, 'answer': 0}, {'id': 23, 'answer': 1}, {'id': 24, 'answer': 1}, {'id': 25, 'answer': 1}, {'id': 26, 'answer': 0}, {'id': 27, 'answer': 0}, {'id': 28, 'answer': 1}, {'id': 29, 'answer': 0}, {'id': 30, 'answer': 0}, {'id': 31, 'answer': 0}, {'id': 32, 'answer': 0}, {'id': 33, 'answer': 1}, {'id': 34, 'answer': 0}, {'id': 35, 'answer': 1}, {'id': 36, 'answer': 1}, {'id': 37, 'answer': 0}, {'id': 38, 'answer': 0}, {'id': 39, 'answer': 0}, {'id': 40, 'answer': 0}, {'id': 41, 'answer': 1}, {'id': 42, 'answer': 1}, {'id': 43, 'answer': 1}, {'id': 44, 'answer': 0}, {'id': 45, 'answer': 0}, {'id': 46, 'answer': 1}, {'id': 47, 'answer': 1}, {'id': 48, 'answer': 0}, {'id': 49, 'answer': 1}, {'id': 50, 'answer': 0}, {'id': 51, 'answer': 1}, {'id': 52, 'answer': 1}, {'id': 53, 'answer': 1}, {'id': 54, 'answer': 1}, {'id': 55, 'answer': 1}, {'id': 56, 'answer': 0}, {'id': 57, 'answer': 0}, {'id': 58, 'answer': 1}, {'id': 59, 'answer': 0}, {'id': 60, 'answer': 0}, {'id': 61, 'answer': 1}, {'id': 62, 'answer': 1}, {'id': 63, 'answer': 1}, {'id': 64, 'answer': 0}, {'id': 65, 'answer': 0}, {'id': 66, 'answer': 0}, {'id': 67, 'answer': 0}, {'id': 68, 'answer': 0}, {'id': 69, 'answer': 0}, {'id': 70, 'answer': 1}, {'id': 71, 'answer': 0}, {'id': 72, 'answer': 0}, {'id': 73, 'answer': 1}, {'id': 74, 'answer': 1}, {'id': 75, 'answer': 0}, {'id': 76, 'answer': 0}, {'id': 77, 'answer': 0}, {'id': 78, 'answer': 1}, {'id': 79, 'answer': 0}, {'id': 80, 'answer': 1}, {'id': 81, 'answer': 1}, {'id': 82, 'answer': 1}, {'id': 83, 'answer': 0}, {'id': 84, 'answer': 0}]

    # Выбор для обработки
    if input("Напишите 1 или 2:\n1. Загрузить готовый массив данных\n2. Сгенерировать новый массив данных\nОтвет: ") == str(1):
        print(hq.handle_answers(user_answers))
    else:
        hq.handle_answers(generate_test_list_answers())

    # test 2: Проверка вопросов на обработку введенного массива ответов
    phase_id, symptom_id, question_id = 1, 1, 1
    test_print_question(hq, phase_id, symptom_id, question_id)

    # test 3: Сумма ответов
    test_summary_answers(hq)
