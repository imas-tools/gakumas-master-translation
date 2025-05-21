import os
import yaml
import json
from typing import List
from yaml.reader import Reader


primary_key_rules = {
    "Achievement": [["id"], ["name", "description"]],
    # "AchievementProgress": [[], []],
    # "AppReview": [[], []],
    # "AssetDownload": [[], []],
    # "Bgm": [[], []],
    "Character": [["id"], ["lastName", "firstName"]],
    "CharacterAdv": [["characterId"], ["name", "regexp"]],
    # "CharacterColor": [[], []],
    "CharacterDearnessLevel": [["characterId", "dearnessLevel"], ["produceConditionDescription"]],
    # "CharacterDearnessStoryGashaCampaign": [[], []],
    "CharacterDetail": [["characterId", "type", "order"], ["content"]],
    # "CharacterProduceStory": [[], []],
    "CharacterPushMessage": [["characterId", "type", "number"], ["title", "message"]],
    # "CharacterTrueEndAchievement": [[], []],
    # "CharacterTrueEndBonus": [[], []],
    "CoinGashaButton": [["id"], ["name", "description"]],
    # "ConditionSet": [[], []],
    # "ConsumptionSet": [[], []],
    "Costume": [["id"], ["name", "description"]],
    # "CostumeColorGroup": [[], []],
    # "CostumeGroup": [[], []],
    "CostumeHead": [["id"], ["name", "description"]],
    # "CostumeMotion": [[], []],
    # "CostumePhotoGroup": [[], []],
    # "DearnessStoryCampaign": [[], []],
    # "DeepLinkTransition": [[], []],
    "EffectGroup": [["id"], ["name"]],
    "EventLabel": [["eventType"], ["name"]],
    # "EventStoryCampaign": [[], []],
    # "ExamInitialDeck": [[], []],
    # "ExamMotion": [[], []],
    # "ExamOutGameMotion": [[], []],
    # "ExamSetting": [[], []],
    # "ExamSimulation": [[], []],
    "ExchangeItemCategory": [["exchangeId", "number", "categoryType", "resourceType", "itemType"], ["name"]],
    "FeatureLock": [["tutorialType"], ["name", "description", "routeDescription"]],
    # "ForceAppVersion": [[], []],
    # "GashaAnimation": [[], []],
    # "GashaAnimationStep": [[], []],
    "GashaButton": [["id", "order"], ["name", "description"]],
    # "GuildDonationItem": [[], []],
    # "GuildReaction": [[], []],
    "GvgRaid": [["id", "order"], ["name"]],
    # "GvgRaidStageLoop": [[], []],
    "HelpCategory": [["id", "order"], ["name", "texts"]],
    "HelpContent": [["helpCategoryId", "id", "order"], ["name"]],
    # "HelpInfo": [[], []],
    # "HomeBoard": [[], []],
    # "HomeMonitor": [[], []],
    # "HomeMotion": [[], []],
    # "HomeTime": [[], []],
    "IdolCard": [["id"], ["name"]],
    # "IdolCardLevelLimit": [[], []],
    # "IdolCardLevelLimitProduceSkill": [[], []],
    # "IdolCardLevelLimitStatusUp": [[], []],
    # "IdolCardPiece": [[], []],
    # "IdolCardPieceQuantity": [[], []],
    # "IdolCardPotential": [[], []],
    # "IdolCardPotentialProduceSkill": [[], []],
    # "IdolCardSimulation": [[], []],
    # "IdolCardSkin": [[], []],
    # "IdolCardSkinSelectReward": [[], []],
    # "InvitationMission": [[], []],
    # "InvitationPointReward": [[], []],
    "Item": [["id"], ["name", "description", "acquisitionRouteDescription"]],
    # "JewelConsumptionCount": [[], []],
    # "LimitItem": [[], []],
    "Localization": [["id"], ["description"]],
    # "LoginBonusMotion": [[], []],
    "MainStoryChapter": [["mainStoryPartId", "id"], ["title", "description"]],
    "MainStoryPart": [["id"], ["title"]],
    "MainTask": [["mainTaskGroupId", "number"], ["title", "description", "homeDescription"]],
    "MainTaskGroup": [["id"], ["title"]],
    # "MainTaskIcon": [[], []],
    "Media": [["id"], ["name"]],
    "MeishiBaseAsset": [["id"], ["name"]],
    # "MeishiBaseColor": [[], []],
    "MeishiIllustrationAsset": [["id"], ["name"]],
    # "MeishiTextColor": [[], []],
    # "MemoryAbility": [[], []],
    # "MemoryExchangeItem": [[], []],
    # "MemoryExchangeItemQuantity": [[], []],
    "MemoryGift": [["id"], ["name"]],
    "MemoryTag": [["id"], ["defaultName"]],
    "Mission": [["id"], ["name"]],
    # "MissionDailyRelease": [[], []],
    # "MissionDailyReleaseGroup": [[], []],
    "MissionGroup": [["id"], ["name"]],
    "MissionPanelSheet": [["missionPanelSheetGroupId", "number"], ["name"]],
    "MissionPanelSheetGroup": [["id"], ["name"]],
    "MissionPass": [["id"], ["name", "description"]],
    "MissionPassPoint": [["id"], ["name"]],
    # "MissionPassProgress": [[], []],
    "MissionPoint": [["id"], ["name"]],
    # "MissionPointRewardSet": [[], []],
    # "MissionProgress": [[], []],
    # "Money": [[], []],
    "Music": [["id"], ["title", "displayTitle", "lyrics", "composer", "arranger"]],
    # "MusicHot": [[], []],
    # "MusicSinger": [[], []],
    "PhotoBackground": [["id"], ["name"]],
    # "PhotoFacialLookTarget": [[], []],
    "PhotoFacialMotionGroup": [["id", "number"], ["name"]],
    # "PhotoLookTargetVoiceCharacter": [[], []],
    "PhotoPose": [["id"], ["name"]],
    # "PhotoReactionVoiceGroup": [[], []],
    # "PhotoWaitVoiceCharacter": [[], []],
    # "PhotoWaitVoiceGroup": [[], []],
    "Produce": [["id"], ["name"]],
    "ProduceAdv": [["produceType", "type"], ["title"]],
    "ProduceCard": [["id", "upgradeCount", "produceDescriptions.produceDescriptionType", "produceDescriptions.examDescriptionType", "produceDescriptions.examEffectType",
                     "produceDescriptions.produceCardCategory", "produceDescriptions.produceCardMovePositionType", "produceDescriptions.produceStepType", "produceDescriptions.targetId",
                     ],
                    ["name", "produceDescriptions.text"]],  # 嵌套
    "ProduceCardCustomize": [["id", "customizeCount"], ["description"]],
    # "ProduceCardCustomizeRarityEvaluation": [[], []],
    # "ProduceCardGrowEffect": [[], []],
    # "ProduceCardRandomPool": [[], []],
    "ProduceCardSearch": [["id", 
                           "produceDescriptions.produceDescriptionType", "produceDescriptions.examDescriptionType", "produceDescriptions.examEffectType",
                           "produceDescriptions.produceCardCategory", "produceDescriptions.produceCardMovePositionType", "produceDescriptions.produceStepType", "produceDescriptions.targetId"],
                          ["produceDescriptions.text"]],  # 嵌套
    # "ProduceCardSimulation": [[], []],
    # "ProduceCardSimulationGroup": [[], []],
    # "ProduceCardStatusEffect": [[], []],
    "ProduceCardStatusEnchant": [["id", "produceDescriptions.produceDescriptionType", "produceDescriptions.examDescriptionType", "produceDescriptions.examEffectType",
                                  "produceDescriptions.produceCardCategory", "produceDescriptions.produceCardMovePositionType", "produceDescriptions.produceStepType", "produceDescriptions.targetId"],
                                 ["produceDescriptions.text"]],  # 嵌套
    "ProduceCardTag": [["id"], ["name"]],
    # "ProduceChallengeCharacter": [[], []],
    "ProduceChallengeSlot": [["id", "produceId", "number"], ["unlockDescription"]],
    # "ProduceCharacter": [[], []],
    "ProduceCharacterAdv": [["assetId"], ["title"]],
    "ProduceDescription": [["id"], ["name", "swapName"]],
    "ProduceDescriptionExamEffect": [["type"], ["name"]],
    "ProduceDescriptionLabel": [["id", 
                                 "produceDescriptions.produceDescriptionType", "produceDescriptions.examDescriptionType", "produceDescriptions.examEffectType",
                                 "produceDescriptions.produceCardCategory", "produceDescriptions.produceCardMovePositionType", "produceDescriptions.produceStepType", "produceDescriptions.targetId"], 
                                ["name", "produceDescriptions.text"]],
    "ProduceDescriptionProduceCardGrowEffect": [["type"], ["name"]],
    "ProduceDescriptionProduceCardGrowEffectType": [["type"], ["name", "produceCardCustomizeTemplate"]],
    # "ProduceDescriptionProduceCardMovePosition": [[], []],
    "ProduceDescriptionProduceEffect": [["type"], ["name"]],
    "ProduceDescriptionProduceEffectType": [["type"], ["name"]],
    "ProduceDescriptionProduceExamEffectType": [["type"], ["name", "swapName"]],
    "ProduceDescriptionProducePlan": [["type"], ["name"]],
    "ProduceDescriptionProducePlanType": [["type"], ["name"]],
    "ProduceDescriptionProduceStep": [["type"], ["name"]],
    "ProduceDescriptionSwap": [["id", "swapType"], ["text"]],
    "ProduceDrink": [["id", "produceDescriptions.produceDescriptionType", "produceDescriptions.examDescriptionType", "produceDescriptions.examEffectType",
                      "produceDescriptions.produceCardCategory", "produceDescriptions.produceCardMovePositionType", "produceDescriptions.produceStepType", "produceDescriptions.targetId"],
                     ["name", "produceDescriptions.text"]],  # 嵌套
    # "ProduceDrinkEffect": [[], []],
    # "ProduceEffect": [[], []],
    # "ProduceEffectIcon": [[], []],
    "ProduceEventCharacterGrowth": [["characterId", "number"], ["title", "description"]],
    # "ProduceEventSupportCard": [[], []],
    # "ProduceExamAutoCardSelectEvaluation": [[], []],
    # "ProduceExamAutoEvaluation": [[], []],
    # "ProduceExamAutoGrowEffectEvaluation": [[], []],
    # "ProduceExamAutoPlayCardEvaluation": [[], []],
    # "ProduceExamAutoResourceEvaluation": [[], []],
    # "ProduceExamAutoTriggerEvaluation": [[], []],
    # "ProduceExamBattleConfig": [[], []],
    # "ProduceExamBattleNpcGroup": [[], []],
    "ProduceExamBattleNpcMob": [["id"], ["name"]],
    # "ProduceExamBattleScoreConfig": [[], []],
    "ProduceExamEffect": [["id", "produceDescriptions.produceDescriptionType", "produceDescriptions.examDescriptionType", "produceDescriptions.examEffectType",
                          "produceDescriptions.produceCardCategory", "produceDescriptions.produceCardMovePositionType", "produceDescriptions.produceStepType", "produceDescriptions.targetId"],
                          ["produceDescriptions.text"]],  # 嵌套List Obj
    "ProduceExamGimmickEffectGroup": [["id", "priority", "produceDescriptions.produceDescriptionType", "produceDescriptions.examDescriptionType", "produceDescriptions.examEffectType",
                                      "produceDescriptions.produceCardCategory", "produceDescriptions.produceCardMovePositionType", "produceDescriptions.produceStepType", "produceDescriptions.targetId"],
                                      ["produceDescriptions.text"]],  # 嵌套List Obj
    "ProduceExamStatusEnchant": [["id", "produceDescriptions.produceDescriptionType", "produceDescriptions.examDescriptionType", "produceDescriptions.examEffectType",
                                  "produceDescriptions.produceCardCategory", "produceDescriptions.produceCardMovePositionType", "produceDescriptions.produceStepType", "produceDescriptions.targetId"],
                                 ["produceDescriptions.text"]],  # 嵌套List Obj
    "ProduceExamTrigger": [["id", "produceDescriptions.produceDescriptionType", "produceDescriptions.examDescriptionType", "produceDescriptions.examEffectType",
                            "produceDescriptions.produceCardCategory", "produceDescriptions.produceCardMovePositionType", "produceDescriptions.produceStepType", "produceDescriptions.targetId",
                            ],
                           ["produceDescriptions.text"]],  # 嵌套List Obj
    "ProduceGroup": [["id"], ["name", "description"]],
    # "ProduceGroupLiveCommon": [[], []],
    "ProduceHighScore": [["id"], ["name"]],
    "ProduceItem": [["id", "produceDescriptions.produceDescriptionType", "produceDescriptions.examDescriptionType", "produceDescriptions.examEffectType",
                     "produceDescriptions.produceCardCategory", "produceDescriptions.produceCardMovePositionType", "produceDescriptions.produceStepType", "produceDescriptions.targetId"],
                    ["name", "produceDescriptions.text"]],  # 嵌套List Obj
    # "ProduceItemChallengeGroup": [[], []],
    # "ProduceItemEffect": [[], []],
    # "ProduceItemSimulation": [[], []],
    # "ProduceItemSimulationGroup": [[], []],
    # "ProduceLive": [[], []],
    # "ProduceLiveCommon": [[], []],
    "ProduceNavigation": [["id", "number"], ["description"]],
    # "ProduceResultMotion": [[], []],
    # "ProducerLevel": [[], []],
    # "ProduceScheduleBackground": [[], []],
    # "ProduceScheduleMotion": [[], []],
    # "ProduceSetting": [[], []],
    "ProduceSkill": [["id", "level", "produceDescriptions.produceDescriptionType", "produceDescriptions.examDescriptionType", "produceDescriptions.examEffectType",
                      "produceDescriptions.produceCardCategory", "produceDescriptions.produceCardMovePositionType", "produceDescriptions.produceStepType", "produceDescriptions.targetId"],
                     ["produceDescriptions.text"]],  # 嵌套List Obj
    # "ProduceStartMotion": [[], []],
    # "ProduceStepAuditionCharacter": [[], []],
    # "ProduceStepAuditionDifficulty": [[], []],
    # "ProduceStepAuditionMotion": [[], []],
    "ProduceStepEventDetail": [["id", 
                                "produceDescriptions.produceDescriptionType", "produceDescriptions.examDescriptionType",
                                "produceDescriptions.examEffectType",
                                "produceDescriptions.produceCardCategory",
                                "produceDescriptions.produceCardMovePositionType",
                                "produceDescriptions.produceStepType", "produceDescriptions.targetId"
                                ],
                               ["produceDescriptions.text"]],  # 嵌套List Obj
    "ProduceStepEventSuggestion": [["id", "produceDescriptions.produceDescriptionType", "produceDescriptions.examDescriptionType", "produceDescriptions.examEffectType",
                                    "produceDescriptions.produceCardCategory", "produceDescriptions.produceCardMovePositionType", "produceDescriptions.produceStepType", "produceDescriptions.targetId",
                                    ],
                                   ["produceDescriptions.text"]],  # 嵌套List Obj
    # "ProduceStepFanPresentMotion": [[], []],
    "ProduceStepLesson": [["id"], ["name"]],
    # "ProduceStepLessonLevel": [[], []],
    # "ProduceStepSelfLesson": [[], []],
    # "ProduceStepSelfLessonMotion": [[], []],
    # "ProduceStepTransition": [[], []],
    "ProduceStory": [["id"], ["title", "produceEventHintProduceConditionDescriptions"]],
    # "ProduceStoryGroup": [[], []],
    # "ProduceTrigger": [[], []],
    # "ProduceWeekMotion": [[], []],
    # "PvpRateCommonProduceCard": [[], []],
    "PvpRateConfig": [["id"], ["description"]],
    # "PvpRateMotion": [[], []],
    # "PvpRateUnitSlotUnlock": [[], []],
    # "ResultGradePattern": [[], []],
    "Rule": [["type", "platformType", "number"], ["html"]],
    "SeminarExamTransition": [["examEffectType", "isLessonInt", "seminarExamId"], ["description", "seminarExamGroupName", "seminarExamName"]],
    "Setting": [["id"], ["initialUserName", "banWarningMessage"]],
    "Shop": [["id"], ["name"]],
    "ShopItem": [["id"], ["name"]],
    # "ShopProduct": [[], []],
    "Story": [["id"], ["title"]],
    "StoryEvent": [["id"], ["title"]],
    "StoryGroup": [["id"], ["title"]],
    "SupportCard": [["id", "upgradeProduceCardProduceDescriptions.produceDescriptionType", "upgradeProduceCardProduceDescriptions.examDescriptionType", "upgradeProduceCardProduceDescriptions.examEffectType", 
                     "upgradeProduceCardProduceDescriptions.produceCardGrowEffectType", "upgradeProduceCardProduceDescriptions.produceCardCategory", "upgradeProduceCardProduceDescriptions.produceCardMovePositionType", "upgradeProduceCardProduceDescriptions.produceStepType"],
                    ["name", "upgradeProduceCardProduceDescriptions.text"]],  # 嵌套List Obj
    # "SupportCardBonus": [[], []],
    "SupportCardFlavor": [["supportCardId", "number"], ["text"]],
    # "SupportCardLevel": [[], []],
    # "SupportCardLevelLimit": [[], []],
    "SupportCardProduceSkillFilter": [["id", "order"], ["title"]],
    # "SupportCardProduceSkillLevelAssist": [[], []],
    # "SupportCardProduceSkillLevelDance": [[], []],
    # "SupportCardProduceSkillLevelVisual": [[], []],
    # "SupportCardProduceSkillLevelVocal": [[], []],
    # "SupportCardSimulation": [[], []],
    # "SupportCardSimulationGroup": [[], []],
    "Terms": [["type"], ["name"]],
    "Tips": [["id"], ["title", "description"]],
    # "TitleAsset": [[], []],
    # "TitleVoice": [[], []],
    "Tower": [["id"], ["title"]],
    # "TowerLayer": [[], []],
    # "TowerLayerExam": [[], []],
    # "TowerLayerRank": [[], []],
    # "TowerTotalClearRankReward": [[], []],
    "Tutorial": [["tutorialType", "step", "subStep"], ["texts"]],
    # "TutorialCharacterVoice": [[], []],
    # "TutorialProduce": [[], []],
    "TutorialProduceStep": [["tutorialType", "stepNumber", "tutorialStep", "stepType"], ["name"]],
    # "Voice": [[], []],
    "VoiceGroup": [["id", "voiceAssetId"], ["title"]],
    "VoiceRoster": [["characterId", "assetId"], ["title"]],
    "Work": [["type"], ["name"]],
    # "WorkLevel": [[], []],
    # "WorkLevelReward": [[], []],
    # "WorkMotion": [[], []],
    # "WorkSkip": [[], []],
    # "WorkTime": [[], []]
}

