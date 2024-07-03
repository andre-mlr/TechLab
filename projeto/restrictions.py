class Restrictions:
    @staticmethod
    def apply_restrictions(response):
        restricted_phrases = ["outras empresas", "informações pessoais"]
        for phrase in restricted_phrases:
            if phrase in response:
                return "Desculpe, não posso fornecer essa informação."
        if any(word in response for word in ["ódio", "violência"]):
            return "Desculpe, não posso responder a isso."
        return response

restrictions = Restrictions()
