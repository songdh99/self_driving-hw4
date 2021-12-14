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
        front = scanned[0]
        point = scanned[70]
        point2 = scanned[80]
        point3 = scanned[90]
        fleft = np.nan_to_num(np.mean(scanned[1:45][np.nonzero(scanned[1:45])]))
        left = np.nan_to_num(np.mean(scanned[45:135][np.nonzero(scanned[45:135])]))
        bleft = np.nan_to_num(np.mean(scanned[135:180][np.nonzero(scanned[135:180])]))

        return right, fright, front, fleft, left, bleft, bright, point, point2, point3

    def lds_callback(self, scan):
        right, fright, front, fleft, left, bleft, bright, point, point2, point3 = self.init_ranges(scan.ranges)
        print(point, point2)
        if point3 > 0.5 and front > 0.3:
            self.turtle_vel.linear.x = 0.15
            self.turtle_vel.angular.z = 0

        elif 0 < front < 0.30:
            self.Turn_Right()
            print("turn right")


        elif point2 > 0.45 or point2 == 0 or point-point3 > 0.07:
            self.Turn_Left()
            print("outside turn left")



        # elif left > 0.25:
        #     if fleft > bleft:
        #         self.Semi_Left()
        #         print("lil turn left")
        #
        #     elif fleft < bleft:
        #         self.Semi_Right()
        #         print("lil turn right")

        elif left <= 0.25:
            if fleft < bleft:
                self.Semi_Right()
                print("lil turn right")

            elif fleft > bleft:
                self.Semi_Left()
                print("lil turn left")

        else:
            self.turtle_vel.linear.x = 0.15
            self.turtle_vel.angular.z = 0.1
            print("stright")
        self.publisher.publish(self.turtle_vel)

    def Turn_Right(self):
        self.turtle_vel = Twist()
        self.turtle_vel.linear.x = 0.15
        self.turtle_vel.angular.z = -2.7

    def Turn_Left(self):
        self.turtle_vel = Twist()
        self.turtle_vel.linear.x = 0.15
        self.turtle_vel.angular.z = 1.4

    def Semi_Right(self):
        self.turtle_vel = Twist()
        self.turtle_vel.linear.x = 0.22
        self.turtle_vel.angular.z = -1.5

    def Semi_Left(self):
        self.turtle_vel = Twist()
        self.turtle_vel.linear.x = 0.2
        self.turtle_vel.angular.z = 0.5
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