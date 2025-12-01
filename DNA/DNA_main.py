import time
import random
import vgamepad as vg
from tqdm import tqdm


# создаём виртуальный геймпад Xbox 360
gamepad = vg.VX360Gamepad()


def randomized_delay(delay:float, 
                     rng_time_variation: float = 0.1, 
                     p_bar: bool = False, 
                     desc: str = "Ожидание"):
    """
    Задержка в секундах с добавлением случайного разброса.
    base_delay - в секундах
    rng_time_variation - максимальная погрешность в секундах
    p_bar - отображать прогресс-бар или нет
    """
    t = delay + random.uniform(0, rng_time_variation)

    if p_bar:
        for _ in tqdm(range(int(t)), 
                      desc=f"  {desc} {t:.1f}s", 
                      bar_format='{l_bar}{bar}', 
                      ncols=50):
            time.sleep(1)
    else:
        time.sleep(t)



def gamepad_button_press(button: str, 
                         press_duration:float = 0.1, 
                         rng_time_variation: float = 0.1):
    """
    Нажимает указанную кнопку геймпада на заданное время.

    Параметры:
        button (str): строковое обозначение кнопки:
            - 'A', 'B', 'X', 'Y' — основные кнопки
            - 'UP', 'DOWN', 'LEFT', 'RIGHT' — крестовина (D-Pad)
            - 'LB', 'RB' — плечевые кнопки
            - 'L3', 'R3' — кнопки стиков
            - 'START', 'BACK', 'GUIDE' — системные кнопки

        press_duration (float): длительность нажатия в секундах.

        rng_time (bool): использовать ли случайную погрешность при ожидании.
    """
    match button.upper():
        # Основные кнопки
        case 'Y':
            btn = vg.XUSB_BUTTON.XUSB_GAMEPAD_Y
        case 'A':
            btn = vg.XUSB_BUTTON.XUSB_GAMEPAD_A
        case 'B':
            btn = vg.XUSB_BUTTON.XUSB_GAMEPAD_B
        case 'X':
            btn = vg.XUSB_BUTTON.XUSB_GAMEPAD_X

        # Крестовина (D-Pad)
        case 'DPAD_UP' | 'UP':
            btn = vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP
        case 'DPAD_DOWN' | 'DOWN':
            btn = vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN
        case 'DPAD_LEFT' | 'LEFT':
            btn = vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT
        case 'DPAD_RIGHT' | 'RIGHT':
            btn = vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT

        # Плечевые кнопки
        case 'LB' | 'L1' | 'LEFT_SHOULDER':
            btn = vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER
        case 'RB' | 'R1' | 'RIGHT_SHOULDER':
            btn = vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER

        # Стики (кнопки нажатия)
        case 'L3' | 'LEFT_THUMB':
            btn = vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB
        case 'R3' | 'RIGHT_THUMB':
            btn = vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB

        # Системные кнопки
        case 'START':
            btn = vg.XUSB_BUTTON.XUSB_GAMEPAD_START
        case 'BACK':
            btn = vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK
        case 'GUIDE' | 'HOME':
            btn = vg.XUSB_BUTTON.XUSB_GAMEPAD_GUIDE

        # По умолчанию - ошибка
        case _:
            raise ValueError(
                "Unsupported button. Use one of: "
                "'A', 'B', 'X', 'Y', 'UP', 'DOWN', 'LEFT', 'RIGHT', "
                "'LB', 'RB', 'L3', 'R3', 'START', 'BACK', 'GUIDE'."
            )

    # нажимаем кнопку
    gamepad.press_button(btn)
    gamepad.update()

    # ждём со случайной погрешностью
    randomized_delay(delay=press_duration, rng_time_variation=rng_time_variation)
 
    # отпускаем кнопку
    gamepad.release_button(btn)
    gamepad.update()


def gamepad_dna_action(action:str):
        # нажимаем кнопку
    match action.lower():
        case 'ultimate' | 'ult':
            # Зажатие LB
            btn1 = vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER
            gamepad.press_button(btn1)
            gamepad.update()
            randomized_delay(delay=0.2, rng_time_variation=0.1)

            # Зажатие Y
            btn2 = vg.XUSB_BUTTON.XUSB_GAMEPAD_Y
            gamepad.press_button(btn2)
            gamepad.update()
            randomized_delay(delay=0.1, rng_time_variation=0.1)

            # Отпускание кнопок
            gamepad.release_button(btn1)
            gamepad.release_button(btn2)
            gamepad.update()
            return

        case 'position_reset':
            # Переход в настройки внутри комиссии
            gamepad_button_press('START')
            randomized_delay(1)
            gamepad_button_press('DPAD_RIGHT', press_duration=0.1, rng_time_variation=0.1)
            randomized_delay(1)
            gamepad_button_press('A')
            randomized_delay(1)

            # Переходд в нужную вкладку
            for _ in range(5):
                gamepad_button_press('RB')
                randomized_delay(delay=0.1, rng_time_variation=0.1)
           
            # Выбор и подтверждение сброса
            for _ in range(2):
                gamepad_button_press('DPAD_DOWN', press_duration=0.1, rng_time_variation=0.1)
                randomized_delay(0.2, rng_time_variation=0.1)
            
            gamepad_button_press('A')
            randomized_delay(0.3, rng_time_variation=0.2)
            gamepad_button_press('A')            
            return


def expulsion_run(iteration: int = 0, 
                  load_delay: int = 10, 
                  clear_delay: int = 60, 
                  position_reset: bool = False, 
                  ult_use: bool = False):
    """
    Выполняет одну итерацию нажатий кнопок геймпада с задержкой.
    """
    if iteration:
        print(f"\n--- итерация {iteration} ---")

    print("Начало комиссии...")
    gamepad_button_press("Y")
    randomized_delay(2)

    print("Выбор мануала...")
    gamepad_button_press("A")

    print("Ожидание загрузки...")
    randomized_delay(load_delay, p_bar=True, desc="Загрузка") 

    if position_reset:
        print("Сброс позиции...")
        gamepad_dna_action('position_reset')
        randomized_delay(2, p_bar=False)  
    if ult_use:
        print("Использование ультимейта...")
        gamepad_dna_action('ult')

    print("Ожидание прохождения...")
    randomized_delay(clear_delay, unit='s') 

    if iteration:
        print(f"  Итерация {iteration} завершена.")


if __name__ == "__main__":
    print("Ожидание перед стартом (5 секунд)...")
    randomized_delay(5, p_bar=True, rng_time_variation=0)
    i = 1
    while True:
        expulsion_run(i, 
                      load_delay=10, 
                      clear_delay=50,
                      position_reset=True,
                      ult_use=True)
        i += 1
