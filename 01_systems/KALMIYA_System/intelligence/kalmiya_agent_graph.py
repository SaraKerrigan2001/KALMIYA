from typing import TypedDict, Annotated, Sequence, cast
import operator
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    current_agent: str
    next_step: str

def route_message(state: AgentState) -> str:
    """Decide qué sub-agente debe manejar el mensaje."""
    last_msg = str(state['messages'][-1].content).lower()
    
    if "investiga" in last_msg or "busca" in last_msg:
        return "investigator_agent"
    elif "código" in last_msg or "programa" in last_msg:
        return "coder_agent"
    else:
        return "main_assistant"

def investigator_agent(state: AgentState):
    print("[AgentGraph] Activando Agente Investigador...")
    response = AIMessage(content="[Investigador] He buscado en mi bóveda y encontré la información relevante.")
    return {"messages": [response], "current_agent": "investigator_agent"}

def coder_agent(state: AgentState):
    print("[AgentGraph] Activando Agente Programador...")
    response = AIMessage(content="[Programador] Escribiendo el código solicitado...")
    return {"messages": [response], "current_agent": "coder_agent"}

def main_assistant(state: AgentState):
    print("[AgentGraph] Activando Asistente Principal...")
    try:
        from intelligence.brain_v4 import ask_kalmiya
        user_msg = str(state['messages'][-1].content)
        reply = ask_kalmiya(user_msg)
    except Exception as e:
        reply = f"[KALMIYA] ¿En qué más puedo ayudarte hoy? (Modo Offline)"
    response = AIMessage(content=reply)
    return {"messages": [response], "current_agent": "main_assistant"}

# Construir el grafo de LangGraph
workflow = StateGraph(AgentState)

# Añadir nodos
workflow.add_node("investigator_agent", investigator_agent)
workflow.add_node("coder_agent", coder_agent)
workflow.add_node("main_assistant", main_assistant)

# Añadir enrutador condicional desde el inicio
workflow.set_conditional_entry_point(
    route_message,
    {
        "investigator_agent": "investigator_agent",
        "coder_agent": "coder_agent",
        "main_assistant": "main_assistant"
    }
)

# Todos terminan
workflow.add_edge("investigator_agent", END)
workflow.add_edge("coder_agent", END)
workflow.add_edge("main_assistant", END)

# Compilar
kalmiya_brain_graph = workflow.compile()

if __name__ == "__main__":
    print("Probando grafo...")
    inputs = cast(AgentState, {"messages": [HumanMessage(content="Escribe un código en python")]})
    for output in kalmiya_brain_graph.stream(inputs):
        for key, value in output.items():
            print(f"[{key}]: {value}")
