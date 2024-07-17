import pandas as pd
import matplotlib.pyplot as plt
from process_data import MatchHistory

class CreatePlt:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def winrate_per_day_plot(self) -> plt.Figure:
        match_history = MatchHistory(self.df)
        match_history.get_match_day('gameCreation')
        filtered_history = match_history.filter_by_win()
        victories_by_day = filtered_history['gameCreation'].value_counts()
        total_victories = victories_by_day.sum()

        if total_victories > 0:
            win_rate_by_day = (victories_by_day / total_victories) * 100
        else:
            win_rate_by_day = 0

        fig, ax = plt.subplots()
        win_rate_by_day.plot(kind='bar', ax=ax)
        ax.set_xlabel('Día de la semana')
        ax.set_ylabel('Porcentaje de victorias')
        ax.set_title('Tasa de victorias según el día de la semana')
        plt.show()

        return fig

    def winrate_per_hour_plot(self) -> plt.Figure:
        match_history = MatchHistory(self.df)
        match_history.get_match_hour('gameCreation')
        filtered_history = match_history.filter_by_win()
        victories_by_hour = filtered_history['gameCreation'].value_counts()
        total_victories = victories_by_hour.sum()

        if total_victories > 0:
            win_rate_by_hour = (victories_by_hour / total_victories) * 100
        else:
            win_rate_by_hour = 0

        fig, ax = plt.subplots()
        win_rate_by_hour.plot(kind='bar', ax=ax)
        ax.set_xlabel('Hora')
        ax.set_ylabel('Porcentaje de victorias')
        ax.set_title('Tasa de victorias según la hora del día')
        plt.show()
        
        return fig