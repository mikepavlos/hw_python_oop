from dataclasses import asdict, dataclass
from typing import Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MESSAGE = ('Тип тренировки: {training_type}; '
               'Длительность: {duration:.3f} ч.; '
               'Дистанция: {distance:.3f} км; '
               'Ср. скорость: {speed:.3f} км/ч; '
               'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_IN_HR = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        self.action: int = action
        self.duration_h: float = duration
        self.weight_kg: float = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration_h

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            f'Метод "get_spent_calories" в дочернем классе '
            f'{type(self).__name__} не переопределён.')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration_h,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    RUN_CAL_MEAN_SPEED_MULTIPLIER = 18
    RUN_CAL_MULT_MEAN_SPEED_SUBTRACTOR = 20

    def get_spent_calories(self) -> float:
        calories_per_min: float = (
            (self.RUN_CAL_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
             - self.RUN_CAL_MULT_MEAN_SPEED_SUBTRACTOR) * self.weight_kg
            / self.M_IN_KM
        )
        return calories_per_min * self.duration_h * self.MIN_IN_HR


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    WLK_CAL_WEIGHT_MULTIPLIER_1 = 0.035
    WLK_CAL_WEIGHT_MULTIPLIER_2 = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height_cm: float = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories_per_min: float = (
            self.WLK_CAL_WEIGHT_MULTIPLIER_1 * self.weight_kg
            + (self.get_mean_speed() ** 2 // self.height_cm)
            * self.WLK_CAL_WEIGHT_MULTIPLIER_2 * self.weight_kg
        )
        return calories_per_min * self.duration_h * self.MIN_IN_HR


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    SWM_CAL_MEAN_SPEED_ADDITION = 1.1
    SWM_CAL_WEIGHT_DOUBLER = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool_m: float = length_pool
        self.count_pool: int = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool_m * self.count_pool / self.M_IN_KM
                / self.duration_h)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + self.SWM_CAL_MEAN_SPEED_ADDITION)
                * self.SWM_CAL_WEIGHT_DOUBLER * self.weight_kg)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_type: dict[str, Type[Swimming | Running | SportsWalking]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type not in training_type:
        raise ValueError(f'Тип тренировки "{workout_type}" не найден. '
                         f'Коды доступных тренировок: {[*training_type]}')
    else:
        return training_type[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages: list[tuple[str, list[int]]] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180])
    ]

    for workout_type, data in packages:
        training: Training = read_package(workout_type, data)
        main(training)
