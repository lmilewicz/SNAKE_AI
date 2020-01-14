from keras.models import model_from_json
import sys
import time
import numpy as np


def print_progress(name, i, n, start):
    sys.stdout.write(
        "\r%s progress: %0.2f percent. Execution time: %0.2f" % (name, 100 * (i + 1) / n, time.time() - start))
    sys.stdout.flush()


def print_eneration_progress(z, best_score, fitness_array, generations_num, start):
    array_to_print = (np.sort(fitness_array)[::-1])[: 10]
    print("Best score for gen %d: %d. Fitness: %d. Median: %d. Progress: %0.2f. Time: %0.2f. FitArr: %s." %
          (z, best_score, np.max(fitness_array), np.median(fitness_array), 100 * (z + 1) / generations_num,
           time.time() - start, ", ".join(str(int(x)) for x in array_to_print)))


def save_model(model_to_save, model_filename):
    # serialize model to JSON
    model_json = model_to_save.to_json()
    with open("saved_models/"+model_filename+".json", "w") as json_file:
        json_file.write(model_json)
    # serialize weights to HDF5
    model_to_save.save_weights("saved_models/"+model_filename + ".h5")
    print(model_filename + " Saved model to disk")


def load_saved_model(model_filename):
    # load json and create model
    json_file = open("saved_models/"+model_filename+".json", 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    # load weights into new model
    model.load_weights("saved_models/"+model_filename+".h5")
    print(model_filename+" loaded model from disk")

    return model


def save_fitness_array(filename, fitness_array):
    np.savetxt("saved_models/" + filename + ".txt", fitness_array, delimiter=',')
    print(filename + " Saved fitness_array to disk")
