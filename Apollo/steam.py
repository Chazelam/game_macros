import os
import re
import sys
import time
import ctypes
import pyautogui
from config import steam_path, steam_accounts, steam_games, non_steam_games

def window_exists(title: str) -> bool:
    hwnd = ctypes.windll.user32.FindWindowW(None, title)
    return hwnd != 0


class Steam:
    '''
    Manages Steam account login and game launching functionality.
    
    This class handles switching between Steam accounts, launching both Steam
    and non-Steam games.
    '''
    def __init__(self, 
                 steam_path: str,
                 steam_accounts: dict,
                 steam_games: dict,
                 non_steam_games: dict):
        '''
        Initialize the Steam launcher.
        
        Args:
            steam_path: Path to the Steam installation directory.
            steam_accounts: Dictionary containing Steam account information.
                Expected keys: account identifiers with 'pfp' (profile picture path).
            steam_games: Dictionary of Steam games with game configurations.
            non_steam_games: Dictionary of non-Steam games with execution configurations.
        '''
        self.steam_path = steam_path
        self.steam_accounts = steam_accounts
        self.steam_games = steam_games
        self.non_steam_games = non_steam_games


    def get_current_steam_account(self):
        '''
        Retrieve the currently logged-in Steam account ID.
        
        Parses the loginusers.vdf file to find which account was most recently used.
        
        Returns:
            Steam account ID of the most recent login, or None if not found.
            
        Raises:
            FileNotFoundError: If loginusers.vdf file is not found.
        '''
        login_file = os.path.join(self.steam_path, "config", "loginusers.vdf")
        if not os.path.exists(login_file):
            raise FileNotFoundError(f"File loginusers.vdf not found: {login_file}")

        with open(login_file, "r", encoding="utf-8") as f:
            content = f.read()
        match = re.search(r'"(\d+)"\s*\{[^}]*?"MostRecent"\s*"1"', content, re.DOTALL)
        return match.group(1) if match else None


    def _steam_login(self, acc_id: str,
                     attempts: int = 10,
                     attempts_delay: int = 2):
        '''
        Log into specified Steam account by matching the profile picture.
        
        Args:
            acc_id: Account identifier key (must exist in steam_accounts).
            attempts: Maximum number of attempts to find the profile picture.
            attempts_delay: Delay in seconds between attempts.
        
        Returns:
            True if successfully logged in, False otherwise.
            
        Raises:
            ValueError: If the account identifier is not found in steam_accounts.
        '''

        if acc_id in self.steam_accounts:
            acc_pfp_path = self.steam_accounts[acc_id]['pfp']
        else:
            raise ValueError("Unknown account identifier.")

        # TODO: Fix moveTo, currently mouse doesn't move
        pyautogui.moveTo(15, 15)  # Move cursor to screen corner

        for i in range(attempts):
            try:
                pfp = pyautogui.locateOnScreen(acc_pfp_path, confidence=0.8)
                if pfp:
                    pyautogui.click(pyautogui.center(pfp))
                    return True
            except pyautogui.ImageNotFoundException:
                print(f"[{i+1}/{attempts}] Account profile picture not found, "
                      f"retrying in {attempts_delay} seconds...")
            time.sleep(attempts_delay)

        print(f"Failed to login after {attempts} attempts.")
        return False
    

    def open_steam(self, acc_id: str,
                   attempts: int = 60,
                   attempts_delay: int = 2):
        '''
        Open Steam and ensure the correct account is logged in.
        
        Args:
            acc_id: Account identifier to log into.
            attempts: Maximum number of attempts to verify library loading.
            attempts_delay: Delay in seconds between attempts.
        
        Returns:
            True when Steam library has successfully loaded.
            
        Raises:
            RuntimeError: If Steam Library does not load within the attempt limit.
        '''
        current_acc_id = self.get_current_steam_account()
        if current_acc_id != acc_id:
            # Reopen Steam if a different account is currently logged in
            kill_steam = "Stop-Process -Name steam -ErrorAction SilentlyContinue"
            os.system(f'powershell -Command "{kill_steam}"')
            time.sleep(2)
        os.system('start steam://open/main')
        login = False

        for _ in range(attempts):
            if not login:
                if window_exists("Sign in to Steam"):
                    login = self._steam_login(acc_id=acc_id)
            try:
                loaded = pyautogui.locateOnScreen(
                    r'C:\Users\Chazelam\Code\game_macros\Apollo\steam_liberary_loaded.png',
                    confidence=0.8
                )
                if loaded:
                    return True
            except pyautogui.ImageNotFoundException:
                print("Waiting for the Steam Library to load...")
            time.sleep(attempts_delay)
        else:
            raise RuntimeError("Steam Library did not load in time.")


    def _start_steam_game(self, game_id: str):
        '''
        Start a Steam game using its game ID.
        
        Launches a game through the Steam protocol handler.
        
        Args:
            game_id: Steam game ID (numeric string).
        '''
        os.system(f'start "" "steam://rungameid/{game_id}"')
        print(f"Launching game {game_id}...")

    def _start_non_steam_game(self, command: str, dir: str):
        '''
        Start a non-Steam game by executing a command.
        
        Changes to the specified directory (if provided) and executes the given command.
        
        Args:
            command: Command to execute.
            dir: Directory to change to before execution (can be empty string).
        '''
        if dir:
            os.chdir(dir)
        os.system(command)
    

    def launch_game(self, game_name: str):
        '''
        Launch a game by name.
        
        Handles switching to the correct Steam account if necessary, then launches
        either a Steam game or a non-Steam game based on its configuration.
        
        Args:
            game_name: Name of the game to launch (must be in steam_games or non_steam_games).
            
        Raises:
            ValueError: If the game is not found in either steam_games or non_steam_games.
        '''
        if game_name in self.steam_games:
            is_steam_game = True
            game = self.steam_games[game_name]
        elif game_name in self.non_steam_games:
            is_steam_game = False
            game = self.non_steam_games[game_name]
        else:
            raise ValueError(f"Game '{game_name}' not found in game lists")

        self.open_steam(acc_id=game['account_id'])

        if is_steam_game:
            self._start_steam_game(game["game_id"])
        else:
            self._start_non_steam_game(game["command"], game["dir"])


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python steam.py <GameName>")
        sys.exit(1)

    game_name = sys.argv[1]
    steam = Steam(steam_path=steam_path,
                  steam_accounts=steam_accounts,
                  steam_games=steam_games,
                  non_steam_games=non_steam_games)
    steam.launch_game(game_name)
