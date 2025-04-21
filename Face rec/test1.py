import cv2

# ✅ Step 1: Load the image (use forward slashes or raw string to avoid path errors)
image = cv2.imread('E:/ganaka/Open CV/images/boy.jpeg')  # ✅ Make sure this path and file name are correct

# ✅ Step 2: Check if the image was loaded properly
if image is None:
    print("❌ Failed to load image. Please check the file path and try again.")
else:
    print("✅ Image loaded successfully!")

    # ✅ Step 3: Show the original image
    cv2.imshow("Original Image", image)
    cv2.waitKey(0)  # Wait for any key press

    # ✅ Step 4: Resize the image
    resized = cv2.resize(image, (224, 224))  # Resize to 224x224
    cv2.imshow("Resized Image", resized)
    cv2.waitKey(0)

    # ✅ Step 5: Save the resized image
    cv2.imwrite('E:/ganaka/Open CV/images/resized_output.jpg', resized)
    print("✅ Resized image saved as 'resized_output.jpg'")

    # ✅ Step 6: Close all OpenCV windows
    cv2.destroyAllWindows()
