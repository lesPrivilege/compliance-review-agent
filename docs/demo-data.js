// Auto-generated from data/materials.jsonl + data/audit_log.jsonl. Regenerate with scripts/build_demo_data.py.
const MATERIALS = [
  {
    "id": "M001",
    "test_case": "normal_pass",
    "材料类型": "采购合同",
    "板块": "A",
    "内容摘要": "标准设备采购，非关联方，市场价格，预算内",
    "关联方标记": false,
    "金额": 200000,
    "涉及数据共享": false,
    "涉及受监管业务": false,
    "说明": "标准采购，无合规风险",
    "hasTrace": true,
    "risk": "low",
    "outcome": "auto_approved",
    "hitl": false
  },
  {
    "id": "M002",
    "test_case": "related_party_review",
    "材料类型": "服务合同",
    "板块": "B",
    "内容摘要": "集团内子公司之间的技术服务合同，定价需审查",
    "关联方标记": true,
    "金额": 800000,
    "涉及数据共享": false,
    "涉及受监管业务": false,
    "说明": "关联交易，定价需独立评估",
    "hasTrace": true,
    "risk": "medium",
    "outcome": "approved",
    "hitl": true
  },
  {
    "id": "M003",
    "test_case": "high_risk_block",
    "材料类型": "担保合同",
    "板块": "A",
    "内容摘要": "对外担保，大额，不可撤销条款",
    "关联方标记": false,
    "金额": 10000000,
    "涉及数据共享": false,
    "涉及受监管业务": false,
    "条款标记": {
      "不可逆": true,
      "担保": true
    },
    "说明": "大额担保，高风险",
    "hasTrace": true,
    "risk": "high",
    "outcome": "rejected",
    "hitl": true
  },
  {
    "id": "M004",
    "test_case": "isolation_block",
    "材料类型": "合作协议",
    "板块": "B",
    "内容摘要": "涉及受监管业务板块客户数据的合作安排",
    "关联方标记": false,
    "金额": 500000,
    "涉及数据共享": true,
    "涉及受监管业务": true,
    "说明": "受监管业务数据流向竞争性业务，需隔离审查",
    "hasTrace": true,
    "risk": "high",
    "outcome": "approved",
    "hitl": true
  },
  {
    "id": "M005",
    "test_case": "c_sector_low_risk",
    "材料类型": "服务合同",
    "板块": "C",
    "内容摘要": "标准营销推广服务合同，市场价格，消费者权益保障完整",
    "关联方标记": false,
    "金额": 150000,
    "涉及数据共享": false,
    "涉及受监管业务": false,
    "说明": "C板块标准服务，无合规风险",
    "hasTrace": true,
    "risk": "low",
    "outcome": "auto_approved",
    "hitl": false
  },
  {
    "id": "M006",
    "test_case": "c_sector_medium_risk",
    "材料类型": "销售合同",
    "板块": "C",
    "内容摘要": "渠道分销合同，涉及定价安排和消费者权益",
    "关联方标记": false,
    "金额": 6000000,
    "涉及数据共享": false,
    "涉及受监管业务": false,
    "说明": "C板块大额销售，需审查定价合理性",
    "hasTrace": true,
    "risk": "medium",
    "outcome": "approved",
    "hitl": true
  },
  {
    "id": "M007",
    "test_case": "d_sector_low_risk",
    "材料类型": "采购合同",
    "板块": "D",
    "内容摘要": "行政办公家具采购，标准流程，预算内",
    "关联方标记": false,
    "金额": 80000,
    "涉及数据共享": false,
    "涉及受监管业务": false,
    "说明": "D板块行政采购，无合规风险",
    "hasTrace": true,
    "risk": "low",
    "outcome": "auto_approved",
    "hitl": false
  },
  {
    "id": "M008",
    "test_case": "d_sector_guarantee_high",
    "材料类型": "担保合同",
    "板块": "D",
    "内容摘要": "对外担保合同，涉及借贷担保，需关联主合同审查",
    "关联方标记": false,
    "金额": 8000000,
    "涉及数据共享": false,
    "涉及受监管业务": false,
    "条款标记": {
      "担保": true
    },
    "说明": "D板块大额担保，高风险",
    "hasTrace": true,
    "risk": "high",
    "outcome": "rejected",
    "hitl": true
  },
  {
    "id": "M009",
    "test_case": "franchise_compliance",
    "材料类型": "特许经营权协议",
    "板块": "A",
    "内容摘要": "管道燃气特许经营权协议，需审查招投标合规和经营权使用费",
    "关联方标记": false,
    "金额": 2000000,
    "涉及数据共享": false,
    "涉及受监管业务": true,
    "说明": "A板块特许经营权，命中特许经营权合规审查",
    "hasTrace": true,
    "risk": "low",
    "outcome": "auto_approved",
    "hitl": false
  },
  {
    "id": "M010",
    "test_case": "antitrust_filing",
    "材料类型": "投资合作合同",
    "板块": "B",
    "内容摘要": "投资项目合作协议，需审查投资评审条件落地和反垄断申报阈值",
    "关联方标记": false,
    "金额": 4000000,
    "涉及数据共享": false,
    "涉及受监管业务": false,
    "说明": "B板块投资合作，命中反垄断申报阈值审查",
    "hasTrace": true,
    "risk": "medium",
    "outcome": "approved",
    "hitl": true
  },
  {
    "id": "M011",
    "test_case": "llm_one_shot",
    "材料类型": "采购合同",
    "板块": "A",
    "内容摘要": "集团内子公司之间的设备采购合同，定价需审查是否符合关联交易规定",
    "关联方标记": true,
    "金额": 300000,
    "涉及数据共享": false,
    "涉及受监管业务": false,
    "说明": "关联交易，现有法规一次检索应足够",
    "hasTrace": false,
    "risk": null,
    "outcome": null,
    "hitl": false
  },
  {
    "id": "M012",
    "test_case": "llm_multi_turn",
    "材料类型": "合作协议",
    "板块": "B",
    "内容摘要": "涉及受监管业务板块客户数据的投资合作安排，需审查数据隔离和反垄断合规",
    "关联方标记": false,
    "金额": 5000000,
    "涉及数据共享": true,
    "涉及受监管业务": true,
    "说明": "跨业务数据共享，需要多轮检索才能给出完整结论",
    "hasTrace": false,
    "risk": null,
    "outcome": null,
    "hitl": false
  },
  {
    "id": "M013",
    "test_case": "llm_no_match",
    "材料类型": "服务合同",
    "板块": "C",
    "内容摘要": "量子计算技术咨询服务合同，涉及前沿科技领域",
    "关联方标记": false,
    "金额": 100000,
    "涉及数据共享": false,
    "涉及受监管业务": false,
    "说明": "法规库无相关内容，LLM 应诚实给出低置信度",
    "hasTrace": false,
    "risk": null,
    "outcome": null,
    "hitl": false
  }
];
const TRACE = {
  "M001": [
    {
      "node": "ingest",
      "action": "parse_material",
      "input_summary": "材料 M001: 采购合同",
      "output_summary": "提取 0 个关键条款: 无",
      "decision": "parsed",
      "duration_ms": 1,
      "tokens_in": null,
      "tokens_out": null
    },
    {
      "node": "retrieve",
      "action": "search_regulations",
      "input_summary": "查询: 采购合同, 标准设备采购，非关联方，市场价格，预算内",
      "output_summary": "检索到 1 条法规",
      "decision": "found",
      "duration_ms": 1,
      "tokens_in": null,
      "tokens_out": null
    },
    {
      "node": "analyze",
      "action": "multi_step_analysis",
      "input_summary": "1 条法规, 0 个风险因素",
      "output_summary": "无明显合规风险",
      "decision": "analyzed",
      "duration_ms": 1,
      "tokens_in": null,
      "tokens_out": null
    },
    {
      "node": "score",
      "action": "risk_scoring",
      "input_summary": "风险因素: 0",
      "output_summary": "风险等级: low",
      "decision": "low",
      "duration_ms": 1,
      "tokens_in": null,
      "tokens_out": null
    },
    {
      "node": "hitl",
      "action": "auto_approve",
      "input_summary": "低风险，无需人工确认",
      "output_summary": "自动通过",
      "decision": "auto_approved",
      "duration_ms": 1,
      "tokens_in": null,
      "tokens_out": null
    }
  ],
  "M002": [
    {
      "node": "ingest",
      "action": "parse_material",
      "input_summary": "材料 M002: 服务合同",
      "output_summary": "提取 1 个关键条款: 关联交易",
      "decision": "parsed",
      "duration_ms": 1,
      "tokens_in": null,
      "tokens_out": null
    },
    {
      "node": "retrieve",
      "action": "search_regulations",
      "input_summary": "查询: 服务合同, 集团内子公司之间的技术服务合同，定价需审查, 关联交易",
      "output_summary": "检索到 2 条法规",
      "decision": "found",
      "duration_ms": 1,
      "tokens_in": null,
      "tokens_out": null
    },
    {
      "node": "analyze",
      "action": "multi_step_analysis",
      "input_summary": "2 条法规, 1 个风险因素",
      "output_summary": "关联交易，定价需独立评估",
      "decision": "analyzed",
      "duration_ms": 1,
      "tokens_in": null,
      "tokens_out": null
    },
    {
      "node": "score",
      "action": "risk_scoring",
      "input_summary": "风险因素: 1",
      "output_summary": "风险等级: medium",
      "decision": "medium",
      "duration_ms": 1,
      "tokens_in": null,
      "tokens_out": null
    },
    {
      "node": "hitl",
      "action": "human_review",
      "input_summary": "需人工确认: 风险等级 medium，需人工确认",
      "output_summary": "人工决策: approved",
      "decision": "approved",
      "duration_ms": 1,
      "tokens_in": null,
      "tokens_out": null
    }
  ],
  "M003": [
    {
      "node": "ingest",
      "action": "parse_material",
      "input_summary": "材料 M003: 担保合同",
      "output_summary": "提取 3 个关键条款: 对外担保, 不可撤销条款, 大额交易",
      "decision": "parsed",
      "duration_ms": 1,
      "tokens_in": null,
      "tokens_out": null
    },
    {
      "node": "retrieve",
      "action": "search_regulations",
      "input_summary": "查询: 担保合同, 对外担保，大额，不可撤销条款, 担保",
      "output_summary": "检索到 2 条法规",
      "decision": "found",
      "duration_ms": 1,
      "tokens_in": null,
      "tokens_out": null
    },
    {
      "node": "analyze",
      "action": "multi_step_analysis",
      "input_summary": "2 条法规, 3 个风险因素",
      "output_summary": "存在高风险条款，需人工确认",
      "decision": "analyzed",
      "duration_ms": 1,
      "tokens_in": null,
      "tokens_out": null
    },
    {
      "node": "score",
      "action": "risk_scoring",
      "input_summary": "风险因素: 3",
      "output_summary": "风险等级: high",
      "decision": "high",
      "duration_ms": 1,
      "tokens_in": null,
      "tokens_out": null
    },
    {
      "node": "hitl",
      "action": "human_review",
      "input_summary": "需人工确认: 风险等级 high，需人工确认",
      "output_summary": "人工决策: rejected",
      "decision": "rejected",
      "duration_ms": 1,
      "tokens_in": null,
      "tokens_out": null
    }
  ],
  "M004": [
    {
      "node": "ingest",
      "action": "parse_material",
      "input_summary": "材料 M004: 合作协议",
      "output_summary": "提取 2 个关键条款: 数据共享, 涉及受监管业务",
      "decision": "parsed",
      "duration_ms": 1,
      "tokens_in": null,
      "tokens_out": null
    },
    {
      "node": "retrieve",
      "action": "search_regulations",
      "input_summary": "查询: 合作协议, 涉及受监管业务板块客户数据的合作安排, 数据隐私",
      "output_summary": "检索到 1 条法规",
      "decision": "found",
      "duration_ms": 1,
      "tokens_in": null,
      "tokens_out": null
    },
    {
      "node": "analyze",
      "action": "multi_step_analysis",
      "input_summary": "1 条法规, 1 个风险因素",
      "output_summary": "存在跨业务合规风险，需隔离审查",
      "decision": "analyzed",
      "duration_ms": 1,
      "tokens_in": null,
      "tokens_out": null
    },
    {
      "node": "score",
      "action": "risk_scoring",
      "input_summary": "风险因素: 1",
      "output_summary": "风险等级: high",
      "decision": "high",
      "duration_ms": 1,
      "tokens_in": null,
      "tokens_out": null
    },
    {
      "node": "hitl",
      "action": "human_review",
      "input_summary": "需人工确认: 跨业务数据共享，需合规审查",
      "output_summary": "人工决策: approved",
      "decision": "approved",
      "duration_ms": 1,
      "tokens_in": null,
      "tokens_out": null
    }
  ],
  "M005": [
    {
      "node": "ingest",
      "action": "parse_material",
      "input_summary": "材料 M005: 服务合同",
      "output_summary": "提取 0 个关键条款: 无",
      "decision": "parsed",
      "duration_ms": 1,
      "tokens_in": null,
      "tokens_out": null
    },
    {
      "node": "retrieve",
      "action": "search_regulations",
      "input_summary": "查询: 服务合同, 标准营销推广服务合同，市场价格，消费者权益保障完整",
      "output_summary": "检索到 1 条法规",
      "decision": "found",
      "duration_ms": 1,
      "tokens_in": null,
      "tokens_out": null
    },
    {
      "node": "analyze",
      "action": "multi_step_analysis",
      "input_summary": "1 条法规, 0 个风险因素",
      "output_summary": "无明显合规风险",
      "decision": "analyzed",
      "duration_ms": 1,
      "tokens_in": null,
      "tokens_out": null
    },
    {
      "node": "score",
      "action": "risk_scoring",
      "input_summary": "风险因素: 0",
      "output_summary": "风险等级: low",
      "decision": "low",
      "duration_ms": 1,
      "tokens_in": null,
      "tokens_out": null
    },
    {
      "node": "hitl",
      "action": "auto_approve",
      "input_summary": "低风险，无需人工确认",
      "output_summary": "自动通过",
      "decision": "auto_approved",
      "duration_ms": 1,
      "tokens_in": null,
      "tokens_out": null
    }
  ],
  "M006": [
    {
      "node": "ingest",
      "action": "parse_material",
      "input_summary": "材料 M006: 销售合同",
      "output_summary": "提取 1 个关键条款: 大额交易",
      "decision": "parsed",
      "duration_ms": 1,
      "tokens_in": null,
      "tokens_out": null
    },
    {
      "node": "retrieve",
      "action": "search_regulations",
      "input_summary": "查询: 销售合同, 渠道分销合同，涉及定价安排和消费者权益",
      "output_summary": "检索到 1 条法规",
      "decision": "found",
      "duration_ms": 1,
      "tokens_in": null,
      "tokens_out": null
    },
    {
      "node": "analyze",
      "action": "multi_step_analysis",
      "input_summary": "1 条法规, 1 个风险因素",
      "output_summary": "存在中等风险，建议审查",
      "decision": "analyzed",
      "duration_ms": 1,
      "tokens_in": null,
      "tokens_out": null
    },
    {
      "node": "score",
      "action": "risk_scoring",
      "input_summary": "风险因素: 1",
      "output_summary": "风险等级: medium",
      "decision": "medium",
      "duration_ms": 1,
      "tokens_in": null,
      "tokens_out": null
    },
    {
      "node": "hitl",
      "action": "human_review",
      "input_summary": "需人工确认: 风险等级 medium，需人工确认",
      "output_summary": "人工决策: approved",
      "decision": "approved",
      "duration_ms": 1,
      "tokens_in": null,
      "tokens_out": null
    }
  ],
  "M007": [
    {
      "node": "ingest",
      "action": "parse_material",
      "input_summary": "材料 M007: 采购合同",
      "output_summary": "提取 0 个关键条款: 无",
      "decision": "parsed",
      "duration_ms": 1,
      "tokens_in": null,
      "tokens_out": null
    },
    {
      "node": "retrieve",
      "action": "search_regulations",
      "input_summary": "查询: 采购合同, 行政办公家具采购，标准流程，预算内",
      "output_summary": "检索到 1 条法规",
      "decision": "found",
      "duration_ms": 1,
      "tokens_in": null,
      "tokens_out": null
    },
    {
      "node": "analyze",
      "action": "multi_step_analysis",
      "input_summary": "1 条法规, 0 个风险因素",
      "output_summary": "无明显合规风险",
      "decision": "analyzed",
      "duration_ms": 1,
      "tokens_in": null,
      "tokens_out": null
    },
    {
      "node": "score",
      "action": "risk_scoring",
      "input_summary": "风险因素: 0",
      "output_summary": "风险等级: low",
      "decision": "low",
      "duration_ms": 1,
      "tokens_in": null,
      "tokens_out": null
    },
    {
      "node": "hitl",
      "action": "auto_approve",
      "input_summary": "低风险，无需人工确认",
      "output_summary": "自动通过",
      "decision": "auto_approved",
      "duration_ms": 1,
      "tokens_in": null,
      "tokens_out": null
    }
  ],
  "M008": [
    {
      "node": "ingest",
      "action": "parse_material",
      "input_summary": "材料 M008: 担保合同",
      "output_summary": "提取 2 个关键条款: 对外担保, 大额交易",
      "decision": "parsed",
      "duration_ms": 1,
      "tokens_in": null,
      "tokens_out": null
    },
    {
      "node": "retrieve",
      "action": "search_regulations",
      "input_summary": "查询: 担保合同, 对外担保合同，涉及借贷担保，需关联主合同审查, 担保",
      "output_summary": "检索到 2 条法规",
      "decision": "found",
      "duration_ms": 1,
      "tokens_in": null,
      "tokens_out": null
    },
    {
      "node": "analyze",
      "action": "multi_step_analysis",
      "input_summary": "2 条法规, 2 个风险因素",
      "output_summary": "存在高风险条款，需人工确认",
      "decision": "analyzed",
      "duration_ms": 1,
      "tokens_in": null,
      "tokens_out": null
    },
    {
      "node": "score",
      "action": "risk_scoring",
      "input_summary": "风险因素: 2",
      "output_summary": "风险等级: high",
      "decision": "high",
      "duration_ms": 1,
      "tokens_in": null,
      "tokens_out": null
    },
    {
      "node": "hitl",
      "action": "human_review",
      "input_summary": "需人工确认: 风险等级 high，需人工确认",
      "output_summary": "人工决策: rejected",
      "decision": "rejected",
      "duration_ms": 1,
      "tokens_in": null,
      "tokens_out": null
    }
  ],
  "M009": [
    {
      "node": "ingest",
      "action": "parse_material",
      "input_summary": "材料 M009: 特许经营权协议",
      "output_summary": "提取 1 个关键条款: 涉及受监管业务",
      "decision": "parsed",
      "duration_ms": 1,
      "tokens_in": null,
      "tokens_out": null
    },
    {
      "node": "retrieve",
      "action": "search_regulations",
      "input_summary": "查询: 特许经营权协议, 管道燃气特许经营权协议，需审查招投标合规和经营权使用费",
      "output_summary": "检索到 1 条法规",
      "decision": "found",
      "duration_ms": 1,
      "tokens_in": null,
      "tokens_out": null
    },
    {
      "node": "analyze",
      "action": "multi_step_analysis",
      "input_summary": "1 条法规, 0 个风险因素",
      "output_summary": "无明显合规风险",
      "decision": "analyzed",
      "duration_ms": 1,
      "tokens_in": null,
      "tokens_out": null
    },
    {
      "node": "score",
      "action": "risk_scoring",
      "input_summary": "风险因素: 0",
      "output_summary": "风险等级: low",
      "decision": "low",
      "duration_ms": 1,
      "tokens_in": null,
      "tokens_out": null
    },
    {
      "node": "hitl",
      "action": "auto_approve",
      "input_summary": "低风险，无需人工确认",
      "output_summary": "自动通过",
      "decision": "auto_approved",
      "duration_ms": 1,
      "tokens_in": null,
      "tokens_out": null
    }
  ],
  "M010": [
    {
      "node": "ingest",
      "action": "parse_material",
      "input_summary": "材料 M010: 投资合作合同",
      "output_summary": "提取 0 个关键条款: 无",
      "decision": "parsed",
      "duration_ms": 1,
      "tokens_in": null,
      "tokens_out": null
    },
    {
      "node": "retrieve",
      "action": "search_regulations",
      "input_summary": "查询: 投资合作合同, 投资项目合作协议，需审查投资评审条件落地和反垄断申报阈值",
      "output_summary": "检索到 0 条法规",
      "decision": "missing",
      "duration_ms": 1,
      "tokens_in": null,
      "tokens_out": null
    },
    {
      "node": "analyze",
      "action": "multi_step_analysis",
      "input_summary": "0 条法规, 1 个风险因素",
      "output_summary": "存在中等风险，建议审查",
      "decision": "analyzed",
      "duration_ms": 1,
      "tokens_in": null,
      "tokens_out": null
    },
    {
      "node": "score",
      "action": "risk_scoring",
      "input_summary": "风险因素: 1",
      "output_summary": "风险等级: medium",
      "decision": "medium",
      "duration_ms": 1,
      "tokens_in": null,
      "tokens_out": null
    },
    {
      "node": "hitl",
      "action": "human_review",
      "input_summary": "需人工确认: 风险等级 medium，需人工确认",
      "output_summary": "人工决策: approved",
      "decision": "approved",
      "duration_ms": 1,
      "tokens_in": null,
      "tokens_out": null
    }
  ]
};
