import requests

class StatsApp:
    # ------------------ #
    #    1. summoner     #
    # ------------------ #
    def __init__(self):
        self.api_key = "RGAPI-dd4273cb-91b6-4537-b78d-5eafe2aaa959"

    def get_response(self, url: str) -> str:
        self.response = requests.get(url)
        self.response.raise_for_status() # valida que esté todo bien en la salida
        return self.response.json()
    
    def get_player_puuid(self, region: str, game_name: str, tag_line: str) -> str:
        
        self.api_url= f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}?api_key={self.api_key}"

        self.player_data = self.get_response(self.api_url)

        self.player_puuid = self.player_data["puuid"]

        return self.player_puuid

    # -------------------- #
    # 2. lista de matches  #
    # -------------------- #
    def get_matches_list(self, region: str, player_puuid: str) -> str:

        self.api_url= f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{player_puuid}/ids?start=0&count=20&api_key={self.api_key}" #LA2

        self.matches_list = self.get_response(self.api_url)
        self.match_id = self.matches_list[0]  

        return self.match_id

    # ------------------ #
    #     3. match       #
    # ------------------ #
    def get_match_data(self, region: str, match_id: int, player_puuid: str) -> str:

        # ----- estructura de la api ----- #
        self.api_url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={self.api_key}"

        self.match_data = self.get_response(self.api_url)
        self.match_data.keys() # me devuelve dos llaves: metadata, info
        self.match_data_info = self.match_data["info"]
        #match_data_info_participants = match_data["info"]["participants"][0] # si solo quisiera la info del primer participante
        #match_data_info_participants_champion_name = match_data["info"]["participants"][0]["championName"] # si solo quisiera el nombre del champ del primer participante
        self.match_self_player_index = self.match_data["metadata"]["participants"].index(player_puuid)
        self.match_data_self_player_info_champion = self.match_data["info"]["participants"][self.match_self_player_index]["championName"]

        return self.match_data_self_player_info_champion
    

# --- testeos --- #
testing = StatsApp()

region = "americas"
game_name  = input("Mandate el game name: ")
tag_line = input("Mandate el tag line: ").upper()
puuid = testing.get_player_puuid(region, game_name, tag_line)
match_id = testing.get_matches_list(region, puuid)


print(testing.get_match_data(region, match_id, puuid))
# -------------- #s