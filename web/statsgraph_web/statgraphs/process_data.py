from datetime import datetime

def filter_by_win(df) -> object:
    win_filter = df['win'] == True
    df = df[win_filter]
    return df

class MatchHistory:
    def __init__(self, df):
        self.df = df 

    def win_rate(self) -> int:
        match_count = self.df.shape[0]
        only_wins = filter_by_win(self.df)
        if match_count == 0:
            return "This summoner has no recent matches"
        else:
            return round((only_wins.shape[0] / match_count) * 100, 1)

    def win_rate_by_map_side(self) -> dict:
        only_wins = filter_by_win(self.df)
        red_map = only_wins['teamId'] == 200
        blue_map = only_wins['teamId'] == 100

        red_and_win = only_wins[red_map]
        blue_and_win = only_wins[blue_map]

        red_and_win_rate = round((len(red_and_win) / only_wins.shape[0]) * 100, 1)
        blue_and_win_rate = round((len(blue_and_win) / only_wins.shape[0]) * 100, 1)

        return {'red_map': red_and_win_rate, 'blue_map': blue_and_win_rate}

    def total_time_played(self) -> str:
        seconds = self.df['gameDuration'].sum()
        hours, seconds = divmod(seconds, 3600)
        minutes, seconds = divmod(seconds, 60)
        total_time = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
        print (f"JUGASTE TODO ESTO PA: {total_time}")
        return total_time


    def total_winning_streak(self) -> int:
        shifted1 = self.df['win'].shift(1)
        shifted2 = self.df['win'].shift(2)

        winning_streak = (self.df['win'] == shifted1) & (shifted1 == shifted2)
        total_winning_streak = winning_streak.sum()

        return total_winning_streak

    def get_match_day(self, timestamp_column):
        def timestamp_to_day_of_week(timestamp) -> str:
            return datetime.fromtimestamp(timestamp / 1000).strftime('%A')
        self.df[timestamp_column] = self.df[timestamp_column].apply(timestamp_to_day_of_week)

    def get_match_hour(self, timestamp_column):
        def timestamp_to_hour(timestamp) -> int:
            return datetime.fromtimestamp(timestamp / 1000).hour
        self.df[timestamp_column] = self.df[timestamp_column].apply(timestamp_to_hour)

    def mean_farm (self) -> int:
        mean_farm_per_match = self.df['totalMinionsKilled'].sum()/self.df.shape[0]
        return mean_farm_per_match

    def get_kda(self) -> int:
        match_count = self.df.shape[0]
        kills = round(self.df['kills'].sum() / match_count, 2)
        deaths = round(self.df['deaths'].sum() / match_count, 2)
        assists = round(self.df['assists'].sum() / match_count, 2)
        print(f"GANASTE TODO ESTO PA: {kills}/{deaths}/{assists}")
        return f"{kills}/{deaths}/{assists}"
