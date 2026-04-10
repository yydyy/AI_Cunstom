'''
Author: yyd
Date: 2026-04-06 14:42:46
LastEditTime: 2026-04-10 11:00:00
FilePath: \AI_Cunstom\main.py
Description: 将 rule 目录下的 skill 文件拷贝到目标项目的 AI 配置目录
支持多种 AI 格式: cline, kimi, cursor, windsurf, claude
每个格式可以有独立的项目和 skill 配置
'''
import json
import shutil
from pathlib import Path


def clear_target_dir(target_dir: Path, expected_name: str) -> bool:
    """清理目标目录，返回是否成功"""
    if not target_dir.exists():
        return True
    if target_dir.name != expected_name and target_dir.name not in expected_name:
        print(f"[失败] 安全校验未通过: 仅允许清理名为 {expected_name} 的目录，实际为 {target_dir.name}")
        return False
    
    existing_files = list(target_dir.glob("*"))
    if not existing_files:
        return True
    
    print(f"\n  [警告] 目标目录 {target_dir} 已存在以下文件:")
    for f in existing_files:
        print(f"    - {f.name}")
    
    confirm = input("\n  是否删除这些文件并继续? (y/n): ").strip().lower()
    if confirm == 'y':
        try:
            shutil.rmtree(target_dir)
            print(f"  [清理] 已删除 {target_dir}")
            return True
        except Exception as e:
            print(f"  [失败] 无法删除目录 {target_dir}: {e}")
            return False
    else:
        print("  [取消] 用户取消操作")
        return False


def clear_target_file(target_file: Path) -> bool:
    """清理目标文件，返回是否成功"""
    if not target_file.exists():
        return True
    
    print(f"\n  [警告] 目标文件 {target_file} 已存在")
    confirm = input("  是否覆盖该文件? (y/n): ").strip().lower()
    if confirm == 'y':
        try:
            target_file.unlink()
            print(f"  [清理] 已删除 {target_file}")
            return True
        except Exception as e:
            print(f"  [失败] 无法删除文件 {target_file}: {e}")
            return False
    else:
        print("  [取消] 用户取消操作")
        return False


def validate_project_config(project: dict, index: int, format_name: str) -> tuple[bool, str]:
    """校验单个项目配置是否有效"""
    path_value = project.get("path")
    if not isinstance(path_value, str) or not path_value.strip():
        return False, f"[跳过] {format_name} projects[{index}] 缺少有效的 path"

    include_skills = project.get("include_skills", [])
    include_all = project.get("include_all", False)
    if not isinstance(include_all, bool):
        return False, f"[跳过] {format_name} projects[{index}].include_all 必须是布尔值 true/false"
    if not isinstance(include_skills, list):
        return False, f"[跳过] {format_name} projects[{index}].include_skills 必须是数组"

    return True, ""


def get_skill_files(base_path: Path, skill_names: list, include_all: bool) -> list[Path]:
    """获取要处理的 skill 文件列表"""
    rule_dir = base_path / "rule"
    
    if not rule_dir.exists():
        return []
    
    if skill_names:
        # 模式1: 指定的 skill 文件
        files = []
        for skill_name in skill_names:
            skill_path = rule_dir / skill_name
            if skill_path.exists():
                files.append(skill_path)
            else:
                print(f"    [警告] 找不到 Skill 文件: {skill_name}")
        return files
    elif include_all:
        # 模式2: 所有 md 文件
        return list(rule_dir.glob("*.md"))
    
    return []


def format_skill_for_single_file(skill_content: str, skill_name: str) -> str:
    """将 skill 内容格式化为单个文件格式"""
    separator = f"\n\n{'='*60}\n"
    header = f"# Skill: {skill_name}\n"
    return separator + header + separator + "\n" + skill_content


def deploy_cline_format(skill_files: list[Path], target_dir: Path, rules_dir: str) -> None:
    """部署 Cline 格式: .clinerules/ 目录下直接放 .md 文件"""
    if not skill_files:
        print(f"    [跳过] 没有 skill 文件")
        return
    
    # 清理目标目录
    if not clear_target_dir(target_dir, rules_dir):
        return
    
    try:
        target_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"    [失败] 无法创建目录 {target_dir}: {e}")
        return
    
    for skill_path in skill_files:
        target_file = target_dir / skill_path.name
        try:
            shutil.copy2(skill_path, target_file)
            print(f"    [成功] {skill_path.name}")
        except Exception as e:
            print(f"    [失败] 无法拷贝 {skill_path.name}: {e}")


