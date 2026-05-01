#!/usr/bin/env python3
"""
开窍辅助脚本 (kaqiao.py)
用于经验库维护：健康度检查、置信度升级、认知对齐提醒、生成报告

用法：
    python kaqiao.py check    # 检查经验库健康度
    python kaqiao.py promote  # 升级符合条件的假设/经验
    python kaqiao.py align    # 生成认知对齐提醒
    python kaqiao.py report   # 生成经验库报告
    python kaqiao.py all      # 执行所有检查
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

# 配置
DATA_DIR = Path("./开窍数据")
OWNER_PROFILE_FILE = DATA_DIR / "主人画像.json"
EXPERIENCE_DB_FILE = DATA_DIR / "经验库.json"
CONFIG_FILE = DATA_DIR / "config.json"

# 默认配置
DEFAULT_CONFIG = {
    "假设过期天数": 14,
    "经验过期天数": 90,
    "铁律过期天数": 180,
    "假设升级阈值": 3,
    "经验升级阈值": 5,
    "对齐提醒周期_天": 14
}


def load_json(file_path: Path, default=None):
    """加载JSON文件"""
    if not file_path.exists():
        return default
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return default


def save_json(file_path: Path, data):
    """保存JSON文件"""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_config():
    """加载配置"""
    return load_json(CONFIG_FILE, DEFAULT_CONFIG)


def load_experience_db():
    """加载经验库"""
    return load_json(EXPERIENCE_DB_FILE, {"cards": [], "last_updated": None})


def save_experience_db(db):
    """保存经验库"""
    db["last_updated"] = datetime.now().isoformat()
    save_json(EXPERIENCE_DB_FILE, db)


def load_owner_profile():
    """加载主人画像"""
    return load_json(OWNER_PROFILE_FILE, {"name": "未知", "last_updated": None})


def days_since(date_str: str) -> int:
    """计算距离某天的天数"""
    try:
        date = datetime.fromisoformat(date_str)
        return (datetime.now() - date).days
    except (ValueError, TypeError):
        return 999


def days_until(date_str: str) -> int:
    """计算距离某天还有多少天（负数表示已过期）"""
    try:
        date = datetime.fromisoformat(date_str)
        return (date - datetime.now()).days
    except (ValueError, TypeError):
        return 0


def print_header(text: str):
    """打印标题"""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print('='*60)


def print_subheader(text: str):
    """打印副标题"""
    print(f"\n## {text}")
    print("-" * 40)


def check_health():
    """检查经验库健康度"""
    print_header("📊 经验库健康度检查")
    
    config = load_config()
    db = load_experience_db()
    cards = db.get("cards", [])
    
    if not cards:
        print("⚠️  经验库为空，还没有记录任何经验")
        return
    
    results = {
        "total": len(cards),
        "假设": 0,
        "经验": 0,
        "铁律": 0,
        "过期_假设": [],
        "过期_经验": [],
        "过期_铁律": [],
        "待验证_假设": [],
        "长期未更新": []
    }
    
    now = datetime.now()
    
    for card in cards:
        confidence = card.get("置信度", "假设")
        results[confidence] = results.get(confidence, 0) + 1
        
        last_verify = card.get("上次验证", card.get("创建时间", ""))
        days = days_since(last_verify)
        
        # 检查过期
        if confidence == "假设":
            if days > config["假设过期天数"]:
                results["过期_假设"].append((card, days))
        elif confidence == "经验":
            if days > config["经验过期天数"]:
                results["过期_经验"].append((card, days))
        elif confidence == "铁律":
            if days > config["铁律过期天数"]:
                results["过期_铁律"].append((card, days))
        
        # 检查长期未验证的假设
        if confidence == "假设" and days > 7:
            results["待验证_假设"].append((card, days))
        
        # 检查长期未更新的卡片
        created = card.get("创建时间", "")
        if created and days_since(created) > 90:
            results["长期未更新"].append((card, days_since(created)))
    
    # 输出结果
    print(f"\n📈 总体统计：")
    print(f"   总经验数：{results['total']}")
    print(f"   ⭐ 假设：{results['假设']} 条")
    print(f"   ⭐⭐ 经验：{results['经验']} 条")
    print(f"   ⭐⭐⭐ 铁律：{results['铁律']} 条")
    
    # 过期检查
    print(f"\n⚠️  需要关注的经验：")
    
    if results["过期_铁律"]:
        print(f"\n   🔴 铁律过期（>{config['铁律过期天数']}天未验证）：")
        for card, days in results["过期_铁律"]:
            print(f"      - {card.get('场景名', '未命名')} ({days}天)")
    
    if results["过期_经验"]:
        print(f"\n   🟡 经验过期（>{config['经验过期天数']}天未验证）：")
        for card, days in results["过期_经验"]:
            print(f"      - {card.get('场景名', '未命名')} ({days}天)")
    
    if results["过期_假设"]:
        print(f"\n   🟠 假设过期（>{config['假设过期天数']}天未验证）：")
        for card, days in results["过期_假设"]:
            print(f"      - {card.get('场景名', '未命名')} ({days}天)")
    
    if results["待验证_假设"]:
        print(f"\n   💡 待验证假设（>7天未验证）：")
        for card, days in results["待验证_假设"]:
            print(f"      - {card.get('场景名', '未命名')} ({days}天)")
    
    if not any([results["过期_铁律"], results["过期_经验"], 
                results["过期_假设"], results["待验证_假设"]]):
        print("\n   ✅ 没有需要特别关注的经验")
    
    return results


def promote_confidence():
    """升级符合条件的置信度"""
    print_header("⬆️ 置信度升级检查")
    
    config = load_config()
    db = load_experience_db()
    cards = db.get("cards", [])
    
    if not cards:
        print("⚠️  经验库为空")
        return
    
    promote_count = 0
    demote_count = 0
    
    for card in cards:
        confidence = card.get("置信度", "假设")
        verify_count = card.get("验证次数", 0)
        
        # 升级检查
        if confidence == "假设" and verify_count >= config["假设升级阈值"]:
            old = card["置信度"]
            card["置信度"] = "经验"
            print(f"\n⬆️ 升级假设 → 经验：")
            print(f"   场景：{card.get('场景名', '未命名')}")
            print(f"   验证次数：{verify_count}")
            print(f"   升级原因：验证次数达到{config['假设升级阈值']}次")
            promote_count += 1
            
        elif confidence == "经验" and verify_count >= config["经验升级阈值"]:
            old = card["置信度"]
            card["置信度"] = "铁律"
            print(f"\n⬆️⬆️ 升级经验 → 铁律：")
            print(f"   场景：{card.get('场景名', '未命名')}")
            print(f"   验证次数：{verify_count}")
            print(f"   升级原因：验证次数达到{config['经验升级阈值']}次")
            promote_count += 1
    
    if promote_count > 0:
        save_experience_db(db)
        print(f"\n✅ 已保存升级结果，共升级 {promote_count} 条经验")
    else:
        print("\nℹ️  没有需要升级的经验")


def generate_alignment_reminders():
    """生成认知对齐提醒"""
    print_header("🔄 认知对齐提醒")
    
    config = load_config()
    db = load_experience_db()
    profile = load_owner_profile()
    cards = db.get("cards", [])
    
    if not cards:
        print("⚠️  经验库为空，没有需要对齐的内容")
        return []
    
    reminders = []
    now = datetime.now()
    period_days = config["对齐提醒周期_天"]
    
    for card in cards:
        last_verify = card.get("上次验证", card.get("创建时间", ""))
        if not last_verify:
            continue
            
        days = days_since(last_verify)
        confidence = card.get("置信度", "假设")
        scene = card.get("场景名", "未命名")
        
        # 铁律每两周检查，经验每月检查
        check_period = 14 if confidence == "铁律" else 30
        
        if days >= check_period:
            reminder = {
                "场景": scene,
                "置信度": confidence,
                "上次验证": last_verify,
                "天数": days,
                "建议": ""
            }
            
            if confidence == "铁律":
                reminder["建议"] = f"我们之前说好的这件事——{scene}，我现在还在这样做，你觉得对吗？"
            elif confidence == "经验":
                reminder["建议"] = f"上次你说过{scene}，最近情况有变化吗？"
            else:
                reminder["建议"] = f"之前我注意到{scene}，不知道还是这样吗？"
            
            reminders.append(reminder)
    
    # 输出提醒
    if reminders:
        print(f"\n📋 建议主动询问主人的内容（共{len(reminders)}条）：")
        for i, r in enumerate(reminders, 1):
            print(f"\n   {i}. {r['场景']} ({r['置信度']})")
            print(f"      上次验证：{r['天数']}天前")
            print(f"      💬 建议这样说：\"{r['建议']}\"")
    else:
        print("\n✅ 所有经验都是最近验证过的，不需要额外对齐")
    
    return reminders


def generate_report():
    """生成经验库报告"""
    print_header("📊 经验库完整报告")
    
    db = load_experience_db()
    profile = load_owner_profile()
    cards = db.get("cards", [])
    
    print(f"\n👤 主人：{profile.get('name', '未知')}")
    print(f"📅 报告生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"📦 经验库最后更新：{db.get('last_updated', '从未')}")
    
    if not cards:
        print("\n⚠️  经验库为空，还没有记录任何经验")
        return
    
    # 统计
    confidence_counts = {"假设": 0, "经验": 0, "铁律": 0}
    sources = {}
    scenes = []
    
    for card in cards:
        conf = card.get("置信度", "假设")
        confidence_counts[conf] = confidence_counts.get(conf, 0) + 1
        
        source = card.get("来源", "未知")
        sources[source] = sources.get(source, 0) + 1
        
        scenes.append(card.get("场景名", "未命名"))
    
    # 输出统计
    print(f"\n{'='*40}")
    print("📈 经验统计")
    print(f"{'='*40}")
    print(f"   总计：{len(cards)} 条经验")
    print(f"   ⭐ 假设：{confidence_counts['假设']} 条")
    print(f"   ⭐⭐ 经验：{confidence_counts['经验']} 条")
    print(f"   ⭐⭐⭐ 铁律：{confidence_counts['铁律']} 条")
    
    print(f"\n📚 学习来源：")
    for source, count in sorted(sources.items(), key=lambda x: -x[1]):
        print(f"   - {source}：{count}条")
    
    print(f"\n🏷️ 场景覆盖：")
    print(f"   {', '.join(scenes[:10])}")
    if len(scenes) > 10:
        print(f"   ...还有{len(scenes)-10}个场景")
    
    # 健康度摘要
    print(f"\n{'='*40}")
    print("💊 健康度摘要")
    print(f"{'='*40}")
    
    config = load_config()
    expired_count = 0
    for card in cards:
        last = card.get("上次验证", card.get("创建时间", ""))
        if last:
            days = days_since(last)
            if card.get("置信度") == "铁律" and days > config["铁律过期天数"]:
                expired_count += 1
            elif card.get("置信度") == "经验" and days > config["经验过期天数"]:
                expired_count += 1
    
    if expired_count == 0:
        print("   ✅ 经验库状态良好，没有过期的铁律/经验")
    else:
        print(f"   ⚠️  有 {expired_count} 条经验需要验证")
    
    # 高价值提醒
    iron_laws = [c for c in cards if c.get("置信度") == "铁律"]
    if iron_laws:
        print(f"\n⭐⭐⭐ 铁律提醒（共{len(iron_laws)}条）：")
        for law in iron_laws[:5]:
            print(f"   • {law.get('场景名', '未命名')}")


def init_data_dir():
    """初始化数据目录"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    # 如果文件不存在，创建示例数据
    if not OWNER_PROFILE_FILE.exists():
        sample_profile = {
            "name": "示例主人",
            "role": "示例角色",
            "created": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        }
        save_json(OWNER_PROFILE_FILE, sample_profile)
        print(f"✅ 已创建示例主人画像：{OWNER_PROFILE_FILE}")
    
    if not EXPERIENCE_DB_FILE.exists():
        sample_db = {
            "cards": [
                {
                    "场景名": "给外部合作方发邮件",
                    "置信度": "铁律",
                    "验证次数": 5,
                    "上次验证": (datetime.now() - timedelta(days=30)).isoformat(),
                    "创建时间": (datetime.now() - timedelta(days=90)).isoformat(),
                    "核心教训": "任何给外部人员的邮件都要CC主人",
                    "来源": "被提醒"
                },
                {
                    "场景名": "汇报工作进展",
                    "置信度": "经验",
                    "验证次数": 4,
                    "上次验证": (datetime.now() - timedelta(days=15)).isoformat(),
                    "创建时间": (datetime.now() - timedelta(days=60)).isoformat(),
                    "核心教训": "先说结论再说细节",
                    "来源": "被打断后纠正"
                },
                {
                    "场景名": "周五约会议",
                    "置信度": "假设",
                    "验证次数": 1,
                    "上次验证": (datetime.now() - timedelta(days=20)).isoformat(),
                    "创建时间": (datetime.now() - timedelta(days=20)).isoformat(),
                    "核心教训": "主人周五下午可能不想开会",
                    "来源": "一次观察"
                }
            ],
            "last_updated": datetime.now().isoformat()
        }
        save_json(EXPERIENCE_DB_FILE, sample_db)
        print(f"✅ 已创建示例经验库：{EXPERIENCE_DB_FILE}")
    
    if not CONFIG_FILE.exists():
        save_json(CONFIG_FILE, DEFAULT_CONFIG)
        print(f"✅ 已创建配置文件：{CONFIG_FILE}")


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print(__doc__)
        print("\n示例：")
        print("  python kaqiao.py check    # 检查健康度")
        print("  python kaqiao.py promote # 升级置信度")
        print("  python kaqiao.py align   # 生成对齐提醒")
        print("  python kaqiao.py report  # 生成报告")
        print("  python kaqiao.py all      # 执行全部")
        print("  python kaqiao.py init     # 初始化数据目录")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    # 初始化
    if command == "init":
        init_data_dir()
        return
    
    # 每次操作前初始化
    init_data_dir()
    
    if command == "check":
        check_health()
    elif command == "promote":
        promote_confidence()
    elif command == "align":
        generate_alignment_reminders()
    elif command == "report":
        generate_report()
    elif command == "all":
        check_health()
        promote_confidence()
        generate_alignment_reminders()
        generate_report()
    else:
        print(f"❓ 未知命令：{command}")
        print("可用命令：check, promote, align, report, all, init")
        sys.exit(1)


if __name__ == "__main__":
    main()
