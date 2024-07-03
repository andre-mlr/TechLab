import json

class KnowledgeBase:
    def __init__(self, json_file):
        with open(json_file, 'r', encoding='utf-8') as file:
            self.data = json.load(file)

    def search(self, query):
        results = []
        query_lower = query.lower()
        for item in self.data:
            if query_lower in item['content'].lower():
                results.append(item['content'])
        return results if results else ["Nenhuma informação relevante encontrada na base de conhecimento."]

# Inicialize com o caminho para seu arquivo JSON
knowledge_base = KnowledgeBase('knowledge_base.json')
