#!/home/pi/.pyenv/versions/rospy3/bin/python

import numpy as np
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import math


class SelfDrive:
    def __init__(self, publisher):
        self.publisher = publisher


    def lds_callback(self, scan):
        front, front_left, front_right, left_side, right_side, hyp2 = self.init_ranges(scan.ranges)
        if hyp2 - 3 <= front_right <= hyp2 + 3 and 23 <= right_side <= 27:
            print("Go straight mode")
            if right_side >= 25:
                print("go around right")
            elif right_side <= 25:
                print("go around left")
            else:
                print("find walls")

        else:
            print('front_right minimum', np.round(((hyp2) - 3), 2))
            print('front_right maximum', np.round(((hyp2) + 3), 2))
            print('right_side minimum', right_side)
            print("Find walls")


        # if left <= 0.25:
        #     turtle_vel.linear.x = 0.15
        # elif
        #
        #
        # # scan 분석 후 속도 결정
        # print("scan[0]:", scan.ranges[0])
        # turtle_vel = Twist()
        # # 전진 속도 및 회전 속도 지정
        # turtle_vel.angular.z = 0.0
        # # 장애물 발견시 정지
        # # if scan.ranges[0] == 0.0:
        # #     turtle_vel.linear.x = 0.15
        # # elif scan.ranges[0] < 0.25:
        # #     turtle_vel.linear.x = 0
        # # else:
        # #     turtle_vel.linear.x = 0.15
        #
        #  # 속도 출력
        # self.publisher.publish(turtle_vel)

    def init_ranges(self, scanned):
        right_side = scanned[-90] * 100
        left_side = scanned[90] * 100
        front = scanned[0] * 100
        front_right = scanned[-60] * 100
        behind_right = scanned[-120] * 100
        front_left = scanned[60] * 100
        hyp = (right_side * 2) / math.sqrt(3)
        hyp2 = right_side / math.cos(30)

        return np.round(front,2), np.round(front_left,2), np.round(front_right,2), np.round(left_side,2), np.round(right_side,2), hyp


def main():
    rospy.init_node('self_drive')
    publisher = rospy.Publisher('cmd_vel', Twist, queue_size=1)
    driver = SelfDrive(publisher)
    subscriber = rospy.Subscriber('scan', LaserScan,
                                  lambda scan: driver.lds_callback(scan))
    rospy.spin()

if __name__ == "__main__":
    main()
