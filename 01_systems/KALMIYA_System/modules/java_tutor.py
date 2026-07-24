import random
import re

class JavaTutor:
    def __init__(self):
        self.topics = ["Sintaxis Básica", "POO", "Estructuras de Datos", "Manejo de Excepciones", "Streams y Lambdas"]
        
        self.theory_questions = {
            "Sintaxis Básica": [
                {"q": "¿Cuál es la diferencia entre 'int' e 'Integer' en Java?", 
                 "a": "int es un tipo primitivo, mientras que Integer es una clase envoltorio (wrapper)."},
                {"q": "¿Para qué sirve la palabra reservada 'final' en una variable?",
                 "a": "Hace que el valor de la variable no pueda ser modificado (constante)."}
            ],
            "POO": [
                {"q": "¿Qué es el polimorfismo en Java?",
                 "a": "Es la capacidad de un objeto de tomar muchas formas. Comúnmente ocurre cuando una clase padre referencia a una instancia de una clase hija."},
                {"q": "¿Cuál es la diferencia entre una clase abstracta y una interfaz?",
                 "a": "Una interfaz solo puede tener métodos abstractos (hasta Java 8) y constantes, y una clase puede implementar múltiples interfaces. Una clase abstracta puede tener métodos con implementación y estado, pero no soporta herencia múltiple."}
            ]
        }
        
        self.practical_exercises = {
            "Sintaxis Básica": {
                "desc": "Escribe una función en Java llamada 'sumar' que reciba dos enteros y devuelva su suma.",
                "solution_keywords": ["int", "sumar", "return", "+"]
            },
            "POO": {
                "desc": "Define una clase 'Perro' que herede de una clase 'Animal' y sobrescriba el método 'hacerSonido()'.",
                "solution_keywords": ["class Perro", "extends Animal", "@Override", "void hacerSonido"]
            }
        }
        self.current_exercise = None

    def get_topics(self):
        """Devuelve los temas disponibles para estudiar."""
        return self.topics

    def get_theory_question(self, topic=None):
        """Devuelve una pregunta teórica aleatoria."""
        if not topic or topic not in self.theory_questions:
            topic = random.choice(list(self.theory_questions.keys()))
        
        question = random.choice(self.theory_questions[topic])
        return {"topic": topic, "question": question["q"], "answer": question["a"]}

    def get_practical_exercise(self, topic=None):
        """Devuelve un ejercicio práctico."""
        if not topic or topic not in self.practical_exercises:
            topic = random.choice(list(self.practical_exercises.keys()))
            
        self.current_exercise = self.practical_exercises[topic]
        return {"topic": topic, "exercise": self.current_exercise["desc"]}

    def evaluate_code(self, code_snippet):
        """Evalúa un fragmento de código Java ingresado por el usuario de forma rudimentaria."""
        if not self.current_exercise:
            return {"status": "error", "message": "No hay un ejercicio práctico activo."}
        
        code_snippet = code_snippet.lower()
        missing_keywords = []
        for kw in self.current_exercise["solution_keywords"]:
            if kw.lower() not in code_snippet:
                missing_keywords.append(kw)
                
        if not missing_keywords:
            self.current_exercise = None
            return {"status": "success", "message": "¡Excelente! Tu código contiene todos los elementos clave del patrón esperado.", "score": 100}
        else:
            return {
                "status": "partial", 
                "message": f"Tu código compilaría, pero parece que te faltan algunos conceptos clave. Intenta incluir: {', '.join(missing_keywords)}",
                "score": max(0, 100 - (len(missing_keywords) * 20))
            }

    def explain_concept(self, concept):
        """Función proxy para que el cerebro de KALMIYA explique un concepto a detalle."""
        return f"KALMIYA consultará sobre '{concept}' en Java a través del cerebro LLM."
