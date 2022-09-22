from typing import Dict, List, Type
from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
        training_type: str,
        duration: float,
        distance: float,
        speed: float,
        calories: float) -> None:

        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:

        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    MIN_IN_H: int = 60
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,

                 ) -> None:
        self.weigth = weight
        self.duration = duration
        self.action = action

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance_KM = self.action * self.LEN_STEP / self.M_IN_KM
        return distance_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        average_speed = self.get_distance() / self.duration
        return average_speed

    def get_spent_calories(self):
        """Получить количество затраченных калорий."""
        coeff_calorie_1: int = 18
        coeff_calorie_2: int = 20
        calories: float = ((coeff_calorie_1 * self.get_mean_speed()
    - coeff_calorie_2) * self.weigth / self.M_IN_KM * self.duration)
        return calories

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60
    LEN_STEP: float = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.weigth = weight
        self.duration = duration
        self.action = action

    def get_mean_speed(self) -> float:
        distance_KM = self.action * self.LEN_STEP / self.M_IN_KM
        average_speed = distance_KM / self.duration
        return average_speed

    def get_spent_calories(self) -> float:
        coeff_calorie_1: int = 18
        coeff_calorie_2: int = 20
        calories: float = ((coeff_calorie_1 * self.get_mean_speed()
                    - coeff_calorie_2) * self.weigth / self.M_IN_KM * self.duration * 60)
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60
    LEN_STEP: float = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int,
                 ) -> None:
        self.weigth = weight
        self.duration = duration
        self.action = action
        self.height = height

    def get_mean_speed(self) -> float:
        distance_KM = self.action * self.LEN_STEP / self.M_IN_KM
        average_speed = distance_KM / self.duration
        return average_speed

    def get_spent_calories(self) -> float:
        call_1: float = 0.035
        call_2: float = 2
        call_3: float = 0.029
        sw_calories: float = ((call_1 * self.weigth + 
        (self.get_mean_speed() ** call_2
        // self.height) * call_3 * self.weigth) * self.duration * 60)
        return sw_calories


class Swimming(Training):
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int,
                 ) -> None:
        self.weigth = weight
        self.duration = duration
        self.action = action
        self.length_pool = length_pool
        self.count_pool = count_pool
    """Тренировка: плавание."""
    def get_mean_speed(self) -> float:
        speed = (self.length_pool * self.count_pool / self.M_IN_KM
        / self.duration)
        return speed

    def get_spent_calories(self) -> float:
        calories_1: float = 1.1
        calories_2: float = 2
        calories: float = ((self.get_mean_speed() + calories_1)
        * calories_2 * self.weigth)
        return calories


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    type_of_sport: Dict[str, Type[Training]] = {'SWM': Swimming,
                                                'RUN': Running,
                                                'WLK': SportsWalking}
    if workout_type not in type_of_sport:
        raise KeyError('Не найдена тренировка')
    return type_of_sport[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)