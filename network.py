import keras
from keras.layers import Dense, SimpleRNN, Input
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

data_X = []
for i in range(50):
    line = read_data('data.txt', i)
    line_list = []
    for l in line:
        line_list.append(list(l))
    data_X.append(line_list)

X = np.array(data_X)

i = 0
for d in X:
    print(f"{i} значение {d}")
    i = i +1

data_y = read_move('move.txt', 1)
y_ = []
for d in data_y:
  y_.append(list(d))
print(y_)

for i in range(len(y_) - 1):
    forx = y_[i + 1][0] - y_[i][0]
    fory = y_[i + 1][1] - y_[i][1]
    if (fory == 50 and forx == 0):
        y_[i] = 0
    if (fory == -50 and forx == 0):
        y_[i] = 1
    if (fory == 0 and forx == 50):
        y_[i] = 2
    if (fory == 0 and forx == -50):
        y_[i] = 3
y_[-1] = 0

y_categorical= np.array(y_)
y = to_categorical(y_categorical)

print(y)
print(X.shape)
print(y.shape)

model = keras.Sequential()
model.add(Input(shape=(122, 3)))
model.add(SimpleRNN(128, activation='tanh'))
model.add(Dense(4, activation='softmax'))
model.summary()

model.compile(loss = 'categorical_crossentropy', metrics=['accuracy'], optimizer='adam')

result = model.fit(X, y, batch_size=11, epochs=100)

test_file = read_data('data.txt', 1)
test_ = []
for w in test_file:
  test_.append(list(w))
test = np.array(test_)

new_arr = np.expand_dims(test, axis=0)
print(model.predict(new_arr))

