import os
import re
import sys
import time
import pyautogui
from pyautogui import ImageNotFoundException


class Steam():
    """
    Manages Steam account login and game launching functionality.
    
    This class handles switching between Steam accounts, launching both Steam
    and non-Steam games, and managing account information.
    """
    def __init__(self, 
                 steam_path: str,
                 steam_accaunts: dict,
                 steam_games: dict,
                 non_steam_games: dict):
        """
        Initialize the Steam launcher.
        
        :param steam_path: Path to the Steam installation directory
        :type steam_path: str
        :param steam_accaunts: Dictionary containing Steam account information
        :type steam_accaunts: dict
        :param steam_games: Dictionary of Steam games
        :type steam_games: dict
        :param non_steam_games: Dictionary of non-Steam games
        :type non_steam_games: dict
        """
        self.steam_path       = steam_path
        self.steam_accaunts   = steam_accaunts
        self.steam_games      = steam_games
        self.non_steam_games  = non_steam_games


    def steam_login(self,
                    acc: str, 
                    re_login: bool = True, 
                    attempts: int = 10):
        """
        Log into a Steam account.
        
        Switches to the specified Steam account by matching the profile picture.
        Optionally kills the Steam process before logging in to ensure a fresh start.
        
        :param acc: Account identifier key (must exist in steam_accaunts)
        :type acc: str
        :param re_login: Whether to kill Steam and restart before login
        :type re_login: bool
        :param attempts: Maximum number of attempts to find the profile picture
        :type attempts: int
        :return: True if successfully logged in, False otherwise
        :rtype: bool
        :raises ValueError: If the account identifier is not found in steam_accaunts
        """
        kill_steam = "Get-Process -Name steam -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue"
        steam_exe = os.path.join(self.steam_path, "Steam.exe")

        if acc in self.steam_accaunts:
            acc_pfp_path = self.steam_accaunts[acc]['pfp']
        else:
            raise ValueError("Unknown account identifier.")

        if re_login:
            os.system(f'powershell -Command "{kill_steam}"')
            time.sleep(5)
        os.system(f'start "" "{steam_exe}"')

        # TODO: Ensure Steam is fully loaded
        time.sleep(10)  # Wait for Steam to load

        # TODO: fix moveTo, currently mouse dosn't move
        pyautogui.moveTo(15, 15)  # Move cursor to screen corner

        for i in range(attempts):
            try:
                pfp = pyautogui.locateOnScreen(acc_pfp_path, confidence=0.8)
                if pfp:
                    pyautogui.click(pyautogui.center(pfp))
                    return True
            except ImageNotFoundException:
                print(f"[{i+1}/{attempts}] Image not found, retrying in 2 seconds...")
            time.sleep(2)

        print(f"Failed to find image after {attempts} attempts.")
        return False

    def get_current_steam_account(self):
        """
        Retrieve the currently logged-in Steam account ID.
        
        Parses the loginusers.vdf file to find which account was most recently used.
        
        :param self: Instance reference
        :return: Steam account ID of the most recent login, or None if not found
        :rtype: str or None
        :raises FileNotFoundError: If loginusers.vdf file is not found
        """
        login_file = os.path.join(self.steam_path, "config", "loginusers.vdf")
        if not os.path.exists(login_file):
            raise FileNotFoundError(f"File loginusers.vdf not found: {login_file}")

        with open(login_file, "r", encoding="utf-8") as f:
            content = f.read()
        match = re.search(r'"(\d+)"\s*\{[^}]*?"MostRecent"\s*"1"', content, re.DOTALL)
        return match.group(1) if match else None

    def _start_steam_game(self, game_id: str):
        """
        Start a Steam game using its game ID.
        
        Launches a game through the Steam protocol handler.
        
        :param game_id: Steam game ID
        :type game_id: str
        """
        os.system(f'start "" "steam://rungameid/{game_id}"')
        print(f"Launching game {game_id}...")

    def _start_non_steam_game(self, command: str, dir: str):
        """
        Start a non-Steam game by executing a command.
        
        Changes to the specified directory (if provided) and executes the given command.
        
        :param command: Command to execute
        :type command: str
        :param dir: Directory to change to before execution (can be empty string)
        :type dir: str
        """
        if dir:
            os.chdir(dir)
        os.system(command)


    def launch_game(self, game_name: str):
        """
        Launch a game by name.
        
        Handles switching to the correct Steam account if necessary, then launches
        either a Steam game or a non-Steam game based on its configuration.
        
        :param game_name: Name of the game to launch (must be in steam_games or non_steam_games)
        :type game_name: str
        :return: None
        :raises ValueError: If the game is not found in either steam_games or non_steam_games.
        """
        if game_name in self.steam_games:
            is_steam_game = True
            game = self.steam_games[game_name]
        elif game_name in self.non_steam_games:
            is_steam_game = False
            game = self.non_steam_games[game_name]
        else:
            raise ValueError(f"Game '{game_name}' not found in game lists")

        current_acc = self.get_current_steam_account()

        if current_acc != game["account_id"]:
            print(f"Need account {game['account']}, switching...")
            success = self.steam_login(game["account"])
            if not success:
                print("Failed to switch account, exiting.")
                return
        else:
            print(f"Current account is correct: {game['account']}")

        # TODO: Verify that Steam has fully loaded
        time.sleep(10)
        if is_steam_game:
            self._start_steam_game(game["game_id"])
        else:
            self._start_non_steam_game(f'{game["command"]}', f'{game["dir"]}')


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python steam.py <GameName>")
        sys.exit(1)

    steam_path      = r"C:\Program Files (x86)\Steam"
    steam_accaunts  = {
        'kz': {'id': '76561199728650271',
               'name': '',
               'pfp': r'C:\Users\Chazelam\Documents\AutoHotkey\steam_pfp\kz.png'},
        'ru': {'id': '76561199117729436',
               'name': '',
               'pfp': r'C:\Users\Chazelam\Documents\AutoHotkey\steam_pfp\ru.png'}}
    
    steam_games     = {
        "Nier_Automata": {"game_id": "524220",  "account": "kz", "account_id": "76561199728650271"},
        "Stellar_Blade": {"game_id": "3489700", "account": "kz", "account_id": "76561199728650271"},

        "Hollow_Knight": {"game_id": "367520",  "account": "ru", "account_id": "76561199117729436"},
        "SilkSong":      {"game_id": "1030300", "account": "ru", "account_id": "76561199117729436"},
        "PalWorld":      {"game_id": "1623730", "account": "ru", "account_id": "76561199117729436"},
        "NoExistence":   {"game_id": "287380",  "account": "ru", "account_id": "76561199117729436"}}
    
    non_steam_games = {
        "Elden_Ring":    {"command": "modengine2_launcher.exe -t er -c config_eldenring.toml",
                          "dir":     r"C:\Program Files (x86)\Steam\steamapps\common\ELDEN RING\ModEngine-2.1.0.0-win64",
                          "account": "kz", "account_id": "76561199728650271"}}

    game_name = sys.argv[1]
    steam = Steam(steam_path=steam_path,
                  steam_accaunts=steam_accaunts,
                  steam_games=steam_games,
                  non_steam_games=non_steam_games)
    steam.launch_game(game_name)
