import cv2
import numpy as np
from mtcnn import MTCNN
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.preprocessing import image
from sklearn.metrics.pairwise import cosine_similarity

# Initialize detector and VGG16 model
detector = MTCNN()
model = VGG16(weights='imagenet', include_top=False, pooling='avg')

def detect_and_crop_face(img_path, save_path):
    img = cv2.imread(img_path)
    if img is None:
        print(f"❌ Failed to load image: {img_path}")
        return None

    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    faces = detector.detect_faces(rgb_img)

    if not faces:
        print(f"❌ No face detected in: {img_path}")
        return None

    x, y, w, h = faces[0]['box']
    cropped_face = img[y:y+h, x:x+w]
    cv2.imwrite(save_path, cropped_face)
    print(f"✅ Cropped face saved as {save_path}")
    return save_path

def extract_features(img_path):
    img = cv2.imread(img_path)
    if img is None:
        print(f"❌ Failed to load image for features: {img_path}")
        return None

    img = cv2.resize(img, (224, 224))
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_array = image.img_to_array(img_rgb)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    features = model.predict(img_array)
    return features

# Face image paths
img1_path = 'E:/ganaka/Open CV/images/sample1.jpg'
img2_path = 'E:/ganaka/Open CV/images/sample6.jpeg'

# Save cropped faces
face1_path = 'E:/ganaka/Open CV/images/face1.jpg'
face2_path = 'E:/ganaka/Open CV/images/face2.jpg'

# Detect and crop
face1 = detect_and_crop_face(img1_path, face1_path)
face2 = detect_and_crop_face(img2_path, face2_path)

# Extract features and compare
if face1 and face2:
    feat1 = extract_features(face1)
    feat2 = extract_features(face2)

    if feat1 is not None and feat2 is not None:
        similarity = cosine_similarity(feat1, feat2)[0][0]
        print(f"\n🔍 Cosine Similarity: {similarity:.4f}")
        if similarity >= 0.80:
            print("✅ Likely the same person")
        else:
            print("❌ Likely different people")
