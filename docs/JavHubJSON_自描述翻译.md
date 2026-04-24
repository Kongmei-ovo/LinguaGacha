# JavHub JSON 自描述翻译格式

## 概述

LinguaGacha 支持一种**自描述翻译格式**，允许在 JSON 文件头部定义字段映射规则，无需修改代码即可适配任意 JSON 结构。

## 格式结构

```json
{
  "_src": "原文字段名",
  "_dst": "译文字段名",
  "_type": "category",
  "_version": "2",
  "data": {
    "ID_1": { "原文字段名": "原文内容", "译文字段名": "", ... },
    "ID_2": { "原文字段名": "原文内容", "译文字段名": "", ... }
  }
}
```

## 字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| `_src` | 是 | 原文字段名，指定从哪个字段读取原文 |
| `_dst` | 是 | 译文字段名，指定翻译结果写入哪个字段 |
| `data` | 否 | 数据容器 key。不填则直接遍历 JSON 顶层 |
| `_type` | 否 | 类型标识，仅用于记录，无实际作用 |
| `_version` | 否 | 版本号，仅用于记录，无实际作用 |

## 使用步骤

### 1. 准备原始文件

确保文件是以 `_src` 和 `_dst` 开头定义的格式。例如：

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

### 2. 创建 LinguaGacha 工程

1. 打开 LinguaGacha
2. 选择"新建工程"
3. 导入上述 JSON 文件
4. 设置原文语言（日语）和译文语言（中文）

### 3. 翻译

点击开始翻译，LinguaGacha 会：
1. 遍历 `data` 容器中的每个条目
2. 读取 `_src` 指定的字段（如 `name_ja`）作为原文
3. 翻译后将结果写入 `_dst` 指定的字段（如 `name_translated`）

### 4. 导出

导出时只需点击导出按钮，程序会根据 `_src`/`_dst` 配置自动匹配并写入翻译结果。

## 兼容旧格式

没有 `_src`/`_dst` 头部时，自动回退到默认字段：

```json
{
  "1071692": {
    "name_kanji": "松尾理恵",
    "name_translated": "松尾理恵-翻译V2"
  }
}
```

默认：`name_kanji` → `name_translated`

## 完整示例

### 日语名字翻译

```json
{
  "_src": "name_ja",
  "_dst": "name_translated",
  "data": {
    "1": { "name_ja": "田中太郎", "name_en": "Tanaka Taro", "name_translated": "" },
    "2": { "name_ja": "鈴木一郎", "name_en": "Suzuki Ichiro", "name_translated": "" }
  }
}
```

翻译后：

```json
{
  "_src": "name_ja",
  "_dst": "name_translated",
  "data": {
    "1": { "name_ja": "田中太郎", "name_en": "Tanaka Taro", "name_translated": "田中太郎" },
    "2": { "name_ja": "鈴木一郎", "name_en": "Suzuki Ichiro", "name_translated": "铃木一郎" }
  }
}
```

### 自定义字段名

```json
{
  "_src": "original_text",
  "_dst": "translated_text",
  "items": {
    "101": { "original_text": "Hello", "translated_text": "" },
    "102": { "original_text": "World", "translated_text": "" }
  }
}
```

这里使用 `items` 作为数据容器（不是 `data`）。

## 注意事项

1. **字段名区分大小写**：`name_ja` 和 `Name_JA` 是不同字段
2. **空值处理**：如果 `_dst` 字段已存在翻译内容，系统会跳过已有翻译
3. **嵌套结构**：`data`/`items` 等容器下的每个条目必须是 object 类型
