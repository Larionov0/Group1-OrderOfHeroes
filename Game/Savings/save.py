import pickle


FILENAME = 'data.bin'


def save_data(data, filename=FILENAME):
    with open(filename, 'wb') as file:
        pickle.dump(data, file)


def load_data(filename=FILENAME):
    with open(filename, 'rb') as file:
        data = pickle.load(file)

    return data
