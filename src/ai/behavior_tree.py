"""
Implementación de Árbol de Comportamiento (Behavior Tree) para unidades y NPCs.
"""
from enum import Enum
from typing import List, Callable, Any, Optional, Dict


class NodeStatus(Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    RUNNING = "RUNNING"


class BehaviorNode:
    def __init__(self, name: str = "Node"):
        self.name = name

    def tick(self, blackboard: Dict[str, Any]) -> NodeStatus:
        raise NotImplementedError("tick() debe implementarse en la subclase.")


class Selector(BehaviorNode):
    """Ejecuta hijos secuencialmente. Si uno tiene éxito, el selector tiene éxito (Fallback / OR)."""
    def __init__(self, name: str, children: Optional[List[BehaviorNode]] = None):
        super().__init__(name)
        self.children = children or []

    def tick(self, blackboard: Dict[str, Any]) -> NodeStatus:
        for child in self.children:
            status = child.tick(blackboard)
            if status != NodeStatus.FAILURE:
                return status
        return NodeStatus.FAILURE


class Sequence(BehaviorNode):
    """Ejecuta hijos secuencialmente. Todos deben tener éxito para que la secuencia tenga éxito (AND)."""
    def __init__(self, name: str, children: Optional[List[BehaviorNode]] = None):
        super().__init__(name)
        self.children = children or []

    def tick(self, blackboard: Dict[str, Any]) -> NodeStatus:
        for child in self.children:
            status = child.tick(blackboard)
            if status != NodeStatus.SUCCESS:
                return status
        return NodeStatus.SUCCESS


class ConditionNode(BehaviorNode):
    """Evalúa un predicado booleano en la pizarra (blackboard)."""
    def __init__(self, name: str, condition_fn: Callable[[Dict[str, Any]], bool]):
        super().__init__(name)
        self.condition_fn = condition_fn

    def tick(self, blackboard: Dict[str, Any]) -> NodeStatus:
        return NodeStatus.SUCCESS if self.condition_fn(blackboard) else NodeStatus.FAILURE


class ActionNode(BehaviorNode):
    """Ejecuta una acción concreta y retorna su estado."""
    def __init__(self, name: str, action_fn: Callable[[Dict[str, Any]], NodeStatus]):
        super().__init__(name)
        self.action_fn = action_fn

    def tick(self, blackboard: Dict[str, Any]) -> NodeStatus:
        return self.action_fn(blackboard)
