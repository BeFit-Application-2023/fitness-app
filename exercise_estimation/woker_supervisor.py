import cv2
import time
from exercise_estimation.exercise_counter import ExerciseCounter
from exercise_estimation.pose_estimator import PoseEstimation
from utils import frame_decode, frame_encode, moving_average, body_mass_index


class WorkerSupervisor:

    def __init__(self):
        self.__worker_mapper = {}
        self.__visibility_points = [11, 12, 29, 30]

    def retrieve_current_data(self, data, user_unique_id):
        return data.query.filter_by(user_id=user_unique_id).all()[-1]

    def add_worker(self, unique_sid, data, user_unique_id):
        user_exercise_info = self.retrieve_current_data(data, user_unique_id)
        self.__worker_mapper[unique_sid] = [ExerciseCounter({user_exercise_info.exercise_1: user_exercise_info.count_1, \
            user_exercise_info.exercise_2: user_exercise_info.count_2, \
            user_exercise_info.exercise_3: user_exercise_info.count_3, \
            # user_exercise_info.exercise_4: user_exercise_info.count_4
            }), PoseEstimation()]

    def check_visibility(self, points):
        return all([point.visibility > 0.2 for point in points])

    def run(self, sid, frame, exercise):
        frame = frame_decode(frame)
        frame, landmarks = self.__worker_mapper[sid][1].estimate(frame)
        counter = self.__worker_mapper[sid][0].mapping_exercise[exercise]
        # if landmarks is None:
        #     error_message = 'Cannot detect the whole body.'
        #     frame = cv2.putText(frame, error_message, (20, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 1, cv2.LINE_AA)
        # else:
        #     # error_message = 'Cannot detect the whole body.'
        #     # frame = cv2.putText(frame, error_message, (20, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 1, cv2.LINE_AA)
        #     counter = self.__worker_mapper[sid][0].count(landmarks, exercise)
        #     frame = cv2.putText(frame, str(counter), (20, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 2, cv2.LINE_AA)
        # if self.check_visibility([landmarks.landmark[idx] for idx in self.__visibility_points]):
        #     counter = self.__worker_mapper[sid][0].count(landmarks, exercise)
        #     frame = cv2.putText(frame, str(counter), (20, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 2, cv2.LINE_AA)
        # if self.check_visibility([landmarks.landmark[idx] for idx in self.__visibility_points]):
        #     counter = self.__worker_mapper[sid][0].count(landmarks, exercise)
        #     frame = cv2.putText(frame, str(counter), (20, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 2, cv2.LINE_AA)
        try:
            if self.check_visibility([landmarks.landmark[idx] for idx in self.__visibility_points]):
                counter = self.__worker_mapper[sid][0].count(landmarks, exercise)
                # frame = cv2.putText(frame, str(counter), (20, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 2, cv2.LINE_AA)
        except:
            pass

        # string_frame = frame_encode(frame)
        return str(counter)