from flask import Flask, request, jsonify, send_file
from ..data import StatsApp, CreatePlt
import pandas as pd
import io
import os

app = Flask(__name__)

@app.route('/api/search')
def search():
    query = request.args.get('query')
    print(f"Recibida consulta: {query}")

    if not query or '#' not in query:
        print("Consulta inválida.")
        return jsonify({"error": "Query inválida. Asegúrate de usar el formato 'game_name#tag_line'."}), 400

    try:
        game_name, tag_line = query.split('#')
        print(f"Game Name: {game_name}, Tag Line: {tag_line}")

        api_request_app = StatsApp()
        region = "americas"
        puuid = api_request_app.get_player_puuid(region, game_name, tag_line)
        print(f"PUUID: {puuid}")

        matches_list = api_request_app.get_matches_list(region, puuid)
        print(f"Matches List: {matches_list}")

        dictionary = api_request_app.get_every_match_data(region, matches_list, puuid)
        df = pd.DataFrame.from_dict(dictionary, orient="index")
        print(f"DataFrame creado con {df.shape[0]} filas.")

        # Crear los gráficos
        plot_creator = CreatePlt(df)
        fig = plot_creator.winrate_per_hour_plot()
        print("Gráfico generado.")

        # Guardar el gráfico en un buffer de bytes
        img = io.BytesIO()
        fig.savefig(img, format='png')
        img.seek(0)

        # Guardar temporalmente la imagen en un archivo
        img_path = 'static/plot.png'
        with open(img_path, 'wb') as f:
            f.write(img.getbuffer())
        print(f"Imagen guardada en {img_path}.")

        # Enviar la URL del gráfico
        response = {"imageUrl": f"/static/plot.png"}
        print(f"Respuesta JSON: {response}")  # Mensaje de depuración

        return jsonify(response)

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
