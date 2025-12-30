import json
import sys
import os
import re
import string

def path_normalize_for_pk(path_str: str) -> str:
    """
    将像 'produceDescriptions[0].produceDescriptionType'
    转换成 'produceDescriptions.produceDescriptionType'
    只去掉 [数字] 这一层，以便和 primaryKeys 匹配。
    """
    return re.sub(r"\[\d+\]", "", path_str)

'''
def check_need_export(v: str) -> bool:
    if not v:
        return False

    # 定义允许的字符集
    allowed_chars = string.ascii_letters + string.digits + string.punctuation + " "

    # 检查是否所有字符都在允许的字符集中
    for char in v:
        if char not in allowed_chars:
            return True

    return False
'''
def check_need_export(v: str) -> bool:
    if not v:
        return False
    return True


def collect_translatable_text(data_obj, primary_keys):
    """
    遍历 data_obj（即单条记录），收集需要翻译的文本信息。
    返回形如 { fullKey: textValue, ... } 的字典。
    """

    result = {}

    # 1) 把 primaryKeys 存到一个 set 里，后续好快速判断
    pk_set = set(primary_keys)

    # 2) 构建 baseKey (把所有主键值拼在一起)
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

    # 3) 递归遍历，找出非主键的、非空的string字段
    def traverse(obj, prefix=""):
        if isinstance(obj, dict):
            for k, v in obj.items():
                new_prefix = prefix + "." + k if prefix else k
                if isinstance(v, str):
                    # 如果字符串为空，则跳过
                    if not check_need_export(v):
                        continue
                    # 处理数组index => produceDescriptions[0].xxx -> produceDescriptions.xxx
                    normalized_path = path_normalize_for_pk(new_prefix)
                    # 如果它是 pk，就跳过
                    if normalized_path not in pk_set:
                        fullKey = baseKey + "|" + new_prefix
                        result[fullKey] = v
                elif isinstance(v, list):
                    if (len(v) > 0) and (not isinstance(v[0], str)):
                        traverse(v, new_prefix)
                    else:
                        new_v = "[LA_N_F]".join(v)
                        new_v = f"[LA_F]{new_v}"
                        # 如果字符串为空，则跳过
                        if not check_need_export(new_v):
                            continue
                        # 处理数组index => produceDescriptions[0].xxx -> produceDescriptions.xxx
                        normalized_path = path_normalize_for_pk(new_prefix)
                        # 如果它是 pk，就跳过
                        if normalized_path not in pk_set:
                            fullKey = baseKey + "|" + new_prefix
                            result[fullKey] = new_v

                elif isinstance(v, dict):
                    traverse(v, new_prefix)
        elif isinstance(obj, list):
            for idx, item in enumerate(obj):
                new_prefix = prefix + f"[{idx}]"
                if isinstance(item, (dict, list)):
                    traverse(item, new_prefix)

    traverse(data_obj)
    return result

def ex_main(input_json, output_json):
    if not os.path.isfile(input_json):
        print(f"找不到输入文件: {input_json}")
        sys.exit(1)

    with open(input_json, "r", encoding="utf-8") as f:
        root = json.load(f)

    if "rules" not in root or "primaryKeys" not in root["rules"]:
        print("缺少 rules.primaryKeys，可能不是预期结构")
        sys.exit(1)

    primary_keys = root["rules"]["primaryKeys"]
    if "data" not in root or not isinstance(root["data"], list):
        print("缺少 data 数组，可能不是预期结构")
        sys.exit(1)

    export_dict = {}
    for row in root["data"]:
        row_dict = collect_translatable_text(row, primary_keys)
        export_dict.update(row_dict)

    with open(output_json, "w", encoding="utf-8") as out:
        json.dump(export_dict, out, ensure_ascii=False, indent=2)

    print(f"导出完成: {output_json} (共 {len(export_dict)} 条)")

def main():
    orig_dir = input("原json文件夹: ") or "gakumasu-diff/json"
    if not os.path.isdir("./exports"):
        os.mkdir("./exports")

    for root, dirs, files in os.walk(orig_dir):
        for file in files:
            if file.endswith(".json"):
                input_path = os.path.join(root, file)
                output_path = os.path.join("./exports", file)
                ex_main(input_path, output_path)


if __name__ == "__main__":
    main()
