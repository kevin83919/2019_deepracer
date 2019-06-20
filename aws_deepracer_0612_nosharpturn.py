# {
#     "all_wheels_on_track": Boolean,    # flag to indicate if the vehicle is on the track
#     "x": float,                        # vehicle's x-coordinate in meters
#     "y": float,                        # vehicle's y-coordinate in meters
#     "distance_from_center": float,     # distance in meters from the track center
#     "is_left_of_center": Boolean,      # Flag to indicate if the vehicle is on the left side to the track center or not.
#     "heading": float,                  # vehicle's yaw in degrees
#     "progress": float,                 # percentage of track completed
#     "steps": int,                      # number steps completed
#     "speed": float,                    # vehicle's speed in meters per second (m/s)
#     "steering_angle": float,           # vehicle's steering angle in degrees
#     "track_width": float,              # width of the track
#     "waypoints": [[float, float], … ], # list of [x,y] as milestones along the track center
#     "closest_waypoints": [int, int]    # indices of the two nearest waypoints.
# }

import math

def reward_function(params):

    # Read input variables
	all_wheels_on_track = params['all_wheels_on_track']
	speed = params['speed']
	waypoints = params['waypoints']
	closest_waypoints = params['closest_waypoints']
	heading = params['heading']
	track_width = params['track_width']
	distance_from_center = params['distance_from_center']
	steering = abs(params['steering_angle'])
	steps = params['steps']
	progress = params['progress']

	# Initialize the reward with typical value
	reward = 1.0

	if progress == 100:
		reward += 10000
	else:

		#############################################################################
		'''
		Example of using all_wheels_on_track and speed
		'''
		# Set the speed threshold based your action space
		SPEED_THRESHOLD = 1.0

		if not all_wheels_on_track:
			# Penalize if the car goes off track
			reward -= 1000
		elif speed < SPEED_THRESHOLD:
			# Penalize if the car goes too slow
			reward -= 5
		else:
			# High reward if the car stays on track and goes fast
			reward += 10

		###############################################################################
		'''
		Example of using waypoints and heading to make the car in the right direction
		'''
		# Calculate the direction of the center line based on the closest waypoints
		next_point = waypoints[closest_waypoints[1]]
		prev_point = waypoints[closest_waypoints[0]]

		# Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
		track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
		# Convert to degree
		track_direction = math.degrees(track_direction)

		# Calculate the difference between the track direction and the heading direction
		direction_diff = abs(track_direction - heading)

		# Penalize the reward if the difference is too large
		DIRECTION_THRESHOLD = 10.0
		if direction_diff > DIRECTION_THRESHOLD:
			reward -= 10

		#################################################################################
		'''
		Example of using distance from the center
		'''
		# Penalize if the car is too far away from the center
		marker_1 = 0.1 * track_width
		marker_2 = 0.5 * track_width

		if distance_from_center <= marker_1:
		    reward += 10.0
		elif distance_from_center <= marker_2:
		    reward += 5
		else:
		    reward -= 2  # likely crashed/ close to off track

		##################################################################################
		# #Example of using steering angle
		# # Penalize if car steer too much to prevent zigzag
		# STEERING_THRESHOLD = 20.0
		# if steering > STEERING_THRESHOLD:
		#     reward -= 20

		#############################################################################
		'''
		#Example of using steps and progress
		'''
		# Total num of steps we want the car to finish the lap, it will vary depends on the track length
		TOTAL_NUM_STEPS = 300

		# Give additional reward if the car pass every 100 steps faster than expected
		if (steps % 100) == 0 and progress > (steps / TOTAL_NUM_STEPS) :
			reward += 10.0

		#############################################################################
		'''
		#Example of using track width
		'''
		# Calculate the distance from each border
		distance_from_border = 0.5 * track_width - distance_from_center

		# Reward higher if the car stays inside the track borders
		if distance_from_border >= 0.05:
			reward += 10.0
		else:
			reward -= 100 # Low reward if too close to the border or goes off the track

		############################################################################
		'''
		# Kevin's code
		'''
		# Reward finish the lap
		if progress >= 1:
		    reward += progress * 100


	return reward
