from django.shortcuts import render
from .forms import BusquedaInvocadorForm
from .api_request import StatsApp
import pandas as pd
from .process_data import MatchHistory
# from .visualization_data import CreatePlt
# from matplotlib.backends.backend_agg import FigureCanvasAgg
# from django.http import HttpResponse

def pagina_inicio(request):
    return render(request, 'pagina_inicio.html')

def buscar_invocador(request):
    if request.method == 'POST':
        form = BusquedaInvocadorForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            tag_line = form.cleaned_data['tag_line']
            stats_app = StatsApp()
            
            try:
                puuid = stats_app.get_player_puuid("americas", nombre, tag_line)
                print(f"PUUID obtenido: {puuid}")
                
                matches_list = stats_app.get_matches_list("americas", puuid)
                print(f"Lista de partidas obtenida: {matches_list}")
                
                if not matches_list:
                    raise ValueError("No se encontraron partidas para este invocador.")
                
                summoner_data = stats_app.get_summoner_data("la2", puuid)
                print(f"Datos del invocador: {summoner_data}")
                
                match_data = stats_app.get_every_match_data("americas", matches_list, puuid)
                print(f"Datos de las partidas: {match_data}")
                df = pd.DataFrame.from_dict(match_data, orient="index")
                match_history = MatchHistory(df)
                #all_plots = CreatePlt(match_history)
                #plot = all_plots.winrate_per_hour_plot()
                return render(request, 'resultados.html', {
                    'summoner_data': summoner_data,
                    'match_history': match_history,
                    'nombre': nombre,
                    'tag_line': tag_line
                    #'plot' : plot
                })
            except ValueError as e:
                return render(request, 'resultados.html', {'error': str(e)})
            except KeyError as e:
                return render(request, 'resultados.html', {'error': f'Error de clave: {e}'})
            except Exception as e:
                return render(request, 'resultados.html', {'error': f'Error inesperado: {str(e)}'})
    else:
        form = BusquedaInvocadorForm()
    
    return render(request, 'busqueda.html', {'form': form})

# def plot(request):
#     # AGREGAR LA FUNCION QUE GENERA EL PLOT COMO fig
#     response = HttpResponse(content_type='image/png')
#     canvas = FigureCanvasAgg(fig)
#     canvas.print_png(response)
#     return response