TestMode = False

class CustomLoader(yaml.SafeLoader):
    def __init__(self, stream):
        # 重写初始化以支持特定的控制字符
        super().__init__(stream)

    def check_printable(self, data):
        """
        重写检查函数以允许不可打印字符（如 #x000b）
        """
        for char in data:
            if char == "\x0b":  # 允许垂直制表符
                continue
            if not super().check_printable(char):
                return False
        return True


def save_json(data: list, name: str):
    """
    主流程:
      1. 从 primary_key_rules[name] 中取出主键列表 (primary_keys) 和 非主键列表 (other_keys)。
      2. 仅保留这些字段（拆分 '.' 处理嵌套/数组）。
      3. 如果 TestMode = True，则对「非主键列表」中的字符串或字符串数组，追加 "TEST"。
    """
    if not data:
        return

    # 取出该 name 对应的规则
    rule = primary_key_rules.get(name)
    if not rule or len(rule) < 2:
        return

    primary_keys = rule[0]  # 第一列表 (主键)
    other_keys = rule[1]    # 第二列表 (可能追加 TEST)

    # 合并所有需要保留的字段（第一项 + 第二项）
    all_keys = primary_keys + other_keys

    processed_data = []
    for record in data:
        # 为当前 record 构造一个新对象，只包含需要的字段
        filtered_record = filter_record_fields(
            record,
            all_keys,
            primary_keys,
            other_keys
        )
        processed_data.append(filtered_record)

    # Make first data has all key
    # This can be removed when app can parse all key(also key type) properly.
    # Currently there is a bug on finding type and find local key from data
    # We must make first data has all key
    if not sort_records_fields(processed_data, all_keys):
        print(f"Failed to find super key object from {name}")

    # 生成最终的 JSON 结构
    result = {
        "rules": {
            "primaryKeys": primary_keys
        },
        "data": processed_data
    }

    # 写入 JSON 文件
    os.makedirs('./gakumasu-diff/json', exist_ok=True)
    with open(f'gakumasu-diff/json/{name}.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
    return f'gakumasu-diff/json/{name}.json'

def sort_records_fields(records: List[dict], field_paths: list):
    def hasPaths(record:dict, path:list):
        if not path:
            return False
        key = path[0]
        if not isinstance(record, dict) or key not in record:
            return False
        record_value = record[key]
        # No more sub object, we find all object from record by path 
        if len(path) == 1:
            return True
        
        # If there is obj use treversal to find value 
        if isinstance(record_value, dict):
            return hasPaths(record_value, path[1:])

        # When obj is list, check all element 
        if isinstance(record_value, list):
            for item in record_value:
                if isinstance(item, dict):
                    if hasPaths(item, path[1:]):
                        # it has all subkey
                        return True
        # Failed to find value by key
        return False
    for idx in range(len(records)):
        hasAllField = True
        for paths in field_paths:
            path = paths.split(".") 
            if not hasPaths(records[idx], path):
                hasAllField = False
                break
        if hasAllField:
            records.insert(0, records.pop(idx))
            return True
    return False

def filter_record_fields(record: dict, field_paths: list,
                         primary_keys: list, other_keys: list) -> dict:
    """
    给定一条原始记录 record，以及需要保留的字段路径列表 field_paths，
    返回一个只包含这些字段（及其嵌套结构）的新字典。
    若路径在 other_keys 且 TestMode = True，则对字符串或字符串列表添加 "TEST"。
    """
    new_record = {}
    for path_str in field_paths:
        path = path_str.split(".")  # "descriptions.type" -> ["descriptions", "type"]
        value = get_nested_value(record, path)
        if value is not None:
            # 若属于非主键列表 & TestMode = True，对字符串/字符串列表值追加 "TEST"
            if TestMode and (path_str in other_keys):
                value = transform_value_for_test_mode(value)
            # 将获取到的 value 合并到 new_record 中，保持相同嵌套结构
            merge_nested_value(new_record, path, value)
    return new_record


def get_nested_value(obj, path: list):
    """
    从 obj 中按照 path 依次深入，获取对应的 value。
    如果中间任何一步不存在，则返回 None。
    若遇到列表，则对列表中每个对象做同样的处理，并返回一个同样长度的列表。
    """
    if not path:
        return obj

    key = path[0]
    if not isinstance(obj, dict) or key not in obj:
        return None

    sub_obj = obj[key]
    # 如果仅剩最后一层路径，直接返回
    if len(path) == 1:
        return sub_obj

    # 如果是字典，继续深入
    if isinstance(sub_obj, dict):
        return get_nested_value(sub_obj, path[1:])

    # 如果是列表，则对每个元素做同样的处理，并返回一个列表
    if isinstance(sub_obj, list):
        results = []
        for item in sub_obj:
            if isinstance(item, dict):
                val = get_nested_value(item, path[1:])
                results.append(val)
            else:
                # 如果列表里不是 dict，就无法再深入，只能返回 None
                results.append(None)
        return results

    # 其他情况（数字、字符串等）无法继续深入
    return None


def merge_nested_value(target_dict: dict, path: list, value):
    """
    将 value 根据 path 的层级结构，合并到 target_dict 中。
    若某级是列表，则需要在 target_dict 中也构造出相同长度的列表，再逐项合并。
    """
    if not path:
        return

    key = path[0]

    # 如果只剩最后一级 key，则直接写入
    if len(path) == 1:
        target_dict[key] = value
        return

    # 如果 value 是个列表，说明当前层是列表，需要特殊处理
    if isinstance(value, list):
        # 如果 target_dict[key] 不存在或不是列表，则先初始化为空列表
        if key not in target_dict or not isinstance(target_dict[key], list):
            target_dict[key] = [None] * len(value)

        # 遍历 value 中的每一项，递归合并
        for i, v in enumerate(value):
            if v is None:
                continue  # 跳过 None
            # 如果 target_dict[key][i] 还没创建，就初始化为 dict
            if target_dict[key][i] is None:
                target_dict[key][i] = {}
            # 继续深入合并
            merge_nested_value(target_dict[key][i], path[1:], v)
        return

    # 否则，如果 target_dict[key] 不存在或不是字典，则初始化为字典
    if key not in target_dict or not isinstance(target_dict[key], dict):
        target_dict[key] = {}

    # 递归处理剩余路径
    merge_nested_value(target_dict[key], path[1:], value)


def transform_value_for_test_mode(value):
    """
    如果是字符串，追加 "TEST"。
    如果是字符串列表，为列表中的每项追加 "TEST"。
    其他类型不变。
    """
    if isinstance(value, str):
        return value + "TEST"
    if isinstance(value, list) and all(isinstance(v, str) for v in value):
        return [v + "TEST" for v in value]
    return value


# process_list = ["ProduceStepLesson", "SupportCardFlavor"]
process_list = None

def convert_yaml_types(folder_path="./gakumasu-diff/orig"):
    """
    遍历指定文件夹中的所有 YAML 文件，加载它们的内容，并打印每个文件的类型。
    自动替换 YAML 文件中的制表符为空格。
    """
    if not os.path.isdir(folder_path):
        print(f"路径 '{folder_path}' 不是一个有效的文件夹。")
        return

    for root, _, files in os.walk(folder_path):
        total = len(files)
        for n, file in enumerate(files):
            if file.endswith('.yaml'):
                if process_list:
                    if file[:-5] not in process_list:
                        continue

                file_path = os.path.join(root, file)
                # print(f"\"{file[:-5]}\": [[], []],")
                # continue

                print("Generating", file_path, f"to json. ({n}/{total})")
                try:
                    # 预处理文件：替换制表符为 4 个空格
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    # content = content.replace('\t', '    ')  # 替换制表符
                    content = content.replace(": \t", ": \"\t\"")  # 替换制表符

                    # 解析 YAML 内容
                    # data = yaml.safe_load(content)
                    data = yaml.load(content, CustomLoader)
                    save_json(data, file[:-5])

                    # print(f"文件: {file_path}")
                    # print(f"类型: {type(data)}\n")
                except Exception as e:
                    print(f"加载文件 {file_path} 时出错: {e}")


if __name__ == '__main__':
    convert_yaml_types()
