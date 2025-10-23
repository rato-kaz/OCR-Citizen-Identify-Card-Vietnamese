import os
import cv2
import json
import time
import numpy as np
from ultralytics import YOLO
from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg
from PIL import Image

def setup_models():
    """Khởi tạo YOLO và VietOCR models với cấu hình tối ưu cho tiếng Việt"""
    print("🚀 Khởi tạo models...")
    
    # Khởi tạo YOLO
    yolo_model_path = 'models/Text_Detection/YOLO/ID_CARD_2.pt'
    if not os.path.exists(yolo_model_path):
        print(f"❌ Không tìm thấy YOLO model: {yolo_model_path}")
        return None, None
    
    try:
        yolo_model = YOLO(yolo_model_path)
        print("✅ YOLO model loaded successfully")
    except Exception as e:
        print(f"❌ Lỗi khi load YOLO model: {e}")
        return None, None
    
    # Khởi tạo VietOCR với cấu hình tối ưu cho tiếng Việt
    try:
        model_name = 'vgg_transformer'  # hoặc 'vgg_seq2seq'
        config = Cfg.load_config_from_name(model_name)
        config['weights'] = f'models/Text_Recognition/Vietocr/{model_name}.pth'
        config['device'] = 'cuda:0'  # hoặc 'cpu'
        ocr = Predictor(config)
        print("✅ VietOCR Vietnamese model loaded successfully")
    except Exception as e:
        print(f"❌ Lỗi khi load VietOCR model: {e}")
        return None, None
    
    return yolo_model, ocr

def detect_text_regions(yolo_model, image_path):
    """YOLO detect các vùng text - chỉ lấy các vùng có text"""
    print(f"🔍 YOLO đang detect text regions...")
    start_time = time.time()
    
    # Chỉ OCR các vùng có text thông tin
    text_labels = ["dob", "gender", "id", "name", "nationality", "current_place1", "current_place2", "expire_date", "issue_date", "origin_place1", "origin_place2", "personal_identifi"]
    text_class_ids = []
    
    # Lấy class names từ model
    class_names = {}
    if hasattr(yolo_model, 'names'):
        class_names = yolo_model.names
        for class_id, class_name in class_names.items():
            if class_name in text_labels:
                text_class_ids.append(int(class_id))
    
    print(f"📝 Chỉ OCR các vùng: {text_labels}")
    print(f"🔢 Class IDs cần OCR: {text_class_ids}")
    
    # Hiển thị mapping ID -> tên class
    if class_names:
        print(f"📋 Mapping Class IDs -> Names:")
        for class_id in text_class_ids:
            class_name = class_names.get(class_id, f"class_{class_id}")
            print(f"  - ID {class_id}: {class_name}")
    
    try:
        results = yolo_model(image_path)
        detection_time = time.time() - start_time
        
        text_regions = []
        all_regions = []
        
        for result in results:
            if result.boxes is not None:
                boxes = result.boxes.xyxy.cpu().numpy()
                confidences = result.boxes.conf.cpu().numpy()
                classes = result.boxes.cls.cpu().numpy()
                
                for i, (box, conf, cls) in enumerate(zip(boxes, confidences, classes)):
                    x1, y1, x2, y2 = box.astype(int)
                    class_id = int(cls)
                    class_name = class_names.get(class_id, f"class_{class_id}")
                    
                    region_info = {
                        'id': i + 1,
                        'bbox': [int(x1), int(y1), int(x2), int(y2)],
                        'confidence': float(conf),
                        'class_id': class_id,
                        'class_name': class_name
                    }
                    
                    all_regions.append(region_info)
                    
                    # Chỉ thêm vào text_regions nếu là vùng có text
                    if class_id in text_class_ids:
                        text_regions.append(region_info)
        
        print(f"✅ YOLO detect {len(all_regions)} regions tổng cộng")
        print(f"📝 Chỉ OCR {len(text_regions)} vùng có text trong {detection_time:.3f}s")
        return text_regions, detection_time, all_regions
        
    except Exception as e:
        print(f"❌ Lỗi YOLO detection: {e}")
        return [], 0, []

def extract_text_from_regions(ocr, image_path, text_regions):
    """VietOCR extract text từ các vùng đã detect"""
    print(f"🔍 VietOCR đang extract text từ các vùng đã detect...")
    
    start_time = time.time()
    extracted_results = []
    
    # Load ảnh gốc
    image = cv2.imread(image_path)
    if image is None:
        print(f"❌ Không thể đọc ảnh: {image_path}")
        return [], 0
    
    for region in text_regions:
        x1, y1, x2, y2 = region['bbox']
        cropped_image = image[y1:y2, x1:x2]
        
        # Convert OpenCV image to PIL Image for VietOCR
        cropped_pil = Image.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))
        
        try:
            text = ocr.predict(cropped_pil)
            extracted_results.append({
                'bbox': region['bbox'],
                'extracted_text': text,
                'yolo_confidence': region['confidence'],
                'ocr_confidence': 1.0,  # VietOCR không trả về confidence
                'class_id': region['class_id'],
                'class_name': region['class_name']
            })
        except Exception as e:
            print(f"⚠️  Lỗi OCR cho region {region['id']} ({region['class_name']}): {e}")
            extracted_results.append({
                'bbox': region['bbox'],
                'extracted_text': '',
                'yolo_confidence': region['confidence'],
                'ocr_confidence': 0.0,
                'class_id': region['class_id'],
                'class_name': region['class_name']
            })
    
    extraction_time = time.time() - start_time
    print(f"✅ VietOCR extract {len(extracted_results)} text trong {extraction_time:.3f}s")
    return extracted_results, extraction_time

