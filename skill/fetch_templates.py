#!/usr/bin/env python3
"""
下载 AI-Animation-Skill 模板资产
来源: github.com/Unclecheng-li/AI-Animation-Skill (MIT License)

使用方法:
    python skill/fetch_templates.py

会把 40 个 HTML 模板下载到 skill/templates/ 目录下。
"""

import urllib.request
import urllib.error
from pathlib import Path
import time

# 模板 URL 列表（MIT License — AI-Animation-Skill）
BASE_URL = "https://raw.githubusercontent.com/Unclecheng-li/AI-Animation-Skill/main/assets/templates"

TEMPLATES = {
    # PPT Level2 系列（26个）
    "ppt-level2/series1-1.html": f"{BASE_URL}/PPT%20Template-level2/1.html",
    "ppt-level2/series2-1.html": f"{BASE_URL}/PPT%20Template-level2/2.html",
    "ppt-level2/series3-1.html": f"{BASE_URL}/PPT%20Template-level2/3-1.html",
    "ppt-level2/series3-2.html": f"{BASE_URL}/PPT%20Template-level2/3-2.html",
    "ppt-level2/series3-3.html": f"{BASE_URL}/PPT%20Template-level2/3-3.html",
    "ppt-level2/series4-1.html": f"{BASE_URL}/PPT%20Template-level2/4-1.html",
    "ppt-level2/series4-2.html": f"{BASE_URL}/PPT%20Template-level2/4-2.html",
    "ppt-level2/series4-3.html": f"{BASE_URL}/PPT%20Template-level2/4-3.html",
    "ppt-level2/series5-1.html": f"{BASE_URL}/PPT%20Template-level2/5-1.html",
    "ppt-level2/series5-2.html": f"{BASE_URL}/PPT%20Template-level2/5-2.html",
    "ppt-level2/series5-3.html": f"{BASE_URL}/PPT%20Template-level2/5-3.html",
    "ppt-level2/series5-4.html": f"{BASE_URL}/PPT%20Template-level2/5-4.html",
    "ppt-level2/series6-1.html": f"{BASE_URL}/PPT%20Template-level2/6-1.html",
    "ppt-level2/series6-2.html": f"{BASE_URL}/PPT%20Template-level2/6-2.html",
    "ppt-level2/series6-3.html": f"{BASE_URL}/PPT%20Template-level2/6-3.html",
    "ppt-level2/series6-4.html": f"{BASE_URL}/PPT%20Template-level2/6-4.html",
    "ppt-level2/series7-1.html": f"{BASE_URL}/PPT%20Template-level2/7-1.html",
    "ppt-level2/series7-2.html": f"{BASE_URL}/PPT%20Template-level2/7-2.html",
    "ppt-level2/series7-3.html": f"{BASE_URL}/PPT%20Template-level2/7-3.html",
    "ppt-level2/series7-4.html": f"{BASE_URL}/PPT%20Template-level2/7-4.html",
    "ppt-level2/series8-1.html": f"{BASE_URL}/PPT%20Template-level2/8-1.html",
    "ppt-level2/series8-2.html": f"{BASE_URL}/PPT%20Template-level2/8-2.html",
    "ppt-level2/series8-3.html": f"{BASE_URL}/PPT%20Template-level2/8-3.html",
    "ppt-level2/series9-1.html": f"{BASE_URL}/PPT%20Template-level2/9-1.html",
    "ppt-level2/series9-2.html": f"{BASE_URL}/PPT%20Template-level2/9-2.html",
    "ppt-level2/series9-3.html": f"{BASE_URL}/PPT%20Template-level2/9-3.html",
    # PPT 基础（4个）
    "ppt-basic/ppt-gen-1.html": f"{BASE_URL}/PPT/PPT-Generate-1.html",
    "ppt-basic/ppt-gen-2.html": f"{BASE_URL}/PPT/PPT-Generate-2.html",
    "ppt-basic/ppt-gen-3.html": f"{BASE_URL}/PPT/PPT-Generate-3.html",
    "ppt-basic/ppt-gen-4.html": f"{BASE_URL}/PPT/PPT-Generate-4.html",
    # Animation 流程图（14个）
    "animation/rnn-2.html": f"{BASE_URL}/Animation/RNN-2.html",
    "animation/rnn-3.html": f"{BASE_URL}/Animation/RNN-3.html",
    "animation/rnn-4.html": f"{BASE_URL}/Animation/RNN-4.html",
    "animation/rnn-5.html": f"{BASE_URL}/Animation/RNN-5.html",
    "animation/rnn-6.html": f"{BASE_URL}/Animation/RNN-6.html",
    "animation/rnn-7.html": f"{BASE_URL}/Animation/RNN-7.html",
    "animation/lstm-1.html": f"{BASE_URL}/Animation/LSTM-1.html",
    "animation/onehot.html": f"{BASE_URL}/Animation/onehot.html",
    "animation/onehot-drawback.html": f"{BASE_URL}/Animation/onehot-drawback.html",
    "animation/word2vec-1.html": f"{BASE_URL}/Animation/word2vec-1.html",
    "animation/comprehension.html": f"{BASE_URL}/Animation/Comprehension.html",
    "animation/gpu.html": f"{BASE_URL}/Animation/GPU.html",
    "animation/cross-modal-2.html": f"{BASE_URL}/Animation/Cross-modal%20disentanglement%20-%202.html",
    "animation/fatal-flaw-dnn.html": f"{BASE_URL}/Animation/The%20fatal%20flaw%20of%20DNN.html",
}


def download_all():
    """下载所有模板。"""
    script_dir = Path(__file__).parent.parent
    templates_dir = script_dir / "templates"
    templates_dir.mkdir(exist_ok=True)

    success = 0
    failed = []

    for rel_path, url in TEMPLATES.items():
        dest = templates_dir / rel_path
        dest.parent.mkdir(parents=True, exist_ok=True)

        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "Mozilla/5.0"}
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                content = resp.read()
                dest.write_bytes(content)
                success += 1
                print(f"  ✅ {rel_path} ({len(content):,} bytes)")
        except Exception as e:
            failed.append((rel_path, str(e)))
            print(f"  ❌ {rel_path}: {e}")
            time.sleep(1)  # be polite

    print(f"\n结果: {success}/{len(TEMPLATES)} 成功, {len(failed)} 失败")
    if failed:
        print("失败的文件:")
        for rel_path, err in failed:
            print(f"  - {rel_path}: {err}")
        print("\n网络不通时稍后重试: python skill/fetch_templates.py")


if __name__ == "__main__":
    print("开始下载 AI-Animation-Skill 模板...")
    download_all()
