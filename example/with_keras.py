"""
classify with keras model
"""
from keras.models import Sequential

from stagesepx.cutter import VideoCutter
from stagesepx.classifier.keras import KerasClassifier
from stagesepx.reporter import Reporter
from stagesepx.video import VideoObject


video_path = "../demo.mp4"
video = VideoObject(video_path)
video.load_frames()

# --- cutter ---
cutter = VideoCutter()
res = cutter.cut(video)
stable, unstable = res.get_range()
data_home = res.pick_and_save(stable, 10)

# --- classify ---
# We recommend that you read the code (KerasClassifier) directly for better understanding
# and actually you can build your own Classifier which based on it
class NewKerasClassifier(KerasClassifier):
    def create_model(self) -> Sequential:
        # overwrite this method to design your own model structure!

        # model  = Sequential()
        # ...
        pass

    def train(self, data_path: str, *_, **__):
        # ...
        pass


# or use the default one
# and then init it
# epochs=1 is just a example
cl = KerasClassifier(epochs=1)

# train model and save weights
cl.train(data_home)
cl.save_model("keras_model.h5")

# you would better reuse the trained model for less time cost
# keras model takes much more time than SVM
# cl.load_model("keras_model.h5")

classify_result = cl.classify(video, stable, keep_data=True)
result_dict = classify_result.to_dict()

# --- draw ---
r = Reporter()
r.draw(classify_result)
