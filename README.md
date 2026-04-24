<div align=center><img src="https://github.com/user-attachments/assets/cdf990fb-cf03-4370-a402-844f87b2fab8" width="256px;"></div>
<div align=center><img src="https://img.shields.io/github/v/release/Kongmei-ovo/LinguaGacha"/>   <img src="https://img.shields.io/github/license/Kongmei-ovo/LinguaGacha"/></div>
<p align='center'>LinguaGacha Fork - 支持 JavHub JSON 格式</p>

---

## JavHub JSON 支持 (v0.60.1-javhub)

在原项目基础上新增 `.javhub.json` 文件格式支持，支持**自描述格式**，可通过文件头部配置灵活适配不同 JSON 结构。

### 自描述格式示例

```json
{
  "_src": "name_ja",
  "_dst": "name_translated",
  "data": {
    "79015": { "name_ja": "4K", "name_en": "4K", "name_translated": "" },
    "5031": { "name_ja": "シックスナイン", "name_en": "69", "name_translated": "" }
  }
}
```

**字段说明：**
- `_src`: 原文字段名
- `_dst`: 译文字段名
- `data`: 数据容器 key（不填则直接遍历顶层）

### 兼容旧格式

无头部时自动回退到 `name_kanji → name_translated`：

```json
{
  "1071692": {
    "name_kanji": "松尾理恵",
    "name_translated": "松尾理恵-翻译V2"
  }
}
```

---

## 安装

从 [Releases](https://github.com/Kongmei-ovo/LinguaGacha/releases) 下载对应平台版本。

## 开发

```bash
uv sync -U
uv run app.py
```

## 原项目

[LinguaGacha](https://github.com/neavo/LinguaGacha) - neavo 版
