import pandas as pd
import requests

API_KEY = "ecba2339a28ca95e6a4830fca3b5de46"
BASE_URL = "https://api.themoviedb.org/3"

filmes_lista = []

print("Buscando os 100 filmes mais populares...")

for pagina in range(1, 6):
    url_populares = (
        f"{BASE_URL}/movie/popular?api_key={API_KEY}&language=pt-BR&page={pagina}"
    )
    resposta = requests.get(url_populares)

    if resposta.status_code == 200:
        resultados = resposta.json().get("results", [])

        for filme in resultados:
            filme_id = filme["id"]

            url_detalhes = (
                f"{BASE_URL}/movie/{filme_id}?api_key={API_KEY}&language=pt-BR"
            )
            resp_detalhes = requests.get(url_detalhes)

            if resp_detalhes.status_code == 200:
                detalhes = resp_detalhes.json()

                generos = [g["name"] for g in detalhes.get("genres", [])]

                filmes_lista.append(
                    {
                        "id": detalhes.get("id"),
                        "titulo": detalhes.get("title"),
                        "data_lancamento": detalhes.get("release_date"),
                        "nota_media": detalhes.get("vote_average"),
                        "orcamento": detalhes.get("budget"),
                        "bilheteria": detalhes.get("revenue"),
                        "generos": ", ".join(generos),
                    }
                )
    else:
        print(f"Erro ao acessar página {pagina}: {resposta.status_code}")

df_filmes = pd.DataFrame(filmes_lista)
df_filmes.to_csv("filmes_populares.csv", index=False, encoding="utf-8-sig")

print(
    f"Sucesso! {len(df_filmes)} filmes salvos no arquivo 'filmes_populares.csv'."
)