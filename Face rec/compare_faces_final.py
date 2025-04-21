import cv2
import numpy as np
from mtcnn import MTCNN
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.preprocessing import image
from sklearn.metrics.pairwise import cosine_similarity

# Initialize MTCNN and VGG16
detector = MTCNN()
model = VGG16(weights='imagenet', include_top=False, pooling='avg')

# Draw bold label with background
def draw_label(img, text, position, box_color=(0, 0, 0), text_color=(255, 255, 255)):
    x, y = position
    font = cv2.FONT_HERSHEY_SIMPLEX
    scale = 2
    thickness = 3
    (text_width, text_height), _ = cv2.getTextSize(text, font, scale, thickness)
    cv2.rectangle(img, (x, y - text_height - 10), (x + text_width + 10, y), box_color, -1)
    cv2.putText(img, text, (x + 5, y - 5), font, scale, text_color, thickness)

# Detect face and crop for features
def detect_face_and_draw(img_path):
    img = cv2.imread(img_path)
    if img is None:
        print(f"❌ Failed to load image: {img_path}")
        return None, None, None
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    faces = detector.detect_faces(rgb)
    if not faces:
        print(f"❌ No face detected in: {img_path}")
        return img, None, None
    x, y, w, h = faces[0]['box']
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    face_crop = img[y:y + h, x:x + w]
    return img, face_crop, (x, y)

# Extract features using VGG16
def extract_features(face_img):
    face_img = cv2.resize(face_img, (224, 224))
    face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
    arr = image.img_to_array(face_img)
    arr = np.expand_dims(arr, axis=0)
    arr = preprocess_input(arr)
    return model.predict(arr)

# Image paths
img1_path = 'E:/ganaka/Open CV/images/sample1.jpg'
img2_path = 'E:/ganaka/Open CV/images/sample2.jpeg'

# Detect faces
img1, face1, face1_pos = detect_face_and_draw(img1_path)
img2, face2, face2_pos = detect_face_and_draw(img2_path)

# If both faces found
if face1 is not None and face2 is not None:
    # Extract features and compare
    feat1 = extract_features(face1)
    feat2 = extract_features(face2)
    similarity = cosine_similarity(feat1, feat2)[0][0]
    label = f"Match: {similarity:.2%}"

    # 🖥 Terminal Output
    print("\n Comparing...")
    print(f"- {img1_path.split('/')[-1]}")
    print(f"- {img2_path.split('/')[-1]}")
    print(f"\n🔍 {label}\n")

    # Draw labels on face boxes
    if face1_pos:
        draw_label(img1, label, (face1_pos[0], face1_pos[1] - 10))
    if face2_pos:
        draw_label(img2, label, (face2_pos[0], face2_pos[1] - 10))

    # Resize and combine images
    img1_resized = cv2.resize(img1, (500, 500))
    img2_resized = cv2.resize(img2, (500, 500))
    combined = np.hstack((img1_resized, img2_resized))

    # Show result
    cv2.imshow("Face Match Result", combined)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("❌ Face not detected in one or both images.")