def deploy_kimi_format(skill_files: list[Path], target_dir: Path, rules_dir: str) -> None:
    """部署 Kimi 格式: .kimi/skills/<skill-name>/SKILL.md"""
    if not skill_files:
        print(f"    [跳过] 没有 skill 文件")
        return
    
    # Kimi 格式使用子目录结构
    skills_base_dir = target_dir
    
    # 清理并创建基础目录
    if skills_base_dir.exists():
        if not clear_target_dir(skills_base_dir, rules_dir.split('/')[-1]):
            return
    
    try:
        skills_base_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"    [失败] 无法创建目录 {skills_base_dir}: {e}")
        return
    
    for skill_path in skill_files:
        # 使用文件名（不含扩展名）作为 skill 名称
        skill_name = skill_path.stem
        skill_subdir = skills_base_dir / skill_name
        
        try:
            skill_subdir.mkdir(parents=True, exist_ok=True)
            target_file = skill_subdir / "SKILL.md"
            shutil.copy2(skill_path, target_file)
            print(f"    [成功] {skill_path.name} -> {skill_name}/SKILL.md")
        except Exception as e:
            print(f"    [失败] 无法部署 {skill_path.name}: {e}")


def deploy_cursor_format(skill_files: list[Path], target_dir: Path, rules_dir: str, file_extension: str = ".mdc") -> None:
    """部署 Cursor 格式: .cursor/rules/ 目录下放 .mdc 文件"""
    if not skill_files:
        print(f"    [跳过] 没有 skill 文件")
        return
    
    # 清理目标目录
    if not clear_target_dir(target_dir, rules_dir.split('/')[-1]):
        return
    
    try:
        target_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"    [失败] 无法创建目录 {target_dir}: {e}")
        return
    
    for skill_path in skill_files:
        # 更改扩展名为 .mdc
        target_name = skill_path.stem + file_extension
        target_file = target_dir / target_name
        
        # 添加 Cursor 格式的前置元数据
        content = skill_path.read_text(encoding='utf-8')
        if not content.startswith('---'):
            # 如果没有 frontmatter，添加默认的
            frontmatter = f"""---
description: Rules for {skill_path.stem}
globs: "*"
alwaysApply: true
---

"""
            content = frontmatter + content
        
        try:
            target_file.write_text(content, encoding='utf-8')
            print(f"    [成功] {skill_path.name} -> {target_name}")
        except Exception as e:
            print(f"    [失败] 无法写入 {target_name}: {e}")


def deploy_single_file_format(skill_files: list[Path], target_file: Path, format_name: str) -> None:
    """部署单个文件格式: 合并所有 skill 到一个文件 (.cursorrules, .windsurfrules, CLAUDE.md)"""
    if not skill_files:
        print(f"    [跳过] 没有 skill 文件")
        return
    
    # 清理目标文件
    if not clear_target_file(target_file):
        return
    
    try:
        # 创建父目录（如果需要）
        target_file.parent.mkdir(parents=True, exist_ok=True)
        
        # 合并所有 skill 文件
        combined_content = []
        combined_content.append(f"# AI Rules - 自动生成的配置\n")
        combined_content.append(f"# 包含 {len(skill_files)} 个 skill\n")
        combined_content.append("\n")
        
        for skill_path in skill_files:
            content = skill_path.read_text(encoding='utf-8')
            formatted = format_skill_for_single_file(content, skill_path.stem)
            combined_content.append(formatted)
        
        target_file.write_text('\n'.join(combined_content), encoding='utf-8')
        print(f"    [成功] 已生成 {target_file.name} ({len(skill_files)} 个 skill)")
    except Exception as e:
        print(f"    [失败] 无法写入文件 {target_file}: {e}")


