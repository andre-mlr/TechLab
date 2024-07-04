import json

class KnowledgeBase:
    def __init__(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            self.knowledge_data = json.load(f)

    def search(self, query):
        results = []

        # Procurar nos círculos
        for circle in self.knowledge_data.get('circulos', []):
            if query.lower() in circle['nome'].lower():
                results.append(circle['descricao'])
                results.extend(circle['responsabilidades'])
            for subcircle in circle.get('subcirculos', []):
                if query.lower() in subcircle['nome'].lower():
                    results.append(subcircle['descricao'])
                    results.extend(subcircle['responsabilidades'])

        # Procurar nos programas
        for program in self.knowledge_data.get('programas', []):
            if query.lower() in program['nome'].lower():
                results.append(program['descricao'])

        # Procurar nas virtudes
        for category, virtues in self.knowledge_data.get('virtudes', {}).items():
            for virtue in virtues:
                if query.lower() in virtue.lower():
                    results.append(virtue)

        return results

# Exemplo de utilização
knowledge_base = KnowledgeBase('knowledge_base.json')