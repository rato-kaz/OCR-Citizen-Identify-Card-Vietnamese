#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Benchmark YOLO Model: CPU vs GPU Performance
So sánh thời gian chạy model giữa CPU và GPU
"""

import torch
import cv2
import numpy as np
from pathlib import Path
import time
import matplotlib.pyplot as plt

# Class names từ model
CLASS_NAMES = {
    0: 'bottom_left', 1: 'bottom_right', 2: 'cccd', 3: 'date_of_birth', 
    4: 'date_of_expiry', 5: 'face', 6: 'gender', 7: 'hometown', 8: 'id', 
    9: 'name', 10: 'nation', 11: 'permanent_residence', 12: 'qr_code', 
    13: 'top_left', 14: 'top_right'
}

def load_model_for_device(model_path, device):
    """
    Load model cho device cụ thể
    """
    try:
        from ultralytics import YOLO
        
        # Set torch.load to use weights_only=False for compatibility
        original_load = torch.load
        torch.load = lambda *args, **kwargs: original_load(*args, **kwargs, weights_only=False)
        
        # Load model
        model = YOLO(model_path)
        
        # Move model to device
        model.to(device)
        
        # Restore original torch.load
        torch.load = original_load
        
        return model
        
    except Exception as e:
        print(f"ERROR khi load model cho {device}: {e}")
        return None

def benchmark_inference(model, image_path, device, num_runs=5):
    """
    Benchmark inference trên device cụ thể
    """
    print(f"\nBenchmarking trên {device.upper()}...")
    
    # Warmup runs
    print("  Warmup runs...")
    for _ in range(2):
        try:
            _ = model(image_path, conf=0.3, device=device, verbose=False)
        except:
            pass
    
    # Actual benchmark
    times = []
    for i in range(num_runs):
        start_time = time.time()
        try:
            results = model(image_path, conf=0.3, device=device, verbose=False)
            end_time = time.time()
            inference_time = end_time - start_time
            times.append(inference_time)
            print(f"  Run {i+1}/{num_runs}: {inference_time:.3f}s")
        except Exception as e:
            print(f"  Run {i+1} failed: {e}")
            continue
    
    if times:
        avg_time = np.mean(times)
        std_time = np.std(times)
        min_time = np.min(times)
        max_time = np.max(times)
        
        return {
            'device': device,
            'times': times,
            'avg_time': avg_time,
            'std_time': std_time,
            'min_time': min_time,
            'max_time': max_time,
            'fps': 1.0 / avg_time
        }
    else:
        return None

def plot_benchmark_results(cpu_results, gpu_results):
    """
    Vẽ biểu đồ so sánh kết quả
    """
    if not cpu_results or not gpu_results:
        print("Không có đủ dữ liệu để vẽ biểu đồ")
        return
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Biểu đồ 1: Thời gian inference
    devices = ['CPU', 'GPU']
    avg_times = [cpu_results['avg_time'], gpu_results['avg_time']]
    std_times = [cpu_results['std_time'], gpu_results['std_time']]
    
    bars = ax1.bar(devices, avg_times, yerr=std_times, capsize=5, 
                   color=['#FF6B6B', '#4ECDC4'], alpha=0.7)
    ax1.set_ylabel('Thời gian inference (giây)')
    ax1.set_title('So sánh thời gian inference: CPU vs GPU')
    ax1.grid(True, alpha=0.3)
    
    # Thêm giá trị lên bars
    for i, (bar, avg, std) in enumerate(zip(bars, avg_times, std_times)):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + std + 0.01,
                f'{avg:.3f}s', ha='center', va='bottom', fontweight='bold')
    
    # Biểu đồ 2: FPS
    fps_values = [cpu_results['fps'], gpu_results['fps']]
    bars2 = ax2.bar(devices, fps_values, color=['#FF6B6B', '#4ECDC4'], alpha=0.7)
    ax2.set_ylabel('FPS (Frames Per Second)')
    ax2.set_title('So sánh FPS: CPU vs GPU')
    ax2.grid(True, alpha=0.3)
    
    # Thêm giá trị lên bars
    for bar, fps in zip(bars2, fps_values):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                f'{fps:.1f} FPS', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('benchmark_results.png', dpi=150, bbox_inches='tight')
    print("\nĐã lưu biểu đồ benchmark ra: benchmark_results.png")
    plt.show()

def print_detailed_results(cpu_results, gpu_results):
    """
    In kết quả chi tiết
    """
    print("\n" + "="*60)
    print("KẾT QUẢ BENCHMARK CHI TIẾT")
    print("="*60)
    
    if cpu_results:
        print(f"\nCPU Results:")
        print(f"  Thời gian trung bình: {cpu_results['avg_time']:.3f}s")
        print(f"  Độ lệch chuẩn: {cpu_results['std_time']:.3f}s")
        print(f"  Thời gian nhanh nhất: {cpu_results['min_time']:.3f}s")
        print(f"  Thời gian chậm nhất: {cpu_results['max_time']:.3f}s")
        print(f"  FPS: {cpu_results['fps']:.1f}")
    
    if gpu_results:
        print(f"\nGPU Results:")
        print(f"  Thời gian trung bình: {gpu_results['avg_time']:.3f}s")
        print(f"  Độ lệch chuẩn: {gpu_results['std_time']:.3f}s")
        print(f"  Thời gian nhanh nhất: {gpu_results['min_time']:.3f}s")
        print(f"  Thời gian chậm nhất: {gpu_results['max_time']:.3f}s")
        print(f"  FPS: {gpu_results['fps']:.1f}")
    
    if cpu_results and gpu_results:
        speedup = cpu_results['avg_time'] / gpu_results['avg_time']
        print(f"\nGPU nhanh hơn CPU: {speedup:.2f}x")
        print(f"Tiết kiệm thời gian: {((cpu_results['avg_time'] - gpu_results['avg_time']) / cpu_results['avg_time'] * 100):.1f}%")

def main():
    """
    Hàm chính để benchmark
    """
    model_path = "models/YOLO/best_1.pt"
    image_path = "z6976731768974_f98dcf62faa42fe9e676dd7713187c88.jpg"
    
    print("="*60)
    print("YOLO MODEL BENCHMARK: CPU vs GPU")
    print("="*60)
    
    # Kiểm tra files
    if not Path(model_path).exists():
        print(f"ERROR: Không tìm thấy model: {model_path}")
        return
    
    if not Path(image_path).exists():
        print(f"ERROR: Không tìm thấy ảnh: {image_path}")
        return
    
    # Kiểm tra CUDA
    cuda_available = torch.cuda.is_available()
    print(f"CUDA available: {cuda_available}")
    if cuda_available:
        print(f"CUDA device: {torch.cuda.get_device_name(0)}")
        print(f"CUDA memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
    
    # Load models
    print("\nLoading models...")
    cpu_model = load_model_for_device(model_path, 'cpu')
    gpu_model = None
    if cuda_available:
        gpu_model = load_model_for_device(model_path, 'cuda')
    
    if cpu_model is None:
        print("ERROR: Không thể load CPU model")
        return
    
    # Benchmark CPU
    print("\n" + "="*40)
    print("BENCHMARK CPU")
    print("="*40)
    cpu_results = benchmark_inference(cpu_model, image_path, 'cpu', num_runs=5)
    
    # Benchmark GPU
    gpu_results = None
    if gpu_model is not None:
        print("\n" + "="*40)
        print("BENCHMARK GPU")
        print("="*40)
        gpu_results = benchmark_inference(gpu_model, image_path, 'cuda', num_runs=5)
    
    # In kết quả
    print_detailed_results(cpu_results, gpu_results)
    
    # Vẽ biểu đồ
    if cpu_results and gpu_results:
        plot_benchmark_results(cpu_results, gpu_results)
    
    print("\n" + "="*60)
    print("HOÀN THÀNH BENCHMARK")
    print("="*60)

if __name__ == "__main__":
    main()