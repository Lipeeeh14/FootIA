from openai import OpenAI
from flask import Flask, jsonify, request
import json

client = OpenAI()

def geraSimulacaoPartida():
  times = request.get_json()

  prompt_sistema = """
  Você é um simulador de partidas de futebol de um campeonato de pontos corridos.
  Simule uma partida entre os dois times que o usuário informar. 
  Você deve apresentar o resultado do jogo no seguinte formato:
  nome do mandante: gols,
  nome do visitante: gols
  """

  resposta = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {
        "role": "system", 
        "content": prompt_sistema
      },
      {
        "role": "user", 
        "content": f"{times['timeMandante']} contra {times['timeVisitante']}"
      }
    ]
  )

  result = resposta.choices[0].message.content

  return {
    "resultado": result,
    "golsTimeMandante": int(result.split(',')[0][-1]),
    "golsTimeVisitante": int(result.split(',')[1][-1])
  }

app = Flask(__name__)

@app.route('/partida/simular', methods=['POST'])
def simularPartida():
  return jsonify(geraSimulacaoPartida())

app.run(port=5000, host='localhost', debug=True)