from keras.models import model_from_json
import sys


def print_progress(name, i, n, start):
    sys.stdout.write(
        "\r%s progress: %0.2f percent. Execution time: %0.2f" % (name, 100 * (i + 1) / n, time.time() - start))
    sys.stdout.flush()


def save_model(model_to_save, model_filename):
    # serialize model to JSON
    model_json = model_to_save.model.to_json()
    with open(model_filename+".json", "w") as json_file:
        json_file.write(model_json)
    # serialize weights to HDF5
    model_to_save.model.save_weights(model_filename+".h5")
    print(model_filename+" Saved model to disk")


def load_saved_model(model_filename):
    # load json and create model
    json_file = open(model_filename+".json", 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    # load weights into new model
    model.load_weights(model_filename+".h5")
    print(model_filename+" loaded model from disk")

    return model
