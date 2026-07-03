"""初版脚手架：当前数据已手动扩展至 13 个材料和 7 篇法规，脚本不再完整反映现状。"""

"""Generate synthetic compliance data for demo.

All data is FICTIONAL. Based on general compliance patterns,
not any specific company's policies.
"""

import json
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"


def build_regulations():
    """General compliance regulations — anonymized, cross-industry."""
    regs = {
        "反垄断合规.md": """# 反垄断合规审查指引

## 适用范围
- 涉及受监管业务板块与竞争性业务板块之间的数据共享
- 关联方交易
- 市场支配地位相关的商业安排

## 审查要点
1. 交易双方是否属于同一集团下的不同业务板块
2. 是否存在受监管业务的客户数据流向竞争性业务
3. 定价是否符合市场公允原则
4. 是否存在强制搭售或排他性条款

## 风险等级判定
- **高风险**：受监管业务客户数据直接流向竞争性业务
- **中风险**：同一集团下不同板块合作，需数据隔离措施
- **低风险**：独立第三方交易，无数据交叉
""",
        "关联交易审查.md": """# 关联交易审查指引

## 适用范围
- 集团内部公司之间的交易
- 与股东、高管有关联的外部交易
- 同一实际控制人下的企业间交易

## 审查要点
1. 是否已披露关联关系
2. 定价是否经过独立评估
3. 是否经过关联方回避的审批程序
4. 交易条件是否优于或劣于市场条件

## 风险等级判定
- **高风险**：未披露关联关系 + 定价未经独立评估
- **中风险**：已披露但定价依据不充分
- **低风险**：已披露 + 独立评估 + 审批程序完整
""",
        "数据隐私合规.md": """# 数据隐私合规审查指引

## 适用范围
- 涉及个人信息处理的合同
- 跨境数据传输
- 数据共享协议

## 审查要点
1. 是否明确数据处理目的和范围
2. 是否获得数据主体同意
3. 是否有数据安全保护措施
4. 是否符合数据本地化要求

## 风险等级判定
- **高风险**：跨境传输 + 无安全保障
- **中风险**：国内共享 + 保障措施不完整
- **低风险**：已获同意 + 安全措施完整
""",
        "财务合规审查.md": """# 财务合规审查指引

## 适用范围
- 大额采购合同
- 对外担保合同
- 借款合同

## 审查要点
1. 是否在预算范围内
2. 付款条件是否合理
3. 发票条款是否合规
4. 是否需要税务专项审查

## 风险等级判定
- **高风险**：超预算 + 无审批 + 对外担保
- **中风险**：预算内但付款条件异常
- **低风险**：预算内 + 标准付款条件
""",
    }
    return regs


def build_materials():
    """Review materials — 4 scenarios, anonymized."""
    return [
        {
            "id": "M001",
            "test_case": "normal_pass",
            "材料类型": "采购合同",
            "板块": "A",
            "内容摘要": "标准设备采购，非关联方，市场价格，预算内",
            "关联方标记": False,
            "金额": 200000,
            "涉及数据共享": False,
            "涉及受监管业务": False,
            "说明": "标准采购，无合规风险",
        },
        {
            "id": "M002",
            "test_case": "related_party_review",
            "材料类型": "服务合同",
            "板块": "B",
            "内容摘要": "集团内子公司之间的技术服务合同，定价需审查",
            "关联方标记": True,
            "金额": 800000,
            "涉及数据共享": False,
            "涉及受监管业务": False,
            "说明": "关联交易，定价需独立评估",
        },
        {
            "id": "M003",
            "test_case": "high_risk_block",
            "材料类型": "担保合同",
            "板块": "A",
            "内容摘要": "对外担保，大额，不可撤销条款",
            "关联方标记": False,
            "金额": 10000000,
            "涉及数据共享": False,
            "涉及受监管业务": False,
            "条款标记": {"不可逆": True, "担保": True},
            "说明": "大额担保，高风险",
        },
        {
            "id": "M004",
            "test_case": "isolation_block",
            "材料类型": "合作协议",
            "板块": "B",
            "内容摘要": "涉及受监管业务板块客户数据的合作安排",
            "关联方标记": False,
            "金额": 500000,
            "涉及数据共享": True,
            "涉及受监管业务": True,
            "说明": "受监管业务数据流向竞争性业务，需隔离审查",
        },
    ]


def main():
    regs = build_regulations()
    materials = build_materials()

    # Write regulations
    reg_dir = DATA_DIR / "regulations"
    reg_dir.mkdir(parents=True, exist_ok=True)
    for name, content in regs.items():
        with open(reg_dir / name, "w", encoding="utf-8") as f:
            f.write(content)
    print(f"[OK] regulations/ — {len(regs)} files")

    # Write materials
    with open(DATA_DIR / "materials.jsonl", "w", encoding="utf-8") as f:
        for m in materials:
            f.write(json.dumps(m, ensure_ascii=False) + "\n")
    print(f"[OK] materials.jsonl — {len(materials)} entries")

    print(f"\nScenario coverage:")
    for m in materials:
        print(f"  {m['id']} | {m['test_case']:25s} | {m['说明']}")


if __name__ == "__main__":
    main()
