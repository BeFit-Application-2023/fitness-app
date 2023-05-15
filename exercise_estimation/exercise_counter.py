import json
from scipy.spatial.distance import cosine


class ExerciseCounter:
    def __init__(self, mapping_exercise, previous_state=None):
        self.mapping_exercise = mapping_exercise
        # self.exercise_count = current_number_exercises
        self.previous_state = 1 if previous_state is None else previous_state
        with open('exercise_estimation/exercise_metrics.json', 'rb') as file:
            self.exercise_static_information = json.load(file)

    def count(self, landmarks, exercise):

        origin = int(landmarks.landmark[self.exercise_static_information[exercise]['origin']].y * 700)
        reference_point_1 = int(landmarks.landmark[self.exercise_static_information[exercise]['reference-points'][0]].y * 700)
        reference_point_2 = int(landmarks.landmark[self.exercise_static_information[exercise]['reference-points'][1]].y * 700)

        state = 0 if cosine([origin, reference_point_1], [origin, reference_point_2]) < \
            self.exercise_static_information[exercise]['threshold-value'] else 1
        
        if self.previous_state == 0 and state == 1:
            self.mapping_exercise[exercise] -= 1
        self.previous_state = state
        
        return self.mapping_exercise[exercise]