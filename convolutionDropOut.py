from keras.datasets import fashion_mnist
import numpy as np
from keras.utils import to_categorical
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import keras
from keras.models import Sequential,Input,Model
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.layers.normalization import BatchNormalization
from keras.layers.advanced_activations import LeakyReLU
import cv2

import loadimages

# Just disables the warning, doesn't enable AVX/FMA
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

train_X,train_Y,test_X,test_Y = loadimages.loading()
print('Training data shape : ', train_X.shape, train_Y.shape)

print('Testing data shape : ', test_X.shape, test_Y.shape)
classes = np.unique(train_Y)
nClasses = len(classes)
print('Total number of outputs : ', nClasses)
print('Output classes : ', classes)
x_train, y_train, x_test, y_test = loadimages.loadingTest()


train_X = train_X.reshape(-1, 150,150, 1)
test_X = test_X.reshape(-1, 150,150, 1)
train_X.shape, test_X.shape
train_X = train_X.astype('float32')
test_X = test_X.astype('float32')
train_X = train_X / 255.
test_X = test_X / 255.

# to try to change complete
x_train = x_train.reshape(-1, 150,150, 1)
x_test = x_test.reshape(-1, 150,150, 1)
x_train.shape, x_test.shape
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train = x_train / 255.
x_test = x_test / 255.

y_train_one_hot = to_categorical(train_Y)
y_test_one_hot = to_categorical(y_test)
x_train,x_valid,label_train,label_valid = train_test_split(x_train, y_train_one_hot, test_size=0.2, random_state=42)


# Change the labels from categorical to one-hot encoding
train_Y_one_hot = to_categorical(y_train)
test_Y_one_hot = to_categorical(test_Y)
# Display the change for category label using one-hot encoding
print('Original label:', train_Y[0])
print('After conversion to one-hot:', train_Y_one_hot[0])

# Mix data ramdomly
train_X,valid_X,train_label,valid_label = train_test_split(train_X, train_Y_one_hot, test_size=0.2, random_state=42)
# test_X,valid_X,test_label,valid_label = train_test_split(test_X, train_Y_one_hot, test_size=1, random_state=42)
# More the batch size is higher more the algo will be performent
batch_size = 64
epochs = 30
num_classes = 2

fashion_model = Sequential()
fashion_model.add(Conv2D(32, kernel_size=(3, 3),activation='linear',input_shape=(150,150,1),padding='same'))
fashion_model.add(LeakyReLU(alpha=0.1))
fashion_model.add(MaxPooling2D((2, 2),padding='same'))
fashion_model.add(Dropout(0.1))

fashion_model.add(Conv2D(64, (3, 3), activation='linear',padding='same'))
fashion_model.add(LeakyReLU(alpha=0.1))
fashion_model.add(MaxPooling2D(pool_size=(2, 2),padding='same'))
fashion_model.add(Dropout(0.1))

fashion_model.add(Conv2D(128, (3, 3), activation='linear',padding='same'))
fashion_model.add(LeakyReLU(alpha=0.1))
fashion_model.add(MaxPooling2D(pool_size=(2, 2),padding='same'))
fashion_model.add(Dropout(0.15))

fashion_model.add(Flatten())
fashion_model.add(Dense(128, activation='linear'))
fashion_model.add(LeakyReLU(alpha=0.1))
fashion_model.add(Dropout(0.1))

fashion_model.add(Dense(num_classes, activation='softmax'))
fashion_model.summary()

fashion_model.compile(loss=keras.losses.categorical_crossentropy, optimizer=keras.optimizers.Adam(),metrics=['accuracy'])
fashion_train_dropout = fashion_model.fit(train_X, train_label, batch_size=batch_size,epochs=epochs,verbose=1,validation_data=(valid_X, valid_label))
fashion_model.save("fashion_model_dropout.h5py")
test_eval = fashion_model.evaluate(x_valid, label_valid, verbose=1)
print('Test loss:', test_eval[0])
print('Test accuracy:', test_eval[1])


predicted_classes = fashion_model.predict(x_valid)
predicted_classes = np.argmax(np.round(predicted_classes),axis=1)
predicted_classes.shape, test_Y.shape
print(predicted_classes)



fig=plt.figure(figsize=(8, 8))
columns = 5
rows = 4
correct = np.where(predicted_classes==x_valid)[0]
print ("Found %d correct labels" % len(correct))
for i, correct in enumerate(correct):
    # fig.add_subplot(rows, columns, i+1)
    # plt.imshow(test_X[correct].reshape(150,150))
    # plt.title("Predicted {}, Class {}".format(predicted_classes[correct], test_Y[correct]))
    cv2.imwrite('/home/camelot/workspace/dicom-tracking-project/goodResult/goodResult(%d).png' % i, x_test[correct].reshape(150,150)*250)


# plt.show()


incorrect = np.where(predicted_classes!=x_valid)[0]
print ("Found %d incorrect labels" % len(incorrect))
for i, incorrect in enumerate(incorrect):
    cv2.imwrite('/home/camelot/workspace/dicom-tracking-project/badResult/badResult(%d).png' % i, x_test[incorrect].reshape(150, 150)*250)
    # fig.add_subplot(1, 1, i+1)
    # plt.title("Predicted {}, Class {}".format(predicted_classes[incorrect], test_Y[incorrect]))
    # plt.imshow(test_X[incorrect].reshape(150, 150))
# plt.show()

# accuracy = fashion_train_dropout.history['acc']
# val_accuracy = fashion_train_dropout.history['val_acc']
# loss = fashion_train_dropout.history['loss']
# val_loss = fashion_train_dropout.history['val_loss']
# epochs = range(len(accuracy))
# plt.plot(epochs, accuracy, 'bo', label='Training accuracy')
# plt.plot(epochs, val_accuracy, 'b', label='Validation accuracy')
# plt.title('Training and validation accuracy')
# plt.legend()
# plt.figure()
# plt.plot(epochs, loss, 'bo', label='Training loss')
# plt.plot(epochs, val_loss, 'b', label='Validation loss')
# plt.title('Training and validation loss')
# plt.legend()
# plt.show()

