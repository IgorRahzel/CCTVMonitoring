import os
import csv
import matplotlib.pyplot as plt


class stats:
    def __init__(self, peopleDict, areasDict, filename,frameNumber=0):
        self.peopleDict = peopleDict
        self.areasDict = areasDict
        self.filename = filename
        self.frameNumber = frameNumber

        # Garante que os diretórios existem
        os.makedirs(os.path.join(self.filename, "areasStats"), exist_ok=True)
        os.makedirs(os.path.join(self.filename, "peopleStats"), exist_ok=True)
        os.makedirs(os.path.join(self.filename, "reportImgs"), exist_ok=True)

    def updateAreasStats(self):
        areasDir = os.path.join(self.filename, "areasStats")
        for area in self.areasDict.values():
            areaFile = os.path.join(areasDir, f"{area.name}.txt")  # Arquivo único por área
            with open(areaFile, 'w') as f:
                f.write(f"Área: {area.name}\n")
                f.write(f"  - Total de pessoas detectadas: {area.totalNumberOfPeople}\n")
                f.write(f"  - Número atual de pessoas: {area.currentNumberOfPeople}\n")
                f.write(f"  - IDs que já estiveram na área: {list(area.IdsRecordInArea)}\n")
                f.write(f"  - IDs atualmente na área: {area.currentIdsInArea}\n")
                f.write("=" * 40 + "\n")

    def updatePeopleStats(self):
        peopleDir = os.path.join(self.filename, "peopleStats")
        for person in self.peopleDict.values():
            personFile = os.path.join(peopleDir, f"person_{person.id}.txt")  # Arquivo único por pessoa
            with open(personFile, 'w') as f:
                f.write(f"Pessoa ID: {person.id}\n")
                f.write(f"  - Último frame detectado: {person.lastFrameDetected}\n")
                f.write(f"  - Área atual: {person.currentArea}\n")
                f.write(f"  - Áreas visitadas: {list(person.visitedAreas)}\n")
                for areaName, frames in person.framesSpentinArea.items():
                    f.write(f"  - Tempo na área '{areaName}': {frames} frames\n")
                for action, count in person.actionCounter.items():
                    f.write(f"  - Ação '{action}': {count} frames\n")
                f.write("=" * 40 + "\n")

        
    def createAreasCSV(self):
        '''
        Create a CSV file with the areas statistics such as:
        - Average number of people in the area
        - Total number of people in the area
        - Total time that each action was performed in the area
        - History of people in the area
        '''

        # Create CSV file
        csv_dir = os.path.join(self.filename, "areasCSV")
        os.makedirs(csv_dir, exist_ok=True)  # Criar apenas os diretórios
        csvFile = os.path.join(csv_dir, "areasStats.csv")  # Definir o caminho do arquivo CSV

        header = ['Àreas','Número Total de Pessoas']
        for person in self.peopleDict.values():
            for action_name in person.actionCounter.keys():
                #print(f'Action: {action}')
                header.append('Time' + action_name)
            break

        with open(csvFile, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(header)

            for area in self.areasDict.values():
                row = [area.name, area.totalNumberOfPeople]
                for action in area.actionCounter.values():
                    row.append(action)
                writer.writerow(row)



    def createPersonCSV(self):
        '''
        Cria um arquivo CSV para cada pessoa no dicionário peopleDict.
        O arquivo CSV contém:
        - Uma linha para cada área.
        - Colunas para o tempo total gasto em cada ação na área.
        '''
        csv_dir = os.path.join(self.filename, "peopleCSV")
        os.makedirs(csv_dir, exist_ok=True)  # Garante que o diretório existe

        # Itera sobre cada pessoa no dicionário
        for person in self.peopleDict.values():
            csvFile = os.path.join(csv_dir, f"person_{person.id}.csv")  # Nome do arquivo CSV

            with open(csvFile, 'w', newline='') as f:
                writer = csv.writer(f)

                # Cria o cabeçalho do CSV
                header = ['Área']  # Primeira coluna é o nome da área
                for action in person.numberToAction.values():  # Adiciona uma coluna para cada ação
                    header.append(action)
                writer.writerow(header)  # Escreve o cabeçalho

                # Itera sobre cada área usando o mapeamento numberToArea
                for area_number, area_name in person.numberToArea.items():
                    row = [area_name]  # Nome da área

                    # Itera sobre cada ação usando o mapeamento numberToAction
                    for action_number in person.numberToAction.keys():
                        # Obtém o tempo gasto na ação na área atual
                        action_time = person.actionsPerAreaMatrix[area_number][action_number]
                        row.append(action_time)  # Adiciona o tempo à linha

                    writer.writerow(row)  # Escreve a linha no CSV