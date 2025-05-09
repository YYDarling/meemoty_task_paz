# === utils.py ===
import pandas as pd
import random
import os
from config import resource_path 
from collections import defaultdict


def save_results(results, output_base, subject_id, session_num, cfg):
    subj_folder = os.path.join(output_base, f"{subject_id}")
    if not os.path.exists(subj_folder):
        os.makedirs(subj_folder)
    filepath = os.path.join(subj_folder, f"session_{session_num}_{cfg['mode']}.csv")


    pd.DataFrame(results).to_csv(filepath, index=False)


def generate_trials(cfg):
    base = resource_path(cfg['image_folder']) 

    # === 1. Load and check
    # === 1. OLD: 随机选出 8 张 identical 图，每张重复两次
    identical_all = sorted([
        os.path.join(base, "identical_pairs", f)
        for f in os.listdir(os.path.join(base, "identical_pairs"))
        if f.startswith("id_") and f.lower().endswith(('.jpg', '.png'))
    ])
    assert len(identical_all) >= cfg['num_old_pairs'], f"Not enough identical images — need at least {cfg['num_old_pairs']}"
    identical_imgs = random.sample(identical_all, cfg['num_old_pairs'])



    # === 2. SIMILAR: 自动识别 _1 / _2 命名成对，并随机选 8 对
    similar_folder = os.path.join(base, "similar_pairs")
    similar_files = [f for f in os.listdir(similar_folder) if f.startswith("sm_") and f.lower().endswith(('.jpg', '.png'))]

    pair_dict = defaultdict(list)
    for fname in similar_files:
        if "_1." in fname or "_2." in fname:
            base_name = fname.rsplit("_", 1)[0]
            pair_dict[base_name].append(os.path.join(similar_folder, fname))

    pair_list = [v for v in pair_dict.values() if len(v) == 2]
    assert len(pair_list) >= cfg['num_similar_pairs'], f"Not enough similar image pairs (found {len(pair_list)} pairs)"
    selected_similar_pairs = random.sample(pair_list, cfg['num_similar_pairs'])
    

    # === 3. NOVEL: 随机选出 44 张 new 图片
    novel_folder = os.path.join(base, "novel_items")
    novel_imgs_all = sorted([
        os.path.join(novel_folder, f)
        for f in os.listdir(novel_folder)
        if f.startswith("un_") and f.lower().endswith(('.jpg', '.png'))
    ])
    assert len(novel_imgs_all) >= cfg['num_new_items'], f"Not enough novel images (need {cfg['num_new_items']})"
    novel_imgs = random.sample(novel_imgs_all, cfg['num_new_items'])

 
    # === 4. 初始化试次槽位
    total_trials = cfg['num_old_pairs'] * 2 + cfg['num_similar_pairs'] * 2 + cfg['num_new_items']
    trial_slots = [None] * total_trials
    occupied = set()

    def place_pair(first_item, second_item):
        for _ in range(1000):
            start = random.randint(0, total_trials - cfg['max_separation'] - 1)
            offset = random.randint(cfg['min_separation'], cfg['max_separation'])
            end = start + offset
            if end >= total_trials:
                continue
            if start not in occupied and end not in occupied:
                trial_slots[start] = first_item
                trial_slots[end] = second_item
                occupied.update([start, end])
                return
        raise RuntimeError("Failed to place pair after many attempts.")

        # === 5. 插入 identical 试次
    for img in identical_imgs:
        item1 = {'img': img, 'type': 'old', 'label': 'N'}
        item2 = {'img': img, 'type': 'old', 'label': 'O'}
        place_pair(item1, item2)

    # === 6. 插入 similar 试次
    for pair in selected_similar_pairs:
        pair = sorted(pair)
        item1 = {'img': pair[0], 'type': 'similar', 'label': 'N'}
        item2 = {'img': pair[1], 'type': 'similar', 'label': 'M'}
        place_pair(item1, item2)

    # === 7. 插入 novel 试次
    new_items = [{'img': img, 'type': 'new', 'label': 'N'} for img in novel_imgs]
    new_slots = [i for i in range(total_trials) if i not in occupied]
    random.shuffle(new_slots)

    for i, slot in enumerate(new_slots):
        trial_slots[slot] = new_items[i]

    # === Debug log: 打印预览信息
    print("\n📋 Trial Preview (Index | Type | Label | Image):")
    for idx, t in enumerate(trial_slots):
        basename = os.path.basename(t['img'])
        print(f"{idx+1:02d}: {t['type'].upper():<8} | {t['label']} | {basename}")


    return trial_slots

