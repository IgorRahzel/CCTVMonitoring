import os

class stats:
    def __init__(self, peopleDict, areasDict, filename):
        self.peopleDict = peopleDict
        self.areasDict = areasDict
        self.filename = filename

        # Garante que os diretórios existem
        os.makedirs(os.path.join(self.filename, "areasStats"), exist_ok=True)
        os.makedirs(os.path.join(self.filename, "peopleStats"), exist_ok=True)

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
                f.write("=" * 40 + "\n")
