import matplotlib
matplotlib.use('Agg') 
import pandas as pd
import matplotlib.pyplot as plt
from .process_data import MatchHistory, filter_by_win

class CreatePlt:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def winrate_per_day_plot(self) -> plt.Figure:
        match_history = MatchHistory(self.df)
        match_history.get_match_day("gameCreation")
        filtered_history = filter_by_win(self.df)
        victories_by_day = filtered_history['gameCreation'].value_counts()

        days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        victories_by_day = victories_by_day.reindex(days_of_week, fill_value=0)

        total_victories = victories_by_day.sum()

        if total_victories > 0:
            win_rate_by_day = (victories_by_day / total_victories) * 100
        else:
            win_rate_by_day = pd.Series([0]*7, index=days_of_week)

        fig, ax = plt.subplots()

        
        color = "#2B2D42"


        win_rate_by_day.plot(kind='bar', ax=ax, color=color)
        ax.set_title('Tasa de victorias según el día')
        ax.set_ylabel('Porcentaje')
        ax.set_xlabel('Día de la semana')
        ax.grid(True, which='both', axis='both', linestyle='--', color='gray', alpha=0.7)

        plt.xticks(rotation=45, ha='right')
        # plt.tight_layout()
        
        return fig

    def winrate_per_hour_plot(self) -> plt.Figure:
        match_history = MatchHistory(self.df)
        match_history.get_match_hour("gameCreation")
        filtered_history = filter_by_win(self.df)
        victories_by_hour = filtered_history['gameCreation'].value_counts()
        all_hours = pd.Series(0, index=range(24))
        victories_by_hour = all_hours.add(victories_by_hour, fill_value=0)
        total_victories = victories_by_hour.sum()
        if total_victories > 0:
            win_rate_by_hour = round((victories_by_hour / total_victories) * 100)
        else:
            win_rate_by_hour = pd.Series([0]*24, index=range(24))

        fig, ax = plt.subplots()

        color = "#2B2D42"

        win_rate_by_hour.plot(kind='bar', ax=ax, color=color)
        ax.set_title('Tasa de victorias según la hora del día')
        ax.set_xticks([0, 5, 10, 15, 20])
        ax.set_xticklabels([0, 5, 10, 15, 20])
        ax.set_ylabel('Porcentaje')
        ax.set_xlabel('Hora del día')
        ax.grid(True, which='both', axis='both', linestyle='--', color='gray', alpha=0.7)
        
        # plt.tight_layout()

        return fig

