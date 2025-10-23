from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg
from PIL import Image
import time
import json

# save_config
def save_config(model, config_dict):
    config_json = json.dumps(config_dict)
    print(config_json)
    # lưu config_json vào file config.json
    with open(f'config_{model}.json', 'w') as f:
        f.write(config_json)
    return config_json

# đo thời gian mô hình vgg_transformer
def test_vgg_transformer(image_path):
    model='vgg_transformer'
    start_time = time.time()
    config = Cfg.load_config_from_name(model)  # Hoặc 'resnet_transformer'
    config['weights'] = f'models/Text_Recognition/Vietocr/{model}.pth'
    config['device'] = 'cuda:0'  # hoặc 'cpu'
    detector = Predictor(config)
    img = Image.open(image_path)
    text = detector.predict(img)
    print(f"Kết quả OCR: {text}")
    save_config(model, config)
    end_time = time.time()
    return end_time - start_time

# đo thời gian mô hình vgg_seq2seq
def test_vgg_seq2seq(image_path):
    model='vgg_seq2seq'
    start_time = time.time()
    config = Cfg.load_config_from_name(model)  # Hoặc 'resnet_transformer'
    config['weights'] = f'models/Text_Recognition/Vietocr/{model}.pth'
    config['device'] = 'cuda:0'  # hoặc 'cpu'
    detector = Predictor(config)
    img = Image.open(image_path)
    text = detector.predict(img)
    print(f"Kết quả OCR: {text}")
    save_config(model, config)
    end_time = time.time()
    return end_time - start_time

# main
def main():
    # Đường dẫn ảnh
    image_path = 'cccd_test_2.jpg'  # Thay bằng ảnh của bạn
    vgg_transformer_time = test_vgg_transformer(image_path)
    vgg_seq2seq_time = test_vgg_seq2seq(image_path)
    print(f"Thời gian mô hình vgg_transformer: {vgg_transformer_time:.3f}s")
    print(f"Thời gian mô hình vgg_seq2seq: {vgg_seq2seq_time:.3f}s")

if __name__ == "__main__":
    main()