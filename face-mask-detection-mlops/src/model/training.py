import time
import mlflow
from keras.applications.vgg19 import VGG19
from keras.applications.vgg19 import preprocess_input
from keras import Sequential
from keras.layers import Flatten, Dense
from keras.preprocessing.image import ImageDataGenerator

def model_training(mlflow_experiment_name = "mask_detection"):
    mlflow.set_experiment(mlflow_experiment_name)
    mlflow.keras.autolog()

    #Load train and test set
    train_dir = './data/Face Mask Dataset/Train'
    val_dir = './data/Face Mask Dataset/Validation'
    
    # Data augmentation

    train_datagen = ImageDataGenerator(rescale=1.0/255, horizontal_flip=True, zoom_range=0.2,shear_range=0.2)
    train_generator = train_datagen.flow_from_directory(directory=train_dir,target_size=(128,128),class_mode='categorical',batch_size=32)

    val_datagen = ImageDataGenerator(rescale=1.0/255)
    val_generator = val_datagen.flow_from_directory(directory=val_dir,target_size=(128,128),class_mode='categorical',batch_size=32)

    
    vgg19 = VGG19(weights='imagenet',include_top=False,input_shape=(128,128,3))

    for layer in vgg19.layers:
        layer.trainable = False

    model = Sequential()
    model.add(vgg19)
    model.add(Flatten())
    model.add(Dense(2,activation='sigmoid'))
    model.summary()
    
    model.compile(optimizer="adam",loss="categorical_crossentropy",metrics ="accuracy")
    
    # Training the model.
    with mlflow.start_run() as run:
        history = model.fit_generator(generator=train_generator,
                              steps_per_epoch=len(train_generator)//32,
                              epochs=20,validation_data=val_generator,
                              validation_steps=len(val_generator)//32)
    model_path = './result/model_{}.h5'.format(int(time.time()))
    model.save(model_path)
    return model_path, run