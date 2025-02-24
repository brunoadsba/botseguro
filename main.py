from flask import Flask, render_template_string, jsonify, send_from_directory
import os

app = Flask(__name__)

# Base de dados com EPIs correspondentes, expandida para incluir mais atividades da indústria
epi_equipment = {
    "Soldagem": [
        {"name": "Máscara de Solda", "image": "mascara_de_solda.jpeg", "description": "Protege os olhos e o rosto das faíscas e radiação UV."},
        {"name": "Luvas de Couro", "image": "leather_gloves.jpg", "description": "Proteção contra calor e abrasão."},
        {"name": "Avental de Couro", "image": "leather_apron.jpg", "description": "Protege o corpo contra respingos de metal fundido."},
        {"name": "Botas de Segurança", "image": "safety_boots.jpg", "description": "Proteção contra quedas de objetos pesados e faíscas."}
    ],
    "Pintura": [
        {"name": "Máscara Respiratória", "image": "respiratory_mask.jpg", "description": "Protege contra inalação de vapores tóxicos."},
        {"name": "Óculos de Proteção", "image": "safety_glasses.jpg", "description": "Proteção contra respingos de tinta."},
        {"name": "Macacão Descartável", "image": "disposable_coverall.jpg", "description": "Evita contato direto da pele com a tinta."},
        {"name": "Luvas de Nitrila", "image": "nitrile_gloves.jpg", "description": "Protege as mãos contra produtos químicos."}
    ],
    "Trabalho em Altura": [
        {"name": "Cinto de Segurança", "image": "safety_harness.jpg", "description": "Previne quedas de altura."},
        {"name": "Capacete com Jugular", "image": "safety_helmet.jpg", "description": "Protege a cabeça de impactos e mantém o capacete no lugar em caso de queda."},
        {"name": "Botas Antiderrapantes", "image": "anti_slip_boots.jpg", "description": "Garante aderência em superfícies escorregadias."}
    ],
    "Trabalho com Eletricidade": [
        {"name": "Luvas Isolantes", "image": "insulating_gloves.jpg", "description": "Isola as mãos contra choques elétricos."},
        {"name": "Botas Isolantes", "image": "insulating_boots.jpg", "description": "Protege contra choques elétricos ao pisar em áreas energizadas."},
        {"name": "Capacete com Isolamento Elétrico", "image": "electric_helmet.jpg", "description": "Protege a cabeça com propriedades isolantes."}
    ],
    "Trabalho com Químicos": [
        {"name": "Máscara de Gás", "image": "gas_mask.jpg", "description": "Protege contra vapores e gases tóxicos."},
        {"name": "Viseira Facial", "image": "face_shield.jpg", "description": "Protege o rosto contra respingos de produtos químicos."},
        {"name": "Roupa de Proteção Química", "image": "chemical_protection_suit.jpg", "description": "Barreira contra contato com substâncias perigosas."},
        {"name": "Luvas de PVC", "image": "pvc_gloves.jpg", "description": "Resistente a muitos produtos químicos."}
    ],
    "Operação de Máquinas": [
        {"name": "Protetor Auricular", "image": "ear_protection.jpg", "description": "Reduz o risco de perda auditiva devido ao ruído das máquinas."},
        {"name": "Óculos de Segurança", "image": "safety_glasses.jpg", "description": "Protege os olhos de partículas e fragmentos."},
        {"name": "Capacete", "image": "safety_helmet.jpg", "description": "Proteção contra impactos e quedas de objetos."}
    ]
    # Adicione mais atividades e EPIs conforme necessário
}

