import cv2
from mtcnn import MTCNN

# Step 1: Load the image
image_path = 'E:/ganaka/Open CV/images/boy.jpeg'
image = cv2.imread(image_path)

# Step 2: Check if image loaded
if image is None:
    print("❌ Failed to load image. Check the path.")
else:
    print("✅ Image loaded.")

    # Step 3: Convert image to RGB (MTCNN expects RGB format)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Step 4: Initialize MTCNN detector
    detector = MTCNN()

    # Step 5: Detect faces
    faces = detector.detect_faces(rgb_image)
    print(f"✅ {len(faces)} face(s) detected.")

    # Step 6: Draw rectangles around detected faces
    for face in faces:
        x, y, width, height = face['box']
        confidence = face['confidence']

        # Draw bounding box
        cv2.rectangle(image, (x, y), (x + width, y + height), (0, 255, 0), 2)
        cv2.putText(image, f'Confidence: {confidence:.2f}', (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Step 7: Show the result
    cv2.imshow("Detected Faces", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()