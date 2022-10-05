from tensorflow import keras
from keras.preprocessing.image import ImageDataGenerator


def model_evaluation(model_path):
    model = keras.models.load_model(model_path)
    
    test_dir = './data/Face Mask Dataset/Test'
    test_datagen = ImageDataGenerator(rescale=1.0/255)
    test_generator = test_datagen.flow_from_directory(directory=test_dir,target_size=(128,128),class_mode='categorical',batch_size=32)
    
    evaluation_result = model.evaluate_generator(test_generator)
    accuracy = evaluation_result[1]
    print("Testing dataset: {}".format(accuracy))
    return accuracy
    