import rospy
import rosbag
import argparse
import numpy as np
from tf.transformations import euler_from_quaternion

import matplotlib.pyplot as plt



def main(args):
    bag = rosbag.Bag(args.bag_file)
    ground_truth_poses = []
    estimate_poses = []
    for topic, msg, t in bag.read_messages(topics=[args.ground_truth_topic, args.estimated_topic]):
        # Construct numpy array from the message
        # Convert quaternion to euler angles
        quat = [
            msg.pose.orientation.x,
            msg.pose.orientation.y,
            msg.pose.orientation.z,
            msg.pose.orientation.w
        ]
        euler = euler_from_quaternion(quat)

        pose = [
            msg.pose.position.x,
            msg.pose.position.y,
            euler[2]
        ]

        if(topic == args.ground_truth_topic):
            ground_truth_poses.append(pose)

        elif(topic == args.estimated_topic):
            estimate_poses.append(pose)


    bag.close()

    ground_truth_poses = np.stack(ground_truth_poses)
    estimate_poses = np.stack(estimate_poses)

    # Plot the ground truth and estimated poses
    plt.figure()
    plt.plot(ground_truth_poses[:,0], ground_truth_poses[:,1], 'b-', label='Ground Truth')
    plt.plot(estimate_poses[:,0], estimate_poses[:,1], 'r-', label='Estimated')



if __name__ == "__main__":

    # Add argument for path to bag file
    parser = argparse.ArgumentParser(description='Visualize bag file')
    parser.add_argument('--bag_file', type=str, help='Path to bag file')
    parser.add_argument('--ground_truth_topic', type=str, help='Topic to visualize')
    parser.add_argument('--estimated_topic', type=str, help='Topic to visualize')


    args = parser.parse_args()

    main(args)