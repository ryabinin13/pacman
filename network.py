import keras
from sklearn.model_selection import train_test_split
from keras.layers import Dense, SimpleRNN, Input, LSTM, Flatten
from keras.utils import to_categorical
import numpy as np

def read_data(filename, line_number, separator=' '):
    result = []
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            line = lines[line_number-1].strip()
            list_data = line.split(separator)
            formatted_list = [x for x in list_data]
            for item in formatted_list:
                item = item.replace('[', '').replace(']', '')
                result.append(item)
                res = [int(item.replace(',', '')) for item in result]
                r = list(zip(res[::3],res[1::3] ,res[2::3]))
            return r
    except:
        print("Ошибка")
def read_move(filename, line_number, separator=' '):
    result = []
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            line = lines[line_number-1].strip()
            list_data = line.split(separator)
            formatted_list = [x for x in list_data]
            for item in formatted_list:
                item = item.replace('[', '').replace(']', '')
                result.append(item)
                res = [int(item.replace(',', '')) for item in result]
                r = list(zip(res[::2], res[1::2]))
            return r
    except:
        print("Ошибка")

file_dataX = open('data.txt')
linesDataX = 0
for line in file_dataX:
    linesDataX += 1

file_dataY = open('move.txt')
linesDataY = 0
for line in file_dataY:
    linesDataY += 1

data_X = []
for i in range(1, linesDataX+1):
    line = read_data('data.txt', i)
    line_list = []
    for l in line:
        res = [l[0], l[1], l[2]]
        line_list.append(res)
    data_X.append(line_list)

X = np.array(data_X)

pacman_coord = []
for i in range(1, linesDataY+1):
    data_y = read_move('move.txt', i)
    for d in data_y:
        pacman_coord.append(list(d))

correctY = []
for i in range(len(pacman_coord) - 1):
    forx = pacman_coord[i + 1][0] - pacman_coord[i][0]
    fory = pacman_coord[i + 1][1] - pacman_coord[i][1]
    if (fory == 50 and forx == 0):
        correctY.append(0)
    elif (fory == -50 and forx == 0):
        correctY.append(1)
    elif (fory == 0 and forx == 50):
        correctY.append(2)
    elif (fory == 0 and forx == -50):
        correctY.append(3)



Y= np.array(correctY)
y = to_categorical(Y)

print(X.shape)
print(y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
print(X_train.shape)
print(y_train.shape)
model = keras.Sequential()
#model.add(Dense(64,input_shape=(121,3), activation='relu'))
model.add(Input(shape=(121, 3)))
model.add(Flatten())
model.add(Dense(121, activation='relu'))
model.add(Dense(4, activation='softmax'))
model.summary()

model.compile(loss = 'categorical_crossentropy', metrics=['accuracy'], optimizer='adam')

model.fit(X_train, y_train, batch_size=10, epochs=200)

scores = model.evaluate(X_test, y_test)
print(scores[1])
