"""Tools — business system functions for compliance review.

Current retrieval is keyword-based because the demo regulation corpus is small and structured.
"""

import json
from pathlib import Path

from langchain_core.tools import tool

DATA_DIR = Path(__file__).parent.parent / "data"

_regulations: dict[str, str] | None = None
_materials: dict[str, dict] | None = None


def _load_regulations() -> dict[str, str]:
    global _regulations
    if _regulations is None:
        _regulations = {}
        reg_dir = DATA_DIR / "regulations"
        for fp in reg_dir.glob("*.md"):
            _regulations[fp.stem] = fp.read_text(encoding="utf-8")
    return _regulations


def _load_materials() -> dict[str, dict]:
    global _materials
    if _materials is None:
        _materials = {}
        with open(DATA_DIR / "materials.jsonl", encoding="utf-8") as f:
            for line in f:
                m = json.loads(line)
                _materials[m["id"]] = m
    return _materials


def search_regulations(query: str, n_results: int = 3) -> list[dict]:
    """Search regulation documents by keyword matching.

    Production upgrade: add vector/BM25 retrieval only when corpus scale or weak structure requires it.
    """
    regs = _load_regulations()
    results = []
    query_lower = query.lower()
    for name, content in regs.items():
        if query_lower in content.lower():
            idx = content.lower().find(query_lower)
            start = max(0, idx - 100)
            end = min(len(content), idx + 400)
            results.append({
                "source": name,
                "excerpt": content[start:end],
                "relevance": 0.8,
            })
    return results[:n_results]


@tool
def search_regulations_tool(query: str) -> str:
    """Search compliance regulations by keyword. Returns matching regulation excerpts."""
    results = search_regulations(query)
    if not results:
        return "未找到相关法规。"
    parts = []
    for r in results:
        parts.append(f"[{r['source']}]\n{r['excerpt']}")
    return "\n\n---\n\n".join(parts)


def check_related_party(material_id: str) -> bool:
    """Check if material involves related party transactions."""
    materials = _load_materials()
    m = materials.get(material_id)
    if m is None:
        return False
    return m.get("关联方标记", False)


def check_data_isolation(material_id: str) -> bool:
    """Check if material involves cross-segment data sharing."""
    materials = _load_materials()
    m = materials.get(material_id)
    if m is None:
        return False
    return m.get("涉及数据共享", False) and m.get("涉及受监管业务", False)


def get_material(material_id: str) -> dict | None:
    """Get material by ID."""
    materials = _load_materials()
    return materials.get(material_id)
