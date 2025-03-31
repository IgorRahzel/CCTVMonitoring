# CCTVMonitoring

Este projeto tem como objeto obter dados/informações sobre uma região monitorada por uma CCTV como por exemplo:
- Detecção das pessoas no vídeo
- Geração de mapa de calor com base nas regiões com maior fluxo de pessoas
- Geração de diagrama de espaguete
- Geração de diagarama de fluxo
- Número de pessoas em cada uma das áreas segmentadas no momento atual
- Número total de pessoas detectadas em cada área segmentada
- Ids/pessoas em cada uma das áreas
- Ids/pessoas que estiveram na área
- Histórico das áreas acessadas por cada pessoa
- Tempo de permanência em cada uma das áreas

![Demo of the project](./readme_data/output.gif)

# 📌 Tabela de Conteúdos
- [Como Executar](#como-executar)
- [Funcionamento do Código](#funcionamento-do-codigo)
  - [Classes Auxiliares](#classes-auxiliares)
    - [person](#1-person)
    - [area](#2-area)
    - [heatMap](#3-heatmap)
    - [stats](#4-stats)
  - [Classe videoAnalyzer](#classe-videoanalyzer)
  - [Arquivo Principal](#arquivo-principal)
- [Resultados](#resultados)

# Estrutura do Projeto
```bash
.
├── backend               # Pasta contendo os arquivos utilizados no backend
│   ├── models            # Pasta com os modelos da YOLOv8
│   │   ├── best.pt       # Pesos do modelo pré-treinado
│   ├── requirements.txt  # Bibliotecas utiilizadas
│   ├── src               # Pasta com os arquivos .py
│   │   ├── area.py       
│   │   ├── heatMap.py
│   │   ├── main.py
│   │   ├── person.py
│   │   ├── spaghetti.py
│   │   ├── stats.py
│   │   ├── trajectoryGraph.py
│   │   ├── utils.py
│   │   └── videoAnalyzer.py
│   ├── stats                  # Pasta para aramezenar as estátisticas geradas
│   │   ├── areasCSV           # Estatísticas para área com extensão .csv
│   │   ├── areasStats         # Estatísticas para área com extensão .txt
│   │   ├── peopleCSV          # Pasta contendo os arquivos de cada uma das pessoas identificadas com arquivos de extensão .csv
│   │   ├── peopleStats        # Pasta contendo os arquivos de cada uma das pessoas identificadas com arquivos de extensão .txt
│   └── videos                 # Pasta com os vídeos utilizados para inferência
│       ├── superMarket.mp4
├── frontend # Pasta contendo os arquivos utilizados no frontend
│   ├── FronEnd
│   │   ├── src
│   │   │   ├── App.vue                # Arquivo responsável por gerar a interface
│   │   │   ├── assets               
│   │   │   ├── components             # Componentes do projeto
│   │   │   │   ├── AreaStats.vue
│   │   │   │   ├── CameraView.vue
│   │   │   │   ├── FlowDiagram.vue
│   │   │   │   ├── HeatMap.vue
│   │   │   │   ├── icons
│   │   │   │   ├── PeopleStats.vue
│   │   │   │   ├── PersonDetails.vue
│   │   │   │   └── Spaghetti.vue
│   │   │   ├── router
│   │   │   │   └── index.ts
│   │   │   └── views
│   │   │       └── HomeView.vue    # Página incial da interface
│   │   ├── (Outros arquivos gerados automaticamente pelo Vue)
│   │  
├── readme_data
└── README.md

```

# Como Executar

1. **Instalar as dependências:**
   Inicialmente certifique-se de que as dependências necessárias foram instaladas, isso pode ser feito executando o seguinte comando:

   ```bash
   pip install -r requirements.txt
   ```
2. **Navegue até a pasta do projeto:**
     A partir da pasta do projeto execute o comando:
     ```bash
     python main.py
     ```
3. **Saída:**
   - O vídeo contendo a inferência e o mapa de calor será exibido em uma janela
   - Os arquivos contendo as estatísticas serão gerados na pasta *stats*
   


# Funcionamento do código
Conforme pode ser observado na seção [Estrutura do Código](estrutura-do-codigo) esse projeto é divídido em duas pastas principais sendo elas `backend` e `frontend`. 

Na seção `backend` será apresentada a ideia geral do funcionamento do código bem como o papel de cada um de seus componentes. Inicialmente trataremos das classes auxiliares como `person`,`area`,`heatMap`,`spaghetti`,`trajectoryGraph`,`stats` então iremos tratar da classe principal, `videoAnalyzer` para conectar todos os componentes, além de realizar a geração das estatísticas e a inferência no vídeo. Por fim mostraremos o fluxo do arquivo principal `main.py`.

já na seção `frontend` será mostrado a ideia por trás de cada um dos componentes: `AreaStats`, `CameraView`, `FlowDiagram`, `HeatMap`, `PeopleStats`, `PersonDetails`,`Spaghetti`

## backend
### Classes Auxiliares
**1. person**: A classe `person` é utilizada para armazenar os dados referentes à pessoas identificadas no vídeo, esta tem como atributos:

- `id` ➡️ Número de identificação da pessoa detectada
- `positionHistory` ➡️ É um *deque(Double ended queue)* utilizada para aramazenar as últimas *n* posições da pessoa, onde *n* é escolhido pelo usuário
- `visitedAreas` ➡️ É uma lista que contém a sequência de áreas visitada pelo usuário, a lista é atualizada apenas caso o úsuario mude da área atual para outra
- currentArea ➡️ Determina o nome da área atual do usuário
- `BBox` ➡️ Coordenadas da bounding box da pessoa no frame atual
- `BBoxColor` ➡️ Cor da bounding box, está é utilizada para melhorar a visualização da área em que a pessoa se encontra
- `framesSpentInArea` ➡️ Dicionário que tem como chave os nomes das áreas e o valor obtido ao acessar as chaves é o tempo(número de frames) que a pessoa permaneceu na área
- `lastFrameDetected` ➡️ Último frame em que a pessoa foi detectada

já os métodos dessa classe são os seguintes:

- `_initFramesSpentInArea(self,areasDict)`  ➡️ Utilizado para construir o dicionário `framesSpentInArea` a partir de um dicionário contendo as áreas
- `dist2centroid(self,centroid)` ➡️ Calcula a distância entre a última posição que a pessoa foi detectada e um centroide detectado no frame atual
- `updatePosition(self,bbox,centroid)` ➡️ Atualiza o BBox da pessoa e posição atual

**2. area**: A classe `area` armazenda dados de cada uma das areas segmentadas. Os atributos dessa classe são:

- `name`  ➡️ Armazena o nome da área
- `color`  ➡️ Armazena a cor relacionada a área
- `vertices`  ➡️ Armazena os vértices que delimitam a área
- `IdsRecordInArea`  ➡️ Armazena os Ids das pessoas que acessaram a área
- `currentIdsInArea`  ➡️ Armazena os Ids das pessoas que se encontram na área atualmente
- `currentNumberOfPeople`  ➡️ Armazena o número de pessoas na área atualmente
- `totalNumberOfPeople`  ➡️ Armazena o número total de pessoas que acessou a área

Essa classe possui apenas um método sendo ele o `isInside`, o qual verifica se o centroide de uma pessoa está dentro da área.

**3. heatMap**: A classe `heatMap` tem como objetivo gerar o mapa de calor do vídeo. Essa classe tem os seguintes atributos:

- `height` ➡️ Altura do vídeo
- `width` ➡️ Largura do vídeo
- `decay` ➡️ Taxa de decaimento do mapa de calor, utilizado para suavizar o mapa ao longo do tempo
- `detectionMatrix` ➡️ Matrix que armazena as regiões onde ocorreram as detecções

Abaixo estão listado os métodos dessa classe e suas funcionalidades:

- `applyDecay(self)` ➡️ Aplica o decaímento na matriz
- `updateDetectionMatrix(self, bbox)` ➡️ Adiciona o valor 1 na matriz `detectionMatrix` nas regiões relativas aos pixels onde foram inferidas as bounding boxes no frame atual
- `getNormalizedDetectionMatrix(self)` ➡️ retorna a matriz `detectionMatrix` normalizada
- `getColoredHeatMap(self)` ➡️  Aplica um mapa de cores na matriz normalizada de modo a produzir o mapa de calor
- `overlayHeatMap(self, frame)` ➡️  Sobrepõe o heatmap ao frame

**4. spaghetti**: A classe `spaghetti` é utilizada para criar o diagrama de espaguete das pessoas detectadas no vídeo, tendo como atributos:

- `frame_shape` ➡️ Tupla com o shape do frame do vídeo em análise.
- `trajectory_points`  ➡️ Dicionário que aramazena o histórico dos centroídes das pessoas detectadas

A classe tem como métodos `update(self,person,areas_dict)` e `drawSpaghetti(self,frame)` os quais atualizam o dicionário e desenham o diagrame de espaguete no frame respectivamente.

**5. trajectoryGraph**: Essa classe é responsável por crirar um grafo de trajetórias, para isso são criados nós no centro de cada uma das áreas de interesse definidas pelo usuário e então quando houver uma transição de uma pessoa de uma área para outra é criada uma aresta direcionada indicando essa transição, conforme o número de transições aumente a espessura da aresta também irá aumentar. Permitindo assim uma melhor comprensão dos fluxos mais comuns. Essa classe tem como atributos:

- `areasList` ➡️ Lista de objetos da classe area
- `height` e `width` ➡️ Dimensões do frame do vídeo
- `centroids` ➡️ Centroides das áreas
- `areaToNumber`,`numberToArea`  ➡️ Mapeamento das áreas para um indice e vice-versa
- `incidenceMatrix` ➡️ Matriz de dimensões |Áreas|x|Áreas| onde a entrada *(i,j)* contabiliza as transições ocorridas da área *i* para a área *j*

Os métodos dessa classe são:

- `getAreasCentroid(self)` ➡️ Utilizada para obter o centroids do atrivuto `centroids`
- `buildMApping(self)` ➡️ Cria o mapeamento das áreas para os índices e vice-versa
- `drawGraph(self,frame)` ➡️ Desenha o diagrama de fluxo no frame

**6. stats**: A classe `stats` é responsável por gerar as estatíscas e escreve-las em arquivos de saída, tendo como atributos:

- `peopleDict` ➡️ Dicionário da classe `person`
- `areasDict` ➡️ Dicionário da classe `area`
- `filename` ➡️ nome da pasta onde serão armazenados os arquivos gerados

Os métodos da classe são `updateAreasStats(self)` e `updatePeopleStats(self)` utilizados para imprimir as informções das áreas e das pessoas.


### Classe videoAnalyzer
Como mencionado anteriormente a classe `videoAnalyzer` tem como papel unificar todas as classes implementadas anteriormente. Os atributos dessa classe são:

- `id` ➡️ Inicializado como zero e é imcrementado em um a cada pessoa nova que é identificada
- `areasDict` ➡️  Dicionário contendo as áreas
- `people` ➡️  Dicionário contendo as pessoas identificadas
- `heatmap` ➡️  Mapa de calor
- `statistics` ➡️  Instância da classe `stats`

Os métodos dessa classe são os seguintes:

- `_buildAreasDict(self,areasList)` ➡️ Constroí o dicionário de áreas a partir de uma lista contendo as áreas
- `getData(self,results)` ➡️ retorna uma lista contendo tuplas de centroides e bounding boxes extráidos de *results*, que dados retornados pela YOLOv8 ao realizar inferência em um frame do vídeo.
- `removeLostPeople(self,frameNumber)` ➡️ Remove pessoa do dicionário `people` caso essa não seja detectada por mais de 10 frames
- `updatePeopleDict(self,results,frameNumber,threshold = 20)` ➡️ Verifica se algum dos centroides do frame atual está próximo do último centroide de uma pessoa do dicionário `people` se isso ocorre, atualiza as informações da pessoa, caso não ocorra uma nova pessoa é adicionada ao diconário
- `updatePersonArea(self)` ➡️  Atualiza a área em que cada uma das pessoas se encontram
- `updateAreas(self)` ➡️ Atualiza os atributos das áreas em `areasDict`
- `drawAreas(self, frame)` ➡️ Desenha as áreas no frame do vídeo
- `drawBoundingBoxes(self,frame)` ➡️ Desenha as Bounding boxes das pessoas identificadas no frame do vídeo
- `buildHeatMap(self,frame)` ➡️ Atualiza o mapa de calor
- `processVideo(self,results,frameNumber,frame)` ➡️ Une os métodos da classe de modo a produzir os resultados durante o processamento do vídeo

### Arquivo principal
No arquivo `main.py` foi importado o modelo YOLOv8 da biblioteca *ultralytics*, nele é feito a segmentação das áreas de interesse do vídeo, bem como a criação de uma lista dessas áreas. É então feito processamento dos frames do vídeos onde a YOLOv8 é utilizada para obter os dados desejados, os quais são armazendos em *results*, em seguida é feito o processamento desses dados utilizadno o método *videoProcess()* da classe `videoAnalyzer`.

### Resultados
O vídeo contendo os resultados pode ser visto no link abaixo:
[link do vídeo](https://drive.google.com/file/d/1Xbkc8S1sPyf-ka_vGlVEXOWuZwVTyzXI/view?usp=sharing)

## frontend

### AreaStats.vue

Esse arquivo gera uma tabela com as seguintes colunas: *Áreas*,*Total de Pessoas*, *Pessoa na área* , *Com cesto*, *Com Carrinho*, o que permite identificar o número de pessoas em cada uma das áreas bem como as ações realizada em cada uma das áreas, onde *Pessoa* representa o tempo total em que as pessoas não estiveram com o carrinho ou com o cesto ná área, já *Com Cesto* e *Com Carrinho* representam o tempo total onde as pessoas foram identificadas carregando um cesto ou carrinho. Também são gerados os gráficos de barras de *Ações por Área* e *Tempo total por Ação*


### PeopleStats.vue

Esse componente mostra os ids das pessoas identificadas, ao selecionar algum dos ids é possível visualizar as estátiscas relacionadas àquela pessoa

### PersonDetails.vue

Gera as estatísticas para o id selecionado em `PeopleStats.vue`. Nele são mostrados um tabela com as colunas: *Área*, *Pessoa na área* , *Com cesto*, *Com Carrinho além dos gráficos de barras: *Ações Por Área*,*Tempo total por ação* e *Tempo total por área*

### HeatMap.vue

Mostra o mapa de calor da movimentação das pessoas

### Spaghetti.vue

Mostra o diagrana de espaguete

### FlowDiagram.vue

Mostra o diagrama de fluxo

### CameraView.vue

Mostra apenas o vídeo




