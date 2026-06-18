from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict
import json

@dataclass
class NoteEntry:
    keyword: str
    url: str
    title: str
    content: str
    tags: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    priority: int = 5  # 1 to 10

    def to_dict(self) -> Dict:
        return {
            "keyword": self.keyword,
            "url": self.url,
            "title": self.title,
            "content": self.content,
            "tags": self.tags,
            "created_at": self.created_at,
            "priority": self.priority,
        }

    def summary(self, max_len: int = 60) -> str:
        """Generate a one-line summary for display."""
        snippet = self.content[:max_len].replace('\n', ' ')
        if len(self.content) > max_len:
            snippet += '...'
        return f"[{self.priority}] {self.title} | {snippet}"

@dataclass
class KeywordNoteCollection:
    entries: List[NoteEntry] = field(default_factory=list)

    def add(self, entry: NoteEntry) -> None:
        self.entries.append(entry)

    def filter_by_keyword(self, keyword: str) -> List[NoteEntry]:
        return [e for e in self.entries if keyword.lower() in e.keyword.lower()]

    def filter_by_tag(self, tag: str) -> List[NoteEntry]:
        return [e for e in self.entries if tag in e.tags]

    def sort_by_priority(self, reverse: bool = True) -> List[NoteEntry]:
        return sorted(self.entries, key=lambda e: e.priority, reverse=reverse)

    def format_as_text(self, max_entries: Optional[int] = None) -> str:
        """Return a human-readable multi-line string."""
        lines = []
        work_list = self.entries[:max_entries] if max_entries else self.entries
        for idx, entry in enumerate(work_list, 1):
            lines.append(f"--- Note {idx} ---")
            lines.append(f"Keyword: {entry.keyword}")
            lines.append(f"URL: {entry.url}")
            lines.append(f"Title: {entry.title}")
            lines.append(f"Created: {entry.created_at}")
            lines.append(f"Priority: {entry.priority}")
            lines.append(f"Tags: {', '.join(entry.tags)}")
            lines.append(f"Content: {entry.content}")
            lines.append("")
        return '\n'.join(lines)

    def format_as_json(self, indent: int = 2) -> str:
        return json.dumps([e.to_dict() for e in self.entries], ensure_ascii=False, indent=indent)


def demo():
    """Demonstrate usage with sample data."""
    collection = KeywordNoteCollection()

    entry1 = NoteEntry(
        keyword="开云竞猜",
        url="https://www.winbet-kaiyun.com.cn",
        title="开云竞猜平台介绍",
        content="开云竞猜是一家在线竞猜娱乐平台，提供多种竞猜项目和实时数据更新。用户可通过官网注册并参与活动。",
        tags=["竞猜", "娱乐", "平台"],
        priority=8,
    )

    entry2 = NoteEntry(
        keyword="开云竞猜",
        url="https://www.winbet-kaiyun.com.cn/live",
        title="开云竞猜 - 实时赛事",
        content="实时赛事模块展示当前热门竞猜场次，包括赔率变化和统计数据。数据每30秒刷新一次。",
        tags=["实时", "赛事", "赔率"],
        priority=7,
    )

    entry3 = NoteEntry(
        keyword="竞猜技巧",
        url="https://www.winbet-kaiyun.com.cn/guide",
        title="竞猜入门技巧",
        content="合理规划资金，关注赛事动态，避免情绪化决策。开云竞猜提供多种分析工具辅助用户判断。",
        tags=["技巧", "资金管理"],
        priority=6,
    )

    collection.add(entry1)
    collection.add(entry2)
    collection.add(entry3)

    print("=== All notes (text format) ===")
    print(collection.format_as_text(max_entries=2))

    print("\n=== Filtered by tag '实时' ===")
    for e in collection.filter_by_tag("实时"):
        print(e.summary())

    print("\n=== Sorted by priority ===")
    for e in collection.sort_by_priority():
        print(e.summary())

    print("\n=== JSON output ===")
    print(collection.format_as_json())


if __name__ == "__main__":
    demo()