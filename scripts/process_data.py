from datetime import datetime

class MatchHistory:
    def __init__(self, df):
        self.df = df 

    def match_count(self) -> int:
        return len(self.df)

    def win_count(self):
        return (self.df['win'] == True).sum()

    def lose_count(self):
        return (self.df['win'] == False).sum()

    def win_rate(self) -> int:
        match_count = self.match_count()
        if match_count == 0:
            return "This summoner has no recent matches"
        else:
            return round((self.win_count() / match_count) * 100, 1)

    def filter_by_win(self) -> object:
        win_filter = self.df['win'] == True
        self.df = self.df[win_filter]
        return self.df

    def win_rate_by_map_side(self) -> dict:
        win_count = self.win_count()
        if win_count == 0:
            return {'red_map': 0, 
                    'blue_map': 0}

        red_map = self.df.filter_by_win()['teamId'] == 200
        blue_map = self.df.filter_by_win()['teamId'] == 100

        red_and_win = self.df.filter_by_win()[red_map]
        blue_and_win = self.df.filter_by_win()[blue_map]

        red_and_win_rate = round((len(red_and_win) / win_count) * 100, 1)
        blue_and_win_rate = round((len(blue_and_win) / win_count) * 100, 1)

        return {'red_map': red_and_win_rate, 'blue_map': blue_and_win_rate}

    def total_time_played(self) -> str:
        seconds = self.df['gameDuration'].sum() / 1000
        hours, seconds = divmod(seconds, 3600)
        minutes, seconds = divmod(seconds, 60)
        total_time = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
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

    def mean_farm(self):
        mean_farm_per_match = self.df['totalMinionsKilled'].sum()/self.df.shape[0]
        return mean_farm_per_match

    def mean_kda(self) -> int:
        if self.df['deaths'] > 0:
            mean_kda_per_match = (self.df['kills'].sum() + self.df['assists'].sum()) / self.df['deaths'].sum()
            return mean_kda_per_match
        else:
            return "Sos el mejor jugador del mundo"