'''
Author: yyd
Date: 2026-04-06 14:42:46
LastEditTime: 2026-04-08 10:04:59
FilePath: \AI_Cunstom\main.py
Description: 将 rule 目录下的 skill 文件拷贝到目标项目的 .clinerules/ 目录
'''
import json
import shutil
from pathlib import Path

def clear_target_dir(target_dir: Path, expected_name: str) -> bool:
    """清理目标目录，返回是否成功"""
    if not target_dir.exists():
        return True
    if target_dir.name != expected_name:
        print(f"[失败] 安全校验未通过: 仅允许清理名为 {expected_name} 的目录，实际为 {target_dir.name}")
        return False
    
    existing_files = list(target_dir.glob("*"))
    if not existing_files:
        return True
    
    print(f"\n[警告] 目标目录 {target_dir} 已存在以下文件:")
    for f in existing_files:
        print(f"  - {f.name}")
    
    confirm = input("\n是否删除这些文件并继续? (y/n): ").strip().lower()
    if confirm == 'y':
        try:
            shutil.rmtree(target_dir)
            print(f"[清理] 已删除 {target_dir}")
            return True
        except Exception as e:
            print(f"[失败] 无法删除目录 {target_dir}: {e}")
            return False
    else:
        print("[取消] 用户取消操作")
        return False

def validate_project_config(project: dict, index: int) -> tuple[bool, str]:
    """校验单个项目配置是否有效"""
    path_value = project.get("path")
    if not isinstance(path_value, str) or not path_value.strip():
        return False, f"[跳过] target_projects[{index}] 缺少有效的 path"

    include_skills = project.get("include_skills", [])
    include_all = project.get("include_all", False)
    if not isinstance(include_all, bool):
        return False, f"[跳过] target_projects[{index}].include_all 必须是布尔值 true/false"
    if not isinstance(include_skills, list):
        return False, f"[跳过] target_projects[{index}].include_skills 必须是数组"

    return True, ""


def build_rules():
    base_path = Path(__file__).parent
    config_path = base_path / "config.json"
    
    if not config_path.exists():
        print("[错误] 找不到 config.json")
        return

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        print(f"[错误] config.json 格式错误: {e}")
        return
    except Exception as e:
        print(f"[错误] 无法读取 config.json: {e}")
        return

    rules_dir = config.get("rules_dir", ".clinerules")
    projects = config.get("target_projects", [])
    if not isinstance(rules_dir, str) or not rules_dir.strip():
        print("[错误] rules_dir 必须是非空字符串")
        return
    if not isinstance(projects, list):
        print("[错误] target_projects 必须是数组")
        return

    print(f"--- AI Rules 自动化构建开始 ---")

    for index, project in enumerate(projects):
        valid, message = validate_project_config(project, index)
        if not valid:
            print(message)
            continue

        project_path = Path(project.get("path"))
        skill_files = project.get("include_skills", [])
        include_all = project.get("include_all", False)
        
        if not project_path.exists():
            print(f"[跳过] 路径不存在: {project_path}")
            continue

        target_dir = project_path / rules_dir
        
        # 清理目标目录（需要用户确认）
        if not clear_target_dir(target_dir, rules_dir):
            continue
        
        # 创建目标目录
        try:
            target_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"[失败] 无法创建目录 {target_dir}: {e}")
            continue

        # include_skills 优先级高于 include_all
        if skill_files:
            # 模式1: 拷贝指定的 skill 文件
            for skill_name in skill_files:
                skill_path = base_path / "rule" / skill_name
                if skill_path.exists():
                    target_file = target_dir / skill_name
                    try:
                        shutil.copy2(skill_path, target_file)
                        print(f"[成功] {skill_name} -> {project_path.name}/{rules_dir}/")
                    except Exception as e:
                        print(f"[失败] 无法拷贝 {skill_name}: {e}")
                else:
                    print(f"[警告] 找不到 Skill 文件: {skill_name}")
        elif include_all:
            # 模式2: 拷贝 rule 目录下所有 md 文件
            rule_dir = base_path / "rule"
            if rule_dir.exists():
                md_files = list(rule_dir.glob("*.md"))
                if md_files:
                    for md_file in md_files:
                        target_file = target_dir / md_file.name
                        try:
                            shutil.copy2(md_file, target_file)
                            print(f"[成功] {md_file.name} -> {project_path.name}/{rules_dir}/")
                        except Exception as e:
                            print(f"[失败] 无法拷贝 {md_file.name}: {e}")
                else:
                    print(f"[警告] rule 目录下没有 md 文件")
            else:
                print(f"[警告] 找不到 rule 目录")
        else:
            print(f"[跳过] {project_path.name}: 未配置 include_skills 或 include_all")

if __name__ == "__main__":
    build_rules()