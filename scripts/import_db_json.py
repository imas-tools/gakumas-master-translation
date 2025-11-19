import json
import sys
import os

# 特殊规则，用于处理某些字段的特殊情况
# 格式为：{"文件名": {"字段名": {"规则"} }}，可以在此添加更多特殊处理的规则
special_rules = {
    "ProduceStory.json": {
        "produceEventHintProduceConditionDescriptions": {
            "is_empty": True,  # 如果该字段为单一空字符串数组，将其替换为空数组
        }
    },
    "Tutorial.json": {
        "texts": {
            "is_empty": True,  # 如果该字段为单一空字符串数组，将其替换为空数组
        }
    },
    "ConditionSet..json": {
        "description": {
            "is_empty": True,  # 如果该字段为单一空字符串数组，将其替换为空数组
        }
    },
    "IdolCardSkin.json": {
        "name": {
            "is_empty": True,  # 如果该字段为单一空字符串数组，将其替换为空数组
        }
    },
    # 以后可以继续在这里添加其他文件和字段的特殊规则
}

def fill_back_translations(data_obj, primary_keys, trans_map, filename=None):
    """
    data_obj 是原本地化数据的一条记录；
    trans_map 是第三方软件翻译后的 { fullKey: translatedValue }
    根据 baseKey(由主键拼成) + 路径 进行匹配，将翻译填充回 data_obj。
    filename 用于特殊处理某些文件的特定逻辑。
    """

    # 先拼出 baseKey
    pk_parts = []
    for pk in primary_keys:
        if "." not in pk:
            val = data_obj.get(pk, "")
            pk_parts.append(str(val))
        else:
            top_level, sub_field = pk.split(".", 1)
            top_val = data_obj.get(top_level, None)
            if isinstance(top_val, list) and len(top_val) > 0 and isinstance(top_val[0], dict):
                sub_val = top_val[0].get(sub_field, "")
                pk_parts.append(str(sub_val))
            elif isinstance(top_val, dict):
                sub_val = top_val.get(sub_field, "")
                pk_parts.append(str(sub_val))
            else:
                pk_parts.append("")
    baseKey = "|".join(pk_parts)

    # 遍历 data_obj，若找到 key= baseKey|xxx，替换其内容
    def traverse(obj, prefix=""):
        if isinstance(obj, dict):
            for k, v in obj.items():
                new_prefix = prefix + "." + k if prefix else k
                if isinstance(v, str):
                    fullKey = baseKey + "|" + new_prefix
                    if fullKey in trans_map:
                        obj[k] = trans_map[fullKey]
                elif isinstance(v, list):
                    fullKey = baseKey + "|" + new_prefix
                    if fullKey in trans_map:
                        trans_data = trans_map[fullKey]
                        if trans_data.startswith("[LA_F]"):
                            remaining = trans_data[len("[LA_F]"):]
                            if remaining == "":
                                # 空数组的情况：[LA_F] 后面没有内容
                                obj[k] = []
                            else:
                                list_data = remaining.split("[LA_N_F]")
                                # 特殊处理：检查是否需要处理空数组的情况
                                if filename in special_rules and k in special_rules[filename]:
                                    rule = special_rules[filename][k]
                                    if "is_empty" in rule and len(list_data) == 1 and list_data[0] == "":
                                        obj[k] = []  # 根据规则清空数组
                                    else:
                                        obj[k] = list_data  # 正常的数组数据
                                else:
                                    obj[k] = list_data
                        else:
                            traverse(v, new_prefix)
                    else:
                        traverse(v, new_prefix)
                elif isinstance(v, dict):
                    traverse(v, new_prefix)
        elif isinstance(obj, list):
            for idx, item in enumerate(obj):
                new_prefix = prefix + f"[{idx}]"
                if isinstance(item, dict) or isinstance(item, list):
                    traverse(item, new_prefix)

    traverse(data_obj)


def import_main(base_json, translated_json, output_json):
    if not os.path.isfile(base_json):
        print(f"找不到 base 文件: {base_json}")
        sys.exit(1)
    if not os.path.isfile(translated_json):
        print(f"找不到翻译文件: {translated_json}")
        sys.exit(1)

    with open(base_json, "r", encoding="utf-8") as f1:
        root = json.load(f1)

    with open(translated_json, "r", encoding="utf-8") as f2:
        trans_map = json.load(f2)  # {"key": "translated text", ...}

    if "rules" not in root or "primaryKeys" not in root["rules"]:
        print("缺少 rules.primaryKeys，可能不是预期结构")
        sys.exit(1)

    primary_keys = root["rules"]["primaryKeys"]
    if "data" not in root or not isinstance(root["data"], list):
        print("缺少 data 数组，可能不是预期结构")
        sys.exit(1)

    # 从输出文件路径中提取文件名用于特殊处理
    filename = os.path.basename(output_json)

    # 遍历 data 数组，一条一条地把翻译填回去
    for row in root["data"]:
        fill_back_translations(row, primary_keys, trans_map, filename)

    # 写出新的 json
    with open(output_json, "w", encoding="utf-8") as out:
        json.dump(root, out, ensure_ascii=False, indent=2)

    print(f"合并完成: {output_json}")


def main(base_dir, translated_dir, output_dir="merged"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for root, dirs, files in os.walk(translated_dir):
        for file in files:
            if file.endswith(".json"):
                translated_json = os.path.join(root, file)
                base_json = os.path.join(base_dir, file)
                output_json = os.path.join(output_dir, file)
                import_main(base_json, translated_json, output_json)


if __name__ == "__main__":
    main(
        base_dir=input("源json文件夹: ") or "gakumasu-diff/json",
        translated_dir=input("预翻译完成文件夹: ") or "pretranslate_todo/translated_out"
    )