# Template HTML para a interface do chatbot com design moderno
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chatbot de EPI</title>
    <style>
        body {
            margin: 0;
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #667eea, #764ba2, #6b8dd6, #8e37d7);
            background-size: 400% 400%;
            animation: gradientBG 15s ease infinite;
            color: white;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            overflow: hidden;
        }

        @keyframes gradientBG {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        h1 {
            font-size: 2.5em;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }

        #activities {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 15px;
            margin-top: 20px;
        }

        .activity {
            background: rgba(255, 255, 255, 0.2);
            border: none;
            color: white;
            padding: 15px 32px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 50px;
            transition: all 0.3s ease;
            backdrop-filter: blur(5px);
        }

        .activity:hover {
            transform: scale(1.05);
            background: rgba(255, 255, 255, 0.3);
        }

        #epi-list {
            margin-top: 20px;
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            width: 90%;
            max-width: 800px;
            display: none;
            backdrop-filter: blur(10px);
        }

        #epi-list h2 {
            font-size: 1.5em;
            margin-bottom: 15px;
        }

        #epi-list ul {
            list-style-type: none;
            padding: 0;
        }

        #epi-list ul li {
            display: flex;
            align-items: center;
            margin: 15px 0;
            background: rgba(255, 255, 255, 0.1);
            padding: 10px;
            border-radius: 10px;
            transition: all 0.3s ease;
        }

        #epi-list ul li:hover {
            transform: translateX(5px);
        }

        #epi-list ul li img {
            width: 50px;
            height: 50px;
            margin-right: 15px;
            border-radius: 10px;
        }

        #epi-list ul li div {
            flex: 1;
        }

        #hide-epis {
            background: #ff416c;
            border: none;
            color: white;
            padding: 10px 20px;
            cursor: pointer;
            border-radius: 50px;
            margin-top: 20px;
            transition: all 0.3s ease;
        }

        #hide-epis:hover {
            background: #ff416c;
            transform: scale(1.05);
        }
    </style>
</head>
<body>
    <h1>Chatbot de EPI</h1>
    <div id="activities">
        {% for activity in activities %}
            <button class="activity" onclick="showEPIs('{{ activity }}')">{{ activity }}</button>
        {% endfor %}
    </div>
    <div id="epi-list">
        <h2 id="activity-title"></h2>
        <ul id="epi-items"></ul>
        <button id="hide-epis" onclick="hideEPIs()">Ocultar EPIs</button>
    </div>

    <script>
        function showEPIs(activity) {
            fetch('/get_epis/' + activity)
                .then(response => response.json())
                .then(data => {
                    document.getElementById('activity-title').innerText = `Para ${activity}, você deve usar os seguintes EPIs:`;
                    let epiList = document.getElementById('epi-items');
                    epiList.innerHTML = '';
                    if (data.epis && data.epis.length > 0) {
                        data.epis.forEach(epi => {
                            let li = document.createElement('li');
                            // Usando encodeURIComponent para garantir que o caminho da imagem seja corretamente codificado
                            li.innerHTML = `<img src="/static/${encodeURIComponent(epi.image)}" alt="${epi.name}"><div><strong>${epi.name}</strong><p>${epi.description}</p></div>`;
                            epiList.appendChild(li);
                        });
                        document.getElementById('epi-list').style.display = 'block';
                    } else {
                        let li = document.createElement('li');
                        li.textContent = "Nenhum EPI encontrado para esta atividade.";
                        epiList.appendChild(li);
                        document.getElementById('epi-list').style.display = 'block';
                    }
                });
        }
        
        function hideEPIs() {
            document.getElementById('epi-list').style.display = 'none';
        }
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    activities = list(epi_equipment.keys())
    return render_template_string(HTML_TEMPLATE, activities=activities)

@app.route("/get_epis/<activity>")
def get_epis(activity):
    if activity in epi_equipment:
        return jsonify({"epis": epi_equipment[activity]})
    else:
        return jsonify({"epis": []})  # Return an empty list if activity not found

@app.route('/static/<path:path>')
def send_static(path):
    print(f"Tentando servir o arquivo: {path}")
    static_folder = os.path.join(os.path.dirname(__file__), 'static')
    return send_from_directory(static_folder, path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)