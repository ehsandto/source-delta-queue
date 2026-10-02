import ast
from pathlib import Path


def functions():
    selected = [node for node in ast.parse(Path("contracts/SourceDeltaQueue.py").read_text(encoding="utf-8")).body
                if isinstance(node, ast.FunctionDef) and node.name in ("dispatch_rank", "reports_equal")]
    namespace = {}
    exec(compile(ast.Module(body=selected, type_ignores=[]), "policy", "exec"), namespace)
    return namespace


def test_exact_equivalence_rejects_priority_and_vector_disagreement():
    equal = functions()["reports_equal"]
    leader = {"priority": "URGENT", "exception_change": "CHANGED", "source_sha256": "a"}
    assert equal(leader, leader.copy())
    for field, value in (("priority", "NORMAL"), ("exception_change", "UNKNOWN"), ("source_sha256", "b")):
        assert not equal(leader, {**leader, field: value})


def test_priority_aging_prevents_normal_starvation():
    rank = functions()["dispatch_rank"]
    normal = {"priority": "NORMAL", "queued_at": 0, "ordinal": 0}
    urgent = {"priority": "URGENT", "queued_at": 599, "ordinal": 1}
    assert rank(urgent, 599) < rank(normal, 599)
    assert rank(normal, 600) < rank(urgent, 600)
