import os

from base.Base import Base
from model.Item import Item
from module.Config import Config
from module.Data.DataManager import DataManager
from module.Text.TextHelper import TextHelper
from module.Utils.JSONTool import JSONTool


class JavHubJSON(Base):
    # JavHub 导出文件格式:
    # {
    #     "1071692": {
    #         "id": 1071692,
    #         "name_kanji": "松尾理恵",
    #         "name_romaji": "Rie Matsuo",
    #         "name_kana": "まつおりえ",
    #         "name_translated": "松尾理恵-翻译V2"
    #     },
    #     ...
    # }
    #
    # 翻译字段: name_kanji -> name_translated

    def __init__(self, config: Config) -> None:
        super().__init__()

        # 初始化
        self.config = config

    # 读取
    def read_from_path(self, abs_paths: list[str], input_path: str) -> list[Item]:
        items: list[Item] = []
        for abs_path in abs_paths:
            # 获取相对路径
            rel_path = os.path.relpath(abs_path, input_path)

            # 数据处理
            with open(abs_path, "rb") as reader:
                items.extend(self.read_from_stream(reader.read(), rel_path))

        return items

    # 从流读取
    def read_from_stream(self, content: bytes, rel_path: str) -> list[Item]:
        items: list[Item] = []

        # 获取文件编码
        encoding = TextHelper.get_encoding(content=content, add_sig_to_utf8=True)

        # 数据处理
        if encoding.lower() in ("utf-8", "utf-8-sig"):
            json_data: dict = JSONTool.loads(content)
        else:
            json_data = JSONTool.loads(content.decode(encoding))

        # 格式校验: 必须是 dict
        if not isinstance(json_data, dict):
            return items

        # 读取数据: 遍历每个 ID 条目
        for entry_id, entry in json_data.items():
            if not isinstance(entry, dict):
                continue

            name_kanji = entry.get("name_kanji", "")
            name_translated = entry.get("name_translated", "")

            # name_kanji 为空则跳过
            if not name_kanji:
                continue

            # 判断是否已翻译
            if name_translated and name_translated != name_kanji:
                items.append(
                    Item.from_dict(
                        {
                            "src": name_kanji,
                            "dst": name_translated,
                            "row": len(items),
                            "file_type": Item.FileType.JAVHUBJSON,
                            "file_path": rel_path,
                            "status": Base.ProjectStatus.PROCESSED_IN_PAST,
                        }
                    )
                )
            else:
                items.append(
                    Item.from_dict(
                        {
                            "src": name_kanji,
                            "dst": "",
                            "row": len(items),
                            "file_type": Item.FileType.JAVHUBJSON,
                            "file_path": rel_path,
                            "status": Base.ProjectStatus.NONE,
                        }
                    )
                )

        return items

    # 写入
    def write_to_path(self, items: list[Item]) -> None:
        # 获取输出目录
        dm = DataManager.get()
        output_path = dm.get_translated_path()

        target = [
            item for item in items if item.get_file_type() == Item.FileType.JAVHUBJSON
        ]

        group: dict[str, list[Item]] = {}
        for item in target:
            group.setdefault(item.get_file_path(), []).append(item)

        for rel_path, group_items in group.items():
            # 按行号排序
            sorted_items = sorted(group_items, key=lambda x: x.get_row())

            # 从数据库读取原始文件（assets 表）
            raw_content = dm.get_asset_decompressed(rel_path)

            if raw_content is None:
                continue

            # 解析原始 JSON
            encoding = TextHelper.get_encoding(content=raw_content, add_sig_to_utf8=True)
            enc_str = raw_content if encoding.lower() in ("utf-8", "utf-8-sig") else raw_content.decode(encoding)
            original_data = JSONTool.loads(enc_str)

            # 用 src (name_kanji) 匹配原文并更新翻译
            for item in sorted_items:
                src = item.get_src()
                dst = item.get_effective_dst()
                for entry_id, entry in original_data.items():
                    if isinstance(entry, dict) and entry.get("name_kanji") == src:
                        entry["name_translated"] = dst

            # 写入输出目录
            abs_path = os.path.join(output_path, rel_path)
            os.makedirs(os.path.dirname(abs_path), exist_ok=True)
            JSONTool.save_file(abs_path, original_data, indent=4)
