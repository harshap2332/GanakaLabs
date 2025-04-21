import cv2
import numpy as np
from mtcnn import MTCNN
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.preprocessing import image
from sklearn.metrics.pairwise import cosine_similarity

# Initialize detectors and model
detector = MTCNN()
model = VGG16(weights='imagenet', include_top=False, pooling='avg')

# Label drawer with semi-transparent box
def draw_label(img, text, position):
    x, y = position
    font = cv2.FONT_HERSHEY_SIMPLEX
    scale = 2.0
    thickness = 2
    (text_width, text_height), _ = cv2.getTextSize(text, font, scale, thickness)
    padding = 10
    # Background rectangle
    box_coords = ((x, y - text_height - padding), (x + text_width + padding, y + padding))
    overlay = img.copy()
    cv2.rectangle(overlay, box_coords[0], box_coords[1], (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.6, img, 0.4, 0, img)
    # Text on top
    cv2.putText(img, text, (x + 5, y - 5), font, scale, (255, 255, 255), thickness)

# Detect face and crop it
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
    cropped = img[y:y + h, x:x + w]
    return img, cropped, (x, y)

# Extract features
def extract_features(face_img):
    face_img = cv2.resize(face_img, (224, 224))
    face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
    arr = image.img_to_array(face_img)
    arr = np.expand_dims(arr, axis=0)
    arr = preprocess_input(arr)
    return model.predict(arr)

# File paths
img1_path = 'E:/ganaka/Open CV/images/sample1.jpg'
img2_path = 'E:/ganaka/Open CV/images/sample2.jpg'

# Detect and crop
img1, face1, pos1 = detect_face_and_draw(img1_path)
img2, face2, pos2 = detect_face_and_draw(img2_path)

# Proceed if both faces found
if face1 is not None and face2 is not None:
    feat1 = extract_features(face1)
    feat2 = extract_features(face2)
    similarity = cosine_similarity(feat1, feat2)[0][0]
    label = f"Match: {similarity:.2%}"
    print("🔍", label)

    if pos1:
        draw_label(img1, label, (pos1[0], pos1[1] - 10))
    if pos2:
        draw_label(img2, label, (pos2[0], pos2[1] - 10))

    # Resize and combine for display
    img1 = cv2.resize(img1, (600, 600))
    img2 = cv2.resize(img2, (600, 600))
    combined = np.hstack((img1, img2))

    # Show result
    cv2.imshow("Face Match Result", combined)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("❌ Face not detected in one or both images.")
