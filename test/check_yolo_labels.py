import os
from ultralytics import YOLO
import json

def check_yolo_labels(model_path):
    """Kiểm tra các label/class có trong YOLO model"""
    print(f"🔍 Kiểm tra YOLO model: {model_path}")
    print("=" * 60)
    
    if not os.path.exists(model_path):
        print(f"❌ Không tìm thấy model: {model_path}")
        return
    
    try:
        # Load model
        model = YOLO(model_path)
        print("✅ Model loaded successfully")
        
        # Lấy thông tin về classes
        if hasattr(model, 'names'):
            class_names = model.names
            print(f"\n📋 Tổng số classes: {len(class_names)}")
            print("\n🏷️  Danh sách các labels:")
            print("-" * 40)
            
            for class_id, class_name in class_names.items():
                print(f"  {class_id}: {class_name}")
            
            # Lưu vào file JSON
            labels_info = {
                'model_path': model_path,
                'total_classes': len(class_names),
                'class_names': class_names,
                'class_list': list(class_names.values())
            }
            
            with open('yolo_labels_info.json', 'w', encoding='utf-8') as f:
                json.dump(labels_info, f, ensure_ascii=False, indent=2)
            
            print(f"\n💾 Đã lưu thông tin labels vào: yolo_labels_info.json")
            
        else:
            print("⚠️  Không tìm thấy thông tin về class names")
            
        # Thông tin khác về model
        print(f"\n📊 Thông tin model:")
        print(f"  - Model type: {type(model.model)}")
        
        if hasattr(model, 'model'):
            print(f"  - Model architecture: {model.model.__class__.__name__}")
        
    except Exception as e:
        print(f"❌ Lỗi khi load model: {e}")

def main():
    """Hàm chính"""
    model_path = "models/Text_Detection/YOLO/ID_CARD_2.pt"
    check_yolo_labels(model_path)

if __name__ == "__main__":
    main()
