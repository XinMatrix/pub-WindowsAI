import os
import shutil
import yaml


def create_yaml():
    current_script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(current_script_path)
    parent_dir = os.path.dirname(script_dir)
    train_path = os.path.join(parent_dir, 'data', 'images', 'train')
    val_path = os.path.join(parent_dir, 'data', 'images', 'val')
    test_path = os.path.join(parent_dir, 'data', 'images', 'test')
    categories = ['nose']
    output_path = '../config/train_config.yaml'  # 可以替换为你想要保存的路径
    data = {
        'train': train_path,
        'val': val_path,
        'test': test_path,
        'names': categories
    }
    with open(output_path, 'w') as file:
        yaml.safe_dump(data, file)


def reset_running_status():
    if not os.path.exists('data.yaml'):
        create_yaml()

    if os.path.exists('runs'):  # 默认删除旧的训练结果，可以注释以保存每次训练结果，但需注意修改 process_images 函数中的模型路径
        shutil.rmtree('runs')

    if os.path.exists('data/labels/train.cache'):
        os.remove('data/labels/train.cache')

    if os.path.exists('data/labels/val.cache'):
        os.remove('data/labels/val.cache')
