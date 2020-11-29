# Import Necessary packages
from keras.preprocessing import image
import numpy as np
import tensorflow as tf
from keras.models import Sequential, load_model
from keras.layers import Dense, Flatten, Dropout
from keras.applications.inception_v3 import InceptionV3
from keras.preprocessing.image import ImageDataGenerator

########################### Data Augmentation ########################

IMAGE_SIZE = [229, 229]

train_path = 'drive//My Drive//Colab Notebooks//hotdog-nothotdog//train'
valid_path = 'drive//My Drive//Colab Notebooks//hotdog-nothotdog//test'

train_datagen = ImageDataGenerator(rescale=1./255,
                                   shear_range=0.2,
                                   zoom_range=0.2,
                                   horizontal_flip=True)

training_set = train_datagen.flow_from_directory(train_path,
                                                 target_size=(224, 224),
                                                 batch_size=32,
                                                 class_mode='binary')

test_datagen = ImageDataGenerator(rescale=1./255,
                                  shear_range=0.2,
                                  zoom_range=0.2,
                                  horizontal_flip=True)

test_set = test_datagen.flow_from_directory(valid_path,
                                            target_size=(224, 224),
                                            batch_size=32,
                                            class_mode='binary')

print(test_set.class_indices)


######### Instantiate InceptionV3 and Build the custom Model (Transfer Learning) #########
Inception = InceptionV3(input_shape=IMAGE_SIZE +
                        [3], weights='imagenet', include_top=False)

# don't train existing weights
for layer in Inception.layers:
    layer.trainable = False

# Build the model
model = Sequential()

model.add(Inception)
model.add(Flatten())
model.add(Dense(256, activation='relu'))
model.add(Dropout(.3))
model.add(Dense(128, activation='relu'))
model.add(Dropout(.2))
model.add(Dense(1, activation='sigmoid'))

model.summary()

########################### Compile & Train the Model ##########################
model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

results = model.fit_generator(
    training_set,
    validation_data=test_set,
    epochs=20,
    steps_per_epoch=len(training_set),
    validation_steps=len(test_set)
)

######################### Evaluating Model Performance #######################

# loss
plt.plot(results.history['loss'], label='train loss')
plt.plot(results.history['val_loss'], label='val loss')
plt.legend()
plt.show()

# accuracies
plt.plot(results.history['accuracy'], label='train acc')
plt.plot(results.history['val_accuracy'], label='val acc')
plt.legend()
plt.show()

model.metrics_names


############## Testing the model ##################

file = valid_path+'//nothotdog//2873.jpg'

img = image.load_img(file, target_size=(229, 229))

img = image.img_to_array(img)

img = np.expand_dims(img, axis=0)
img = dog_img/255

model.predict_classes(img)

#################### Saving and Loading Models  ##################
model.save('Models//hotdog_classifier_final.h5')

new = load_model(
    'Models//hotdog_classifier_final.h5')
