#!/home/pi/.pyenv/versions/rospy3/bin/python

import numpy as np
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import math


class SelfDrive:
    def __init__(self, publisher):
        self.publisher = publisher
        self.turtle_vel = Twist()
        self.count = 0

    def init_ranges(self, scan):
        scanned = np.array(scan)
        right = np.nan_to_num(np.mean(scanned[190:][np.nonzero(scanned[265:275])]))
        fright = np.nan_to_num(np.mean(scanned[275:340][np.nonzero(scanned[340:360])]))
        bright = np.nan_to_num(np.mean(scanned[245:265][np.nonzero(scanned[245:265])]))
        front = np.nan_to_num(np.mean((scanned[340:360] + scanned[0:20])[np.nonzero(scanned[340:360] + scanned[0:20])]))
        fleft = np.nan_to_num(np.mean(scanned[30:75][np.nonzero(scanned[30:75])]))
        bleft = np.nan_to_num(np.mean(scanned[100:140][np.nonzero(scanned[100:140])]))
        left = np.nan_to_num(np.mean(scanned[75:100][np.nonzero(scanned[75:100])]))

        self.count += 1
        return right, fright, front, fleft, left, bleft, bright

    def lds_callback(self, scan):
        right, fright, front, fleft, left, bleft, bright = self.init_ranges(scan.ranges)
        print(right, fright, front, fleft, left)
        direct = 0
        # if front > 3 and left > 3 and right > 3:
        #     self.find_wall()
        #     print("find wall")
        #
        # elif direct == 0:
        #     if  left < 0.25 and right > 0.25:
        #         direct = 1
        #         print("left wall: ", left)
        #
        #     # elif right < 0.25 and right > 0.25:
        #     #     direct = -1
        #     #     print("right wall:", right*100)
        #
        #     else:
        #         print("find the wall")

        if direct == 0:  # 왼쪽 벽

            if left > 0.25 and front > 0.25 or fleft > bleft:
                self.Semi_Left()
                print("lil turn left", self.Semi_Left())

            elif left < 0.25 and front > 0.25 or fleft < bleft:
                self.Semi_Right()
                print("lil turn right", self.Semi_Right())

            elif front < 0.25:
                self.Turn_Right()
                print("turn left")
            else:
                print("no left wall")

        # elif direct == -1:  #오른쪽 벽
        #
        #     if right > 0.25 and front > 0.25:
        #         self.Semi_Left()
        #         print("lil turnt left")
        #
        #     elif right < 0.25 and front > 0.25:
        #         self.Semi_Right()
        #         print("lil semi right")
        #
        #     elif front < 0.25:
        #         self.Turn_Left()
        #         print("turn left")
        #     else:
        #         print("no right wall")

        self.publisher.publish(self.turtle_vel)

    def find_wall(self):
        self.turtle_vel = Twist()
        self.turtle_vel.linear.x = 0.1
        self.turtle_vel.angular.z = 0

    def Turn_Right(self):
        self.turtle_vel = Twist()
        self.turtle_vel.linear.x = 0.0
        self.turtle_vel.angular.z = -0.3

    def Follow_Wall(self):
        self.turtle_vel = Twist()
        self.turtle_vel.linear.x = 0.15
        self.turtle_vel.angular.z = 0

    def Turn_Left(self):
        self.turtle_vel = Twist()
        self.turtle_vel.linear.x = 0.0
        self.turtle_vel.angular.z = 0.3

    def Semi_Right(self):
        self.turtle_vel = Twist()
        self.turtle_vel.linear.x = 0.195
        self.turtle_vel.angular.z = -0.25

    def Semi_Left(self):
        self.turtle_vel = Twist()
        self.turtle_vel.linear.x = 0.195
        self.turtle_vel.angular.z = 0.25
        # return turtle_vel


def main():
    rospy.init_node('self_drive')
    publisher = rospy.Publisher('cmd_vel', Twist, queue_size=1)
    driver = SelfDrive(publisher)
    subscriber = rospy.Subscriber('scan', LaserScan,
                                  lambda scan: driver.lds_callback(scan))
    rospy.spin()


if __name__ == "__main__":
    main()