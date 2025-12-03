import time
import random
import vgamepad as vg
from tqdm import tqdm
import pyautogui
from pyautogui import ImageNotFoundException


# create a virtual Xbox 360 gamepad
gamepad = vg.VX360Gamepad()


def randomized_delay(delay:float, 
                     rng_time_variation: float = 0.1, 
                     p_bar: bool = False, 
                     desc: str = "Waiting"):
    '''
    Delay in seconds with added random jitter.

    :param delay: Base delay in seconds.
    :type delay: float
    :param rng_time_variation: Maximum time variation in seconds.
    :type rng_time_variation: float
    :param p_bar: Whether to display a progress bar.
    :type p_bar: bool
    :param desc: Description used for the progress bar.
    :type desc: str
    '''
    t = delay + random.uniform(0, rng_time_variation)

    if p_bar:
        for _ in tqdm(range(int(t)), 
                      desc=f"{desc} {t:.1f}s", 
                      bar_format='{l_bar}{bar}', 
                      ncols=48):
            time.sleep(1)
        time.sleep(t - int(t))  # sleep the remaining fractional part
    else:
        time.sleep(t)


def gamepad_button_press(button: str, 
                         press_duration:float = 0.1, 
                         rng_time_variation: float = 0.1):
    '''
    Presses the specified gamepad button for a given duration.

    :param button: String identifier of the button (e.g. 'A', 'B', 'X', 'Y', 'UP', 'DOWN', 'LEFT', 'RIGHT', 'LB', 'RB', 'L3', 'R3', 'START', 'BACK', 'GUIDE').
    :type button: str
    :param press_duration: Duration of the press in seconds.
    :type press_duration: float
    :param rng_time_variation: Maximum random variation for the press duration in seconds.
    :type rng_time_variation: float
    '''
    match button.upper():
    # Main buttons
        case 'Y':
            btn = vg.XUSB_BUTTON.XUSB_GAMEPAD_Y
        case 'A':
            btn = vg.XUSB_BUTTON.XUSB_GAMEPAD_A
        case 'B':
            btn = vg.XUSB_BUTTON.XUSB_GAMEPAD_B
        case 'X':
            btn = vg.XUSB_BUTTON.XUSB_GAMEPAD_X

    # D-Pad
        case 'DPAD_UP' | 'UP':
            btn = vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP
        case 'DPAD_DOWN' | 'DOWN':
            btn = vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN
        case 'DPAD_LEFT' | 'LEFT':
            btn = vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT
        case 'DPAD_RIGHT' | 'RIGHT':
            btn = vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT

    # Shoulder buttons
        case 'LB' | 'L1' | 'LEFT_SHOULDER':
            btn = vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER
        case 'RB' | 'R1' | 'RIGHT_SHOULDER':
            btn = vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER

    # Thumbstick buttons (presses)
        case 'L3' | 'LEFT_THUMB':
            btn = vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB
        case 'R3' | 'RIGHT_THUMB':
            btn = vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB

    # System buttons
        case 'START':
            btn = vg.XUSB_BUTTON.XUSB_GAMEPAD_START
        case 'BACK':
            btn = vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK
        case 'GUIDE' | 'HOME':
            btn = vg.XUSB_BUTTON.XUSB_GAMEPAD_GUIDE

    # Default - error
        case _:
            raise ValueError(
                "Unsupported button. Use one of: "
                "'A', 'B', 'X', 'Y', 'UP', 'DOWN', 'LEFT', 'RIGHT', "
                "'LB', 'RB', 'L3', 'R3', 'START', 'BACK', 'GUIDE'."
            )

    # press the button
    gamepad.press_button(btn)
    gamepad.update()

    randomized_delay(delay=press_duration, rng_time_variation=rng_time_variation)
 
    # release the button
    gamepad.release_button(btn)
    gamepad.update()


