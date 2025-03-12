import os

class stats:
    def __init__(self, peopleDict, areasDict, filename):
        self.peopleDict = peopleDict
        self.areasDict = areasDict
        self.filename = filename

        # Garante que o diretório para os arquivos existe
        os.makedirs(self.filename, exist_ok=True)

    def updateAreasStats(self):
        areasFile = os.path.join(self.filename, 'areasStats')
        os.makedirs(areasFile, exist_ok=True)
        for area in self.areasDict.values():
            areasFile = os.path.join(self.filename, f'{area.name}_stats.txt')
            with open(areasFile, 'w') as f:
                f.write(f"Área: {area.name}\n")
                f.write(f"  - Total de pessoas detectadas: {area.totalNumberOfPeople}\n")
                f.write(f"  - Número atual de pessoas: {area.currentNumberOfPeople}\n")
                f.write(f"  - IDs que já estiveram na área: {list(area.IdsRecordInArea)}\n")
                f.write(f"  - IDs atualmente na área: {area.currentIdsInArea}\n")
                f.write("=" * 40 + "\n")  # Linha separadora
         

    def updatePeopleStats(self):
        peopleFile = os.path.join(self.filename, 'peopleStats')
        os.makedirs(peopleFile, exist_ok=True)
        for person in self.peopleDict.values():
            peopleFile = os.path.join(self.filename, f'person_{person.id}_stats.txt')
            with open(peopleFile, 'w') as f:
                f.write(f"Pessoa ID: {person.id}\n")
                f.write(f"  - Último frame detectado: {person.lastFrameDetected}\n")
                f.write(f"  - Área atual: {person.currentArea}\n")
                f.write(f"  - Áreas visitadas: {list(person.visitedAreas)}\n")
                for areaName, frames in person.framesSpentinArea.items():
                    f.write(f"  - Tempo na área '{areaName}': {frames} frames\n")
                f.write("=" * 40 + "\n")  # Linha separadora