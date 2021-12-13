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
        fleft = np.nan_to_num(np.mean(scanned[1:45][np.nonzero(scanned[1:45])]))
        left = np.nan_to_num(np.mean(scanned[45:135][np.nonzero(scanned[75:105])]))
        bleft = np.nan_to_num(np.mean(scanned[135:180][np.nonzero(scanned[145:180])]))

        return right, fright, front, fleft, left, bleft, bright

    def lds_callback(self, scan):
        right, fright, front, fleft, left, bleft, bright = self.init_ranges(scan.ranges)
        print(front)

        if right < 1:
            if front < 0.30:
                self.Turn_Right()
                print("turn right")

            elif left > 0.25:
                if fleft > bleft:
                    self.Semi_Left()
                    print("lil turn left", self.Semi_Left())
                elif fleft < bleft:
                    self.Semi_Right()
                    print("lil turn right", self.Semi_Right())


            elif left < 0.25:
                if fleft < bleft:
                    self.Turn_Right()
                    print("lil turn right", self.Semi_Right())

                else:
                    self.Semi_Left()
                    print("lil turn left", self.Semi_Left())

            else:
                 self.find_wall()
                 print("no left wall")

        # elif front > 1.5:
        #     if fleft > 0.5 or fleft == 0:
        #         self.Turn_Left()
        #         print("turn left")
        #
        #     elif left < 0.25 or fleft < bleft:
        #         self.Semi_Right()
        #         print("semi right")
        #
        #     elif left > 0.25 and fleft > bleft:
        #         self.Semi_Left()
        #         print("semi turn")
        #
        #     else:
        #         self.find_wall()
        #

        self.publisher.publish(self.turtle_vel)

    def Turn_Right(self):
        self.turtle_vel = Twist()
        self.turtle_vel.linear.x = 0.15
        self.turtle_vel.angular.z = -2.5

    def Turn_Left(self):
        self.turtle_vel = Twist()
        self.turtle_vel.linear.x = 0.15
        self.turtle_vel.angular.z = 3

    def Semi_Right(self):
        self.turtle_vel = Twist()
        self.turtle_vel.linear.x = 0.2
        self.turtle_vel.angular.z = -1.15

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