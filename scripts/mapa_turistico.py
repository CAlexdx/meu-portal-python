# scripts/mapa_turistico.py

def obter_pontos_turisticos():
    """
    Retorna uma lista de pontos turísticos globais com informações detalhadas.
    Cada ponto inclui nome, localização, coordenadas e curiosidades.
    """
    return [
        {
            "nome": "Cristo Redentor",
            "pais": "Brasil",
            "cidade": "Rio de Janeiro",
            "coordenadas": [-22.9519, -43.2105],
            "descricao": "Uma das 7 maravilhas do mundo moderno, com 38 metros de altura.",
            "curiosidade": "Construído entre 1922 e 1931 com pedra-sabão, símbolo da fé brasileira."
        },
        {
            "nome": "Torre Eiffel",
            "pais": "França",
            "cidade": "Paris",
            "coordenadas": [48.8584, 2.2945],
            "descricao": "Monumento icônico de Paris com 324 metros de altura.",
            "curiosidade": "Foi a estrutura mais alta do mundo até 1930 e hoje recebe 7 milhões de visitantes por ano."
        },
        {
            "nome": "Grande Muralha da China",
            "pais": "China",
            "cidade": "Beijing",
            "coordenadas": [40.4319, 116.5704],
            "descricao": "Fortificação com mais de 21 mil km, construída há mais de 2 mil anos.",
            "curiosidade": "É uma das únicas estruturas humanas visíveis do espaço a olho nu."
        },
        {
            "nome": "Pirâmides de Gizé",
            "pais": "Egito",
            "cidade": "Gizé",
            "coordenadas": [29.9792, 31.1342],
            "descricao": "Tumbas faraônicas construídas há mais de 4.500 anos.",
            "curiosidade": "A Grande Pirâmide era originalmente coberta por calcário polido, refletindo o sol do deserto."
        },
        {
            "nome": "Estátua da Liberdade",
            "pais": "Estados Unidos",
            "cidade": "Nova York",
            "coordenadas": [40.6892, -74.0445],
            "descricao": "Presente da França aos EUA, símbolo da liberdade e da democracia.",
            "curiosidade": "Seu esqueleto interno foi projetado por Gustave Eiffel, o mesmo da Torre Eiffel."
        },
        {
            "nome": "Taj Mahal",
            "pais": "Índia",
            "cidade": "Agra",
            "coordenadas": [27.1751, 78.0421],
            "descricao": "Mausoléu de mármore branco, construído por amor pelo imperador Shah Jahan.",
            "curiosidade": "Demorou mais de 20 anos para ser construído, com mais de 20 mil trabalhadores."
        },
        {
            "nome": "Machu Picchu",
            "pais": "Peru",
            "cidade": "Cusco",
            "coordenadas": [-13.1631, -72.5450],
            "descricao": "Cidade inca nas montanhas dos Andes, redescoberta em 1911.",
            "curiosidade": "Seu verdadeiro propósito ainda é debatido entre os historiadores."
        },
        {
            "nome": "Cataratas do Iguaçu",
            "pais": "Brasil/Argentina",
            "cidade": "Foz do Iguaçu",
            "coordenadas": [-25.6953, -54.4367],
            "descricao": "Conjunto de 275 quedas d’água no rio Iguaçu, entre Brasil e Argentina.",
            "curiosidade": "O som das quedas pode ser ouvido a mais de 20 km de distância."
        }
    ]
