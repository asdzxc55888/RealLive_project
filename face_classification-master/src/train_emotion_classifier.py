"""
File: train_emotion_classifier.py
Author: Octavio Arriaga
Email: arriaga.camargo@gmail.com
Github: https://github.com/oarriaga
Description: Train emotion classification model
"""

from keras.callbacks import CSVLogger, ModelCheckpoint, EarlyStopping
from keras.callbacks import ReduceLROnPlateau
from keras.preprocessing.image import ImageDataGenerator

from models.cnn import mini_XCEPTION
from utils.datasets import DataManager
from utils.datasets import split_data
from utils.preprocessor import preprocess_input

# parameters
batch_size = 32#整数，指定进行梯度下降时每个batch包含的样本数。训练时一个batch的样本会被计算一次梯度下降，使目标函数优化一步。
num_epochs = 10000#整数，训练终止时的epoch值，训练将在达到该epoch值时停止，当没有设置initial_epoch时，它就是训练的总轮数，否则训练的总轮数为epochs - inital_epoch
input_shape = (64, 64, 1)
validation_split = .2 #0~1之间的浮点数，用来指定训练集的一定比例数据作为验证集。验证集将不参与训练，并在每个epoch结束后测试的模型的指标，如损失函数、精确度等。
verbose = 1#日志显示，0为不在标准输出流输出日志信息，1为输出进度条记录，2为每个epoch输出一行记录
num_classes = 7
patience = 50#当monitor不再有改善的时候就会停止训练，这个可以通过patience看出来
base_path = '../trained_models/emotion_models/'

# data generator调用ImageDataGenerator函数实现实时数据增强生成小批量的图像数据
data_generator = ImageDataGenerator(
                        featurewise_center=False,
                        featurewise_std_normalization=False,
                        rotation_range=10,
                        width_shift_range=0.1,
                        height_shift_range=0.1,
                        zoom_range=.1,
                        horizontal_flip=True)

# model parameters/compilation
model = mini_XCEPTION(input_shape, num_classes)
model.compile(optimizer='adam', loss='categorical_crossentropy',
              metrics=['accuracy'])
model.summary()


#3、指定要训练的数据集(emotion→fer2013即喜怒哀乐数据集
datasets = ['fer2013']
#4、for循环实现callbacks、loading dataset
for dataset_name in datasets:
    print('Training dataset:', dataset_name)

     # callbacks回调：通过调用CSVLogger、EarlyStopping、ReduceLROnPlateau、ModelCheckpoint等函数得到训练参数存到一个list内
    log_file_path = base_path + dataset_name + '_emotion_training.log'
    csv_logger = CSVLogger(log_file_path, append=False)#Callback that streams epoch results to a csv file.
    early_stop = EarlyStopping('val_loss', patience=patience)#Stop training when a monitored quantity has stopped improving.
    reduce_lr = ReduceLROnPlateau('val_loss', factor=0.1,   #Reduce learning rate when a metric has stopped improving.
                                  patience=int(patience/4), verbose=1)
    trained_models_path = base_path + dataset_name + '_mini_XCEPTION'
    model_names = trained_models_path + '.{epoch:02d}-{val_acc:.2f}.hdf5'
    model_checkpoint = ModelCheckpoint(model_names, 'val_loss', verbose=1,  #Save the model after every epoch
                                                    save_best_only=True)
    callbacks = [model_checkpoint, csv_logger, early_stop, reduce_lr]

    # loading dataset加载数据集：通过调用DataManager、
    data_loader = DataManager(dataset_name, image_size=input_shape[:2])#自定义DataManager函数实现根据数据集name进行加载
    faces, emotions = data_loader.get_data() #自定义get_data函数根据不同数据集name得到各自的ground truth data，
    faces = preprocess_input(faces)  #自定义preprocess_input函数：处理输入的数据，先转为float32类型然后/ 255.0
    num_samples, num_classes = emotions.shape  #shape函数读取矩阵的长度
    train_data, val_data = split_data(faces, emotions, validation_split) #自定义split_data对数据整理各取所得train_data、 val_data
    train_faces, train_emotions = train_data
    #training model调用fit_generator函数训练模型
    model.fit_generator(data_generator.flow(train_faces, train_emotions, #flow函数返回Numpy Array Iterator迭代
                                            batch_size),
                        steps_per_epoch=len(train_faces) / batch_size,
                        epochs=num_epochs, verbose=1, callbacks=callbacks,
                        validation_data=val_data)  #fit_generator函数Fits the model on data generated batch-by-batch by a Python generator

