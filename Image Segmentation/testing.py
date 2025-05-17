import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from tensorflow.keras import models, layers
import cv2
import numpy as np
from tensorflow.keras.optimizers import Adam


def preprocess_input(image_path, target_size=(256, 256)):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    resized_image = cv2.resize(image, target_size)

    resized_image = resized_image.astype(np.float32)

    normalized_image = resized_image / 255.0

    return normalized_image


def preprocess_mask(mask_path, target_size=(256, 256)):
    mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)

    resized_mask = cv2.resize(mask, target_size)

    normalized_mask = resized_mask / 255.0

    return normalized_mask


images = []
masks = []

for i in range(1, 438):
    images.append(preprocess_input('Dataset/benign/benign ({}).png'.format(i), (224, 224)))
    masks.append(preprocess_mask('Dataset/benign/benign ({})_mask.png'.format(i), (218, 218)))

for i in range(1, 211):
    if i == 116:
        continue
    images.append(preprocess_input('Dataset/malignant/malignant ({}).png'.format(i), (224, 224)))
    masks.append(preprocess_mask('Dataset/malignant/malignant ({})_mask.png'.format(i), (218, 218)))

for i in range(1, 134):
    images.append(preprocess_input('Dataset/normal/normal ({}).png'.format(i), (224, 224)))
    masks.append(preprocess_mask('Dataset/normal/normal ({})_mask.png'.format(i), (218, 218)))

images = np.array(images)
masks = np.expand_dims(np.array(masks), axis=-1)

x_train, x_test, y_train, y_test = train_test_split(images, masks, test_size=0.2, random_state=0)

model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 1)),
    layers.MaxPooling2D((2, 2)),

    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),

    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),

    layers.Conv2D(256, (3, 3), activation='relu'),
    layers.Conv2DTranspose(128, (3, 3), activation='relu'),
    layers.UpSampling2D((2, 2)),

    layers.Conv2DTranspose(64, (3, 3), activation='relu'),
    layers.UpSampling2D((2, 2)),

    layers.Conv2DTranspose(32, (3, 3), activation='relu'),
    layers.UpSampling2D((2, 2)),

    layers.Conv2D(1, (3, 3), activation='sigmoid')
])


model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

history = model.fit(x_train, y_train, epochs=15, batch_size=32, validation_data=(x_test, y_test))

loss, accuracy = model.evaluate(x_test, y_test)
print("Test Loss:", loss)
print("Test Accuracy:", accuracy)

plt.plot(history.history['accuracy'], label='accuracy')
plt.plot(history.history['val_accuracy'], label='val_accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.ylim([0.9, 1])
plt.legend(loc='lower right')
plt.show()

predictions = model.predict(x_test)

for i in range(15):
    # Plot input image
    plt.subplot(1, 3, 1)
    plt.imshow(x_test[i], cmap='gray')
    plt.axis('off')
    plt.title('Input Image {}'.format(i))

    # Plot ground truth mask
    plt.subplot(1, 3, 2)
    plt.imshow(np.squeeze(y_test[i]), cmap='gray')
    plt.axis('off')
    plt.title('Ground Truth Mask {}'.format(i))

    # Plot predicted mask
    plt.subplot(1, 3, 3)
    plt.imshow(np.squeeze(predictions[i]), cmap='gray')
    plt.axis('off')
    plt.title('Predicted Mask {}'.format(i))

    plt.tight_layout()
    plt.show()