def deploy_format(format_name: str, format_config: dict, skill_files: list[Path], project_path: Path) -> None:
    """根据格式配置部署 skill 文件"""
    output_dir = format_config.get("output_dir", "")
    output_file = format_config.get("output_file", "")
    file_extension = format_config.get("file_extension", ".mdc")
    
    if format_name == "cline":
        target_dir = project_path / output_dir
        deploy_cline_format(skill_files, target_dir, output_dir)
    
    elif format_name == "kimi":
        target_dir = project_path / output_dir
        deploy_kimi_format(skill_files, target_dir, output_dir)
    
    elif format_name == "cursor":
        target_dir = project_path / output_dir
        deploy_cursor_format(skill_files, target_dir, output_dir, file_extension)
    
    elif format_name == "cursor_single":
        target_file = project_path / output_file
        deploy_single_file_format(skill_files, target_file, "cursor_single")
    
    elif format_name == "windsurf":
        target_file = project_path / output_file
        deploy_single_file_format(skill_files, target_file, "windsurf")
    
    elif format_name == "claude":
        target_file = project_path / output_file
        deploy_single_file_format(skill_files, target_file, "claude")
    
    else:
        print(f"    [警告] 未知的格式: {format_name}")


def process_format(format_name: str, format_config: dict, base_path: Path, global_projects: list) -> None:
    """处理单个格式的部署"""
    print(f"\n[{format_name.upper()}]")
    
    # 获取该格式的项目配置，如果没有则使用全局配置
    projects = format_config.get("projects", global_projects)
    
    if not projects:
        print("  [跳过] 未配置项目")
        return
    
    if not isinstance(projects, list):
        print("  [错误] projects 必须是数组")
        return
    
    for index, project in enumerate(projects):
        valid, message = validate_project_config(project, index, format_name)
        if not valid:
            print(f"  {message}")
            continue

        project_path = Path(project.get("path"))
        skill_names = project.get("include_skills", [])
        include_all = project.get("include_all", False)
        
        if not project_path.exists():
            print(f"  [跳过] 路径不存在: {project_path}")
            continue

        print(f"\n  [项目] {project_path.name}")
        
        # 获取 skill 文件列表
        skill_files = get_skill_files(base_path, skill_names, include_all)
        
        if not skill_files and not skill_names and not include_all:
            print(f"    [跳过] 未配置 include_skills 或 include_all")
            continue
        
        if not skill_files:
            print(f"    [跳过] 没有可用的 skill 文件")
            continue

        # 部署到目标路径
        deploy_format(format_name, format_config, skill_files, project_path)


def migrate_old_config(config: dict) -> dict:
    """将旧配置格式迁移到新格式"""
    # 检查是否包含旧格式配置
    if "rules_dir" in config and "target_projects" in config:
        print("[信息] 检测到旧配置格式，自动迁移中...")
        
        old_rules_dir = config.get("rules_dir", ".clinerules")
        old_projects = config.get("target_projects", [])
        
        # 创建新的 formats 配置
        config["formats"] = {
            "cline": {
                "enabled": True,
                "output_dir": old_rules_dir,
                "projects": old_projects
            },
            "kimi": {
                "enabled": False,
                "output_dir": ".kimi/skills",
                "projects": []
            },
            "cursor": {
                "enabled": False,
                "output_dir": ".cursor/rules",
                "file_extension": ".mdc",
                "projects": []
            },
            "cursor_single": {
                "enabled": False,
                "output_file": ".cursorrules",
                "projects": []
            },
            "windsurf": {
                "enabled": False,
                "output_file": ".windsurfrules",
                "projects": []
            },
            "claude": {
                "enabled": False,
                "output_file": "CLAUDE.md",
                "projects": []
            }
        }
    
    return config


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

    # 迁移旧配置
    config = migrate_old_config(config)

    formats = config.get("formats", {})
    global_projects = config.get("target_projects", [])
    
    if not isinstance(formats, dict):
        print("[错误] formats 必须是对象")
        return

    # 过滤启用的格式
    enabled_formats = {
        name: cfg for name, cfg in formats.items()
        if isinstance(cfg, dict) and cfg.get("enabled", False)
    }
    
    if not enabled_formats:
        print("[警告] 没有启用的格式配置，请检查 config.json")
        return

    print("=== AI Rules 自动化构建开始 ===")
    print(f"启用的格式: {', '.join(enabled_formats.keys())}")

    # 处理每个启用的格式
    for format_name, format_config in enabled_formats.items():
        process_format(format_name, format_config, base_path, global_projects)

    print("\n=== AI Rules 自动化构建完成 ===")


if __name__ == "__main__":
    build_rules()
