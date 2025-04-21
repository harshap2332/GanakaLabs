import numpy as np
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.preprocessing import image
import cv2

# Load the VGG16 model (without top layer)
model = VGG16(weights='imagenet', include_top=False, pooling='avg')

# Load the cropped face image
img_path = 'E:/ganaka/Open CV/images/detected_face_1.jpg'
img = cv2.imread(img_path)

if img is None:
    print("❌ Failed to load cropped face.")
else:
    print("✅ Cropped face loaded.")

    # Resize to 224x224 (required by VGG16)
    img = cv2.resize(img, (224, 224))

    # Convert BGR to RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Convert to array and preprocess
    img_array = image.img_to_array(img_rgb)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    # Extract features
    features = model.predict(img_array)

    # Print result
    print("✅ Feature vector shape:", features.shape)
    print("🔍 First 10 feature values:", features[0][:10])
