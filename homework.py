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
    MIN_IN_H: float = 60
    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000

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
        # переопределение метода расчета калорий в каждом классе
        raise NotImplementedError(f'метод не определен'
        f' в классе {self.__class__.__name__}')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    COEFF_MEAN_SPEED_1: float = 18
    COEFF_MEAN_SPEED_2: float = 20

    def get_spent_calories(self) -> float:
        return ((self.COEFF_MEAN_SPEED_1
                * ((self.action
                 * self.LEN_STEP
                 / self.M_IN_KM)
                 / self.duration)
                - self.COEFF_MEAN_SPEED_2)
                * self.weigth
                / self.M_IN_KM
                * self.duration
                * self.MIN_IN_H)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_OF_WEIGHT_1: float = 0.035
    COEFF_OF_WEIGHT_2: float = 0.029
    COEFF_OF_EXPONENTIATION: float = 2

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
        return (self.action * self.LEN_STEP / self.M_IN_KM) / self.duration

    def get_spent_calories(self) -> float:
        return ((self.COEFF_OF_WEIGHT_1
                * self.weigth
                + (self.get_mean_speed()
                 ** self.COEFF_OF_EXPONENTIATION
                 // self.height)
                 * self.COEFF_OF_WEIGHT_2
                * self.weigth)
                * self.duration
                * self.MIN_IN_H)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    COEFF_OF_MEAN_SPEED_1: float = 1.1
    COEFF_OF_WEGHT: float = 2

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

    def get_mean_speed(self) -> float:
        return (self.length_pool
                * self.count_pool
                / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed()
                + self.COEFF_OF_MEAN_SPEED_1)
                * self.COEFF_OF_WEGHT
                * self.weigth)


TYPES_OF_SPORTS: Dict[str, Type[Training]] = {
    'SWM': Swimming,
    'RUN': Running,
    'WLK': SportsWalking,
}


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type not in TYPES_OF_SPORTS:
        raise ValueError(f'Тренировка не найдена {workout_type}')
    return TYPES_OF_SPORTS[workout_type](*data)


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