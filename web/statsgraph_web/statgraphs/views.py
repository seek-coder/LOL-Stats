import pandas as pd
import io

from django.shortcuts import render
from .forms import BusquedaInvocadorForm
from .api_request import StatsApp
from .process_data import MatchHistory
from .visualization_data import CreatePlt
from django.http import HttpResponse

def pagina_inicio(request):
    return render(request, 'buscar_invocador.html')

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

                request.session['match_data'] = df.to_json()

                return render(request, 'resultados.html', {
                    'summoner_data': summoner_data,
                    'match_history': match_history,
                    'nombre': nombre,
                    'tag_line': tag_line,
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

def plot1(request):
    match_data_json = request.session.get('match_data', None)
    if match_data_json:
        df = pd.read_json(match_data_json)
        plot_creator = CreatePlt(df)
        try:
            fig = plot_creator.winrate_per_day_plot()
            
            buf = io.BytesIO()
            fig.savefig(buf, format='png', bbox_inches='tight')

            buf.seek(0)
            
            response = HttpResponse(buf, content_type='image/png')
            response['Content-Disposition'] = 'inline; filename="plot1.png"'
            return response
        except Exception as e:
            print(f"Error generating plot: {e}")
            return HttpResponse("Failed to generate image.", status=500)
    else:
        return HttpResponse("No match data available.", status=404)
    
def plot2(request):
    match_data_json = request.session.get('match_data', None)
    if match_data_json:
        df = pd.read_json(match_data_json)
        plot_creator = CreatePlt(df)   
        try:
            fig = plot_creator.winrate_per_hour_plot()
            
            buf = io.BytesIO()
            fig.savefig(buf, format='png', bbox_inches='tight')
            buf.seek(0)
            
            response = HttpResponse(buf, content_type='image/png')
            response['Content-Disposition'] = 'inline; filename="plot2.png"'
            return response
        except Exception as e:
            print(f"Error generating plot: {e}")
            return HttpResponse("Failed to generate image.", status=500)
    else:
        return HttpResponse("No match data available.", status=404)
    
def sobre_nosotros(request):
    return render(request, 'sobre_nosotros.html')