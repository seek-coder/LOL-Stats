from django.shortcuts import render
from .forms import BusquedaInvocadorForm
from .api_request import StatsApp

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
                
                match_id = matches_list[0]
                
                summoner_data = stats_app.get_summoner_data("la2", puuid)
                print(f"Datos del invocador: {summoner_data}")
                
                match_data = stats_app.get_match_data("americas", match_id, puuid)
                print(f"Datos de la partida: {match_data}")
                
                return render(request, 'resultados.html', {
                    'summoner_data': summoner_data,
                    'match_data': match_data
                })
            except ValueError as e:
                return render(request, 'resultados.html', {'error': str(e)})
            except KeyError as e:
                # Imprimir la excepción KeyError
                return render(request, 'resultados.html', {'error': f'Error de clave: {e}'})
            except Exception as e:
                return render(request, 'resultados.html', {'error': f'Error inesperado: {str(e)}'})
    else:
        form = BusquedaInvocadorForm()
    
    return render(request, 'busqueda.html', {'form': form})