def save_results(image_path, all_results, detection_time, ocr_time, total_time):
    """Lưu kết quả ra file JSON và ảnh"""
    try:
        # Tạo thư mục output
        output_dir = "output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Lưu JSON
        result_data = {
            'image_path': image_path,
            'timing': {
                'detection_time': detection_time,
                'ocr_time': ocr_time,
                'total_time': total_time
            },
            'total_regions': len(all_results),
            'results': all_results
        }
        
        json_file = os.path.join(output_dir, f"yolo_ocr_vietnamese_{os.path.basename(image_path)}.json")
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(result_data, f, ensure_ascii=False, indent=2)
        print(f"💾 Đã lưu kết quả JSON: {json_file}")
        
        # Tạo ảnh kết quả
        create_result_image(image_path, all_results, output_dir)
        
    except Exception as e:
        print(f"❌ Lỗi khi lưu kết quả: {e}")

def create_result_image(image_path, results, output_dir):
    """Tạo ảnh kết quả với bounding box và text"""
    try:
        image = cv2.imread(image_path)
        if image is None:
            return
        
        colors = [
            (0, 255, 0),    # Xanh lá
            (255, 0, 0),    # Xanh dương
            (0, 0, 255),    # Đỏ
            (255, 255, 0),  # Vàng
            (255, 0, 255),  # Magenta
            (0, 255, 255),  # Cyan
        ]
        
        for result in results:
            bbox = result['bbox']
            text = result['extracted_text']
            yolo_conf = result['yolo_confidence']
            ocr_conf = result['ocr_confidence']
            cls_id = result['class_id']
            cls_name = result['class_name']
            
            x1, y1, x2, y2 = bbox
            color = colors[cls_id % len(colors)]
            
            # Vẽ bounding box
            cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
            
            # Vẽ label với tên class
            label = f"{cls_name} (Y:{yolo_conf:.2f})"
            label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
            
            # Background cho text
            cv2.rectangle(image, (x1, y1 - label_size[1] - 10), 
                         (x1 + label_size[0], y1), color, -1)
            
            # Text
            cv2.putText(image, label, (x1, y1 - 5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # Vẽ extracted text bên dưới
            if text:
                text_label = f"'{text[:30]}{'...' if len(text) > 30 else ''}'"
                text_y = y2 + 20
                cv2.putText(image, text_label, (x1, text_y), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)
        
        # Lưu ảnh
        output_path = os.path.join(output_dir, f"yolo_ocr_vietnamese_{os.path.basename(image_path)}")
        cv2.imwrite(output_path, image)
        print(f"🖼️  Đã lưu ảnh kết quả: {output_path}")
        
    except Exception as e:
        print(f"❌ Lỗi khi tạo ảnh kết quả: {e}")

def process_image(yolo_model, ocr, image_path):
    """Xử lý một ảnh với YOLO + VietOCR pipeline"""
    print(f"\n{'='*60}")
    print(f"🖼️  Xử lý ảnh: {image_path}")
    print(f"{'='*60}")
    
    total_start_time = time.time()
    
    # Bước 1: YOLO Detection
    text_regions, detection_time, all_regions = detect_text_regions(yolo_model, image_path)
    
    if not text_regions:
        print("⚠️  Không tìm thấy vùng text nào cần OCR")
        return None
    
    # Bước 2: VietOCR Text Extraction
    extracted_results, ocr_time = extract_text_from_regions(ocr, image_path, text_regions)
    
    total_time = time.time() - total_start_time
    
    # Bước 3: Lưu kết quả
    save_results(image_path, extracted_results, detection_time, ocr_time, total_time)
    
    # In thống kê
    print(f"\n📊 THỐNG KÊ:")
    print(f"  🔍 YOLO Detection: {detection_time:.3f}s")
    print(f"  📝 VietOCR: {ocr_time:.3f}s")
    print(f"  ⏱️  Total Time: {total_time:.3f}s")
    print(f"  📍 Tổng regions detected: {len(all_regions)}")
    print(f"  📝 Regions cần OCR: {len(text_regions)}")
    print(f"  📄 Text extracted: {len(extracted_results)}")
    
    # In chi tiết các vùng đã OCR
    print(f"\n📋 CHI TIẾT CÁC VÙNG ĐÃ OCR:")
    for result in extracted_results:
        print(f"  - {result['class_name']}: '{result['extracted_text']}' (conf: {result['yolo_confidence']:.2f})")
    
    return extracted_results

def main():
    """Hàm chính"""
    print("🚀 YOLO + VietOCR Vietnamese Pipeline")
    print("=" * 60)
    
    # Khởi tạo models
    yolo_model, ocr = setup_models()
    if yolo_model is None or ocr is None:
        return
    
    # Danh sách ảnh test
    test_images = [
        "img527.jpg",
        "49.jpg"
    ]
    
    all_results = {}
    total_processing_time = 0
    
    for image_path in test_images:
        if not os.path.exists(image_path):
            print(f"⚠️  Không tìm thấy ảnh: {image_path}")
            continue
        
        start_time = time.time()
        results = process_image(yolo_model, ocr, image_path)
        processing_time = time.time() - start_time
        
        if results:
            all_results[image_path] = {
                'results': results,
                'processing_time': processing_time
            }
            total_processing_time += processing_time
    
    # Tổng kết
    print(f"\n{'='*60}")
    print("📊 TỔNG KẾT")
    print(f"{'='*60}")
    print(f"🖼️  Số ảnh đã xử lý: {len(all_results)}")
    print(f"⏱️  Tổng thời gian xử lý: {total_processing_time:.3f}s")
    print(f"📁 Kết quả được lưu trong thư mục 'output/'")
    print("✅ Pipeline hoàn thành!")

if __name__ == "__main__":
    main()
