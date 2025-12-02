import os
import re
import sys
import time
import pyautogui
from pyautogui import ImageNotFoundException


class Exe():
    pass


class Steam():
    steam_path      = r"C:\Program Files (x86)\Steam"
    steam_accaunts  = {}
    steam_games     = {
        "Nier_Automata": {"game_id": "524220",  "account": "kz", "account_id": "76561199728650271"},
        "Stellar_Blade": {"game_id": "3489700", "account": "kz", "account_id": "76561199728650271"},

        "Hollow_Knight": {"game_id": "367520",  "account": "ru", "account_id": "76561199117729436"},
        "SilkSong":      {"game_id": "1030300", "account": "ru", "account_id": "76561199117729436"},
        "PalWorld":      {"game_id": "1623730", "account": "ru", "account_id": "76561199117729436"},
        "NoExistence":   {"game_id": "287380",  "account": "ru", "account_id": "76561199117729436"}
    }
    non_steam_games = {
        "Elden_Ring":    {"command": "",        "account": "kz", "account_id": "76561199728650271"}
    }

    def steam_login(self,
                    acc: str, 
                    re_login: bool = True, 
                    attempts: int = 10):
        kill_steam = "Get-Process -Name steam -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue"
        steam_exe = os.path.join(self.steam_path, "Steam.exe")


        # TODO: Заменить на словарь в self
        match acc:
            case 'kz':
                acc_pfp_path = r'C:\Users\Chazelam\Documents\AutoHotkey\steam_pfp\kz.png'
            case 'ru':
                acc_pfp_path = r'C:\Users\Chazelam\Documents\AutoHotkey\steam_pfp\ru.png'
            case _:
                raise ValueError("Unknown account identifier.")

        if re_login:
            os.system(f'powershell -Command "{kill_steam}"')
            time.sleep(5)
        os.system(f'start "" "{steam_exe}"')

        time.sleep(10)  # Ждем загрузки Steam

        pyautogui.moveTo(15, 15)  # перемещаем курсор в угол экрана

        for i in range(attempts):
            try:
                pfp = pyautogui.locateOnScreen(acc_pfp_path, confidence=0.8)
                if pfp:
                    pyautogui.click(pyautogui.center(pfp))
                    return True
            except ImageNotFoundException:
                print(f"[{i+1}/{attempts}] Изображение не найдено, повтор через 2 секунды...")
            time.sleep(2)

        print(f"Не удалось найти изображение после {attempts} попыток.")
        return False

    def get_current_steam_account(self):
        login_file = os.path.join(self.steam_path, "config", "loginusers.vdf")
        if not os.path.exists(login_file):
            raise FileNotFoundError(f"Файл loginusers.vdf не найден: {login_file}")

        with open(login_file, "r", encoding="utf-8") as f:
            content = f.read()
        match = re.search(r'"(\d+)"\s*\{[^}]*?"MostRecent"\s*"1"', content, re.DOTALL)
        return match.group(1) if match else None

    def _start_steam_game(game_id: str):
        os.system(f'start "" "steam://rungameid/{game_id}"')
        print(f"Запускаем игру {game_id}...")

    def _start_non_steam_game(self):
        pass


    def launch_game(self, game_name: str):
        if game_name in self.steam_games:
            is_steam_game = True
        elif game_name in self.non_steam_games:
            is_steam_game = False      
        else:
            print(f"Игра {game_name} не найдена в словаре!")
            return

        game = self.steam_games[game_name]
        current_acc = self.get_current_steam_account()

        if current_acc != game["account_id"]:
            print(f"Нужен аккаунт {game['account']}, переключаем...")
            success = self.steam_login(game["account"])
            if not success:
                print("Не удалось переключить аккаунт, выходим.")
                return
        else:
            print(f"Текущий аккаунт правильный: {game['account']}")

        # time.sleep(5)  # Ждем стабилизации после входа
        if is_steam_game:
            self._start_steam_game(game["game_id"])
        else:
            self._start_non_steam_game(game["game_id"])


class Monitior():
    pass


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python launch.py <GameName>")
        sys.exit(1)

    game_name = sys.argv[1]
    # launch_game(game_name)
