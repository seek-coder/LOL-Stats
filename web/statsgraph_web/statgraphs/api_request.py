import requests
from dotenv import load_dotenv
import os

load_dotenv()
# print("Variables de entorno cargadas: ", os.environ)

class StatsApp:
    # ------------------ #
    #    1. summoner     #
    # ------------------ #
    # def __init__(self):

    #     self.api_key = os.getenv('API_KEY')
    #     if self.api_key is None:
    #         print("Error: No se ha encontrado la clave API.")
    #     else:
    #         print("Clave API cargada correctamente.")
    def __init__(self, api_key):
        self.api_key = api_key

    def get_response(self, url: str) -> str:
        self.response = requests.get(url)
        #self.response.raise_for_status() # valida que esté todo bien en la salida

        return self.response.json()
    
    def get_player_puuid(self, region: str, game_name: str, tag_line: str) -> str:
        
        self.api_url= f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}?api_key={self.api_key}"

        self.player_data = self.get_response(self.api_url)

        self.player_puuid = self.player_data["puuid"]

        return self.player_puuid

    # -------------------- #
    # 2. lista de matches  #
    # -------------------- #
    def get_matches_list(self, region: str, player_puuid: str) -> list:

        self.api_url= f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{player_puuid}/ids?start=0&count=30&api_key={self.api_key}"

        self.matches_list = self.get_response(self.api_url)

        return self.matches_list

    # ------------------ #
    #     3. match       #
    # ------------------ #
    def get_match_data(self, region: str, match_id: int, player_puuid: str) -> dict:

        # ----- estructura de la api ----- #
        self.api_url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={self.api_key}"

        self.match_data = self.get_response(self.api_url)
        self.player_index = self.match_data["metadata"]["participants"].index(player_puuid)
        self.player_info = self.match_data["info"]["participants"][self.player_index]

        
        # KDA: (asesinatos + asistencias)/ muertes

        return {
            "win": self.player_info["win"],
            "championName": self.player_info["championName"],
            "teamId": self.player_info["teamId"],
            "gameDuration": self.match_data["info"]["gameDuration"], #ms
            "gameCreation": self.match_data["info"]["gameCreation"], #unix
            "kills": self.player_info["kills"],
            "deaths": self.player_info["deaths"],
            "assists": self.player_info["assists"],
            "goldEarned": self.player_info["goldEarned"],
            "totalMinionsKilled": self.player_info["totalMinionsKilled"]
        }
    
    def get_every_match_data(self, region:str, matches_list: list, player_puuid: str) -> dict:
        matches_dict = { }

        for match_id in matches_list:
            matches_dict[match_id] = self.get_match_data(region, match_id, player_puuid)
        
        return matches_dict
    
    def get_summoner_data(self, region_specify_n: str, player_puuid: str):
        
        self.api_url = f"https://{region_specify_n}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{player_puuid}?api_key={self.api_key}"

        self.summoner_data = self.get_response(self.api_url)
        self.summoner_data_level = self.summoner_data["summonerLevel"] # long
        self.summoner_data_ico = self.summoner_data["profileIconId"] # int

        return {
            "summonerLevel": self.summoner_data_level,
            "profileIconId": self.summoner_data_ico
        }

# --- testeos --- #
if __name__ == "__main__":
    testing = StatsApp()

    region = "americas"
    game_name  = input("Mandate el game name: ")
    tag_line = input("Mandate el tag line: ").upper()
    puuid = testing.get_player_puuid(region, game_name, tag_line)
    match_id = testing.get_matches_list(region, puuid)[0]

    #print(testing.get_every_match_data(region, testing.get_matches_list(region, puuid), puuid))
    print(testing.get_summoner_data("la2", puuid))

    #https://ddragon.leagueoflegends.com/cdn/14.14.1/img/profileicon/4560.png # iconos
# -------------- #