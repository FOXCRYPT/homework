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
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self):
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    COEFF_CALORIE_1: float = 18
    COEFF_CALORIE_2: float = 20

    def get_spent_calories(self) -> float:
        return ((self.COEFF_CALORIE_1 * ((self.action * self.LEN_STEP
                / self.M_IN_KM) / self.duration)
                - self.COEFF_CALORIE_2)
                * self.weigth
                / self.M_IN_KM
                * self.duration * self.MIN_IN_H)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    call_1: float = 0.035
    call_2: float = 2
    call_3: float = 0.029

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
        return distance_KM / self.duration

    def get_spent_calories(self) -> float:
        return ((self.call_1 * self.weigth
                + (self.get_mean_speed()
                 ** self.call_2
                 // self.height) * self.call_3
                * self.weigth) * self.duration * self.MIN_IN_H)


class Swimming(Training):
    LEN_STEP: float = 1.38
    calories_1: float = 1.1
    calories_2: float = 2

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
        return (self.length_pool * self.count_pool
                / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.calories_1)
                * self.calories_2 * self.weigth)


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    type_of_sport: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking}
    if workout_type not in type_of_sport:
        raise KeyError('Не найдена тренировка')
    return type_of_sport[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        main(read_package(workout_type, data))