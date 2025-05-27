# OpenCV 人脸检测替代方案

## 问题描述

原项目依赖 `slimeface` 包进行人脸检测和图像裁剪，但该包在 macOS ARM64 平台上存在构建问题：

- 缺少 `libfacedetection` 子模块
- CMake 构建失败
- 依赖复杂的 C++ 编译环境

## 解决方案

我们实现了一个基于 OpenCV 的替代方案：

### 1. 移除有问题的依赖

暂时注释掉了 `pyproject.toml` 中的 `slimeface` 依赖：

```toml
# slimeface = "^2024.9.27"  # 暂时注释掉，构建有问题
```

### 2. 添加 OpenCV 依赖

```bash
poetry add opencv-python
```

### 3. 实现 OpenCV 人脸检测器

创建了 `javsp/cropper/opencv_crop.py`，使用 OpenCV 的 Haar 级联分类器进行人脸检测。

### 4. 更新配置系统

- 在 `javsp/config.py` 中添加了 `OpenCVEngine` 配置类
- 更新了 `javsp/cropper/__init__.py` 以支持新的引擎
- 在 `config.yml` 中添加了 OpenCV 配置示例

## 使用方法

### 启用 OpenCV 人脸检测

在 `config.yml` 中取消注释并配置：

```yaml
cover:
  crop:
    engine: 
      name: opencv
```

### 功能对比

| 特性 | Slimeface | OpenCV |
|------|-----------|--------|
| 安装难度 | 困难（需要 CMake、C++ 编译器） | 简单（pip 安装） |
| 平台兼容性 | 有限 | 优秀 |
| 检测精度 | 高 | 中等 |
| 性能 | 快 | 中等 |
| 维护性 | 低 | 高 |

## 测试

运行以下命令测试安装：

```bash
# 测试项目是否可以正常运行
poetry run python -m javsp --help

# 测试 OpenCV 人脸检测器
poetry run python -c "from javsp.cropper.opencv_crop import OpenCVCropper; print('OpenCV cropper imported successfully')"
```

## 未来改进

如果需要更高精度的人脸检测，可以考虑：

1. 使用 `face-recognition` 库（基于 dlib）
2. 使用深度学习模型（如 MTCNN、RetinaFace）
3. 等待 `slimeface` 包修复构建问题

## 注意事项

- OpenCV 的 Haar 级联分类器在某些情况下可能不如深度学习模型精确
- 如果检测不到人脸，会自动回退到默认裁剪方式
- 该实现与原 `slimeface` 接口兼容，可以无缝替换 