def gamepad_dna_action(action:str):
    match action.lower():
        case 'ultimate' | 'ult':
            # Hold LB
            btn1 = vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER
            gamepad.press_button(btn1)
            gamepad.update()
            randomized_delay(delay=0.2, rng_time_variation=0.1)

            # Press Y
            btn2 = vg.XUSB_BUTTON.XUSB_GAMEPAD_Y
            gamepad.press_button(btn2)
            gamepad.update()
            randomized_delay(delay=0.1, rng_time_variation=0.1)

            # Release buttons
            gamepad.release_button(btn1)
            gamepad.release_button(btn2)
            gamepad.update()
            return

        case 'position_reset':
            # Enter settings inside the commission
            gamepad_button_press('START')
            randomized_delay(1)
            gamepad_button_press('DPAD_RIGHT', press_duration=0.1, rng_time_variation=0.1)
            randomized_delay(1)
            gamepad_button_press('A')
            randomized_delay(1)

            # Navigate to the required tab
            for _ in range(5):
                gamepad_button_press('RB')
                randomized_delay(delay=0.1, rng_time_variation=0.1)
           
            # Select and confirm the reset
            for _ in range(2):
                gamepad_button_press('DPAD_DOWN', press_duration=0.1, rng_time_variation=0.1)
                randomized_delay(0.2, rng_time_variation=0.1)
            
            gamepad_button_press('A')
            randomized_delay(0.3, rng_time_variation=0.2)
            gamepad_button_press('A')            
            return

def locate_on_sreen(img_path: str, 
                    attempts: int = 5,
                    attempt_delay: float = 2, 
                    confidence: float = 0.8,
                    description: str = "Locating Image"):
    '''
    Attempts to locate an image on the screen multiple times.
    
    :param img_path: Path to the image file to locate.
    :type img_path: str
    :param attempts: Number of attempts to locate the image.
    :type attempts: int
    :param attempt_delay: Delay between attempts in seconds.
    :type attempt_delay: float
    :param confidence: Confidence level for image matching (0 to 1).
    :type confidence: float
    '''

    for _ in tqdm(range(int(attempts)), 
                    desc=description, 
                    bar_format='{l_bar}{bar}', 
                    ncols=48):
        try:
            img = pyautogui.locateOnScreen(img_path, confidence)
            return img
        except ImageNotFoundException:
            pass
        time.sleep(attempt_delay)
    return False


def expulsion_run(iteration: int = 0, 
                  load_delay: int = 10,
                  position_reset: bool = False, 
                  ult_use: bool = False,
                  use_manual: bool = False):
    '''
    Executes a single run of the expulsion mission in the game.
    
    :param iteration: Description
    :type iteration: int
    :param load_delay: Description
    :type load_delay: int
    :param clear_delay: Description
    :type clear_delay: int
    :param position_reset: Description
    :type position_reset: bool
    :param ult_use: Description
    :type ult_use: bool
    :param use_manual: Description
    :type use_manual: bool
    '''
    if iteration:
        print(f"\n--- iteration {iteration} ---")

    print("Starting commission...")
    gamepad_button_press("Y")
    randomized_delay(1)

    print("Selecting manual...")
    if use_manual:
        gamepad_button_press('DPAD_RIGHT', press_duration=0.05, rng_time_variation=0.1)
    randomized_delay(1)
    gamepad_button_press("A")

    print("Waiting for loading...")
    randomized_delay(load_delay, p_bar=True, desc="Loading") 
    if position_reset:
        print("Resetting position...")
        gamepad_dna_action('position_reset')
        randomized_delay(2)  
    if ult_use:
        print("Using ultimate...")
        gamepad_dna_action('ult')

    print("Waiting for run to complete...")
    randomized_delay(20, p_bar=True, desc="Run") 

    again = r'C:\Users\Chazelam\Documents\AutoHotkey\DNA\Rhythm.png'
    locate_on_sreen(again, attempts=30, confidence=0.8)

    if iteration:
        print(f"  Iteration {iteration} completed.")


if __name__ == "__main__":
    print("Waiting before start (5 seconds)...")
    randomized_delay(5, p_bar=True, rng_time_variation=0)
    i = 1
    while True:
        expulsion_run(i, 
                      load_delay=8, 
                      position_reset=True,
                      ult_use=True,
                      use_manual=False)
        i += 1
