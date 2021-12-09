#!/home/pi/.pyenv/versions/rospy3/bin/python

import numpy as np
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import math


class SelfDrive:
    def __init__(self, publisher):
        self.publisher = publisher



    def init_ranges(self, scanned):
        right_side = scanned[-90] * 100
        left_side = scanned[90] * 100
        front = scanned[0] * 100
        front_right = scanned[-60] * 100
        behind_right = scanned[-120] * 100
        front_left = scanned[60] * 100
        hyp = right_side / math.cos(math.pi*(30/180))
        around = scanned[0:360] *100


        right = scanned[-90:-60] * 100
        fright = scanned[-30:-60] * 100
        front = scanned[-30:30] * 100
        fleft = scanned[30:60] * 100
        left = scanned[60:90] * 100

        return np.round(front,2), np.round(front_left,2), np.round(front_right,2), np.round(left_side,2), np.round(right_side,2), hyp, around

    def act_ros(self, scan):
        global turtle_vel
        turtle_vel = Twist()
        front, front_left, front_right, left_side, right_side, hyp = self.init_ranges(scan.ranges)
        if 25 < front < 50:
            self.go()
            if front_left < hyp and left_side < 25:
                self.semi_turn_left()
            elif front_left > hyp and left_side < 25:
                self.semi_turn_left()
            elif front_left < hyp and left_side > 25:
                self.semi_turn_right()
            elif front_left > hyp and left_side > 25:
                self.semi_turn_right()
        elif 0 <= front <= 25 and hyp-1 < front_left < hyp+1 and 26 < left_side < 27:
            self.turn_right()
        elif 50 <= front <= 100 and 50 <= front_left <= 100 and 50 <= left_side <= 100:
            self.find_wall()
        self.publisher.publish(turtle_vel)



    def turn_left(self):
        turtle_vel = Twist()
        turtle_vel.linear.x = 0.05
        turtle_vel.angular.z = 0.3
        return turtle_vel
    def semi_turn_left(self):
        turtle_vel = Twist()
        turtle_vel.linear.x = 0.15
        turtle_vel.angular.z = 0.01
        return turtle_vel
    def semi_turn_right(self):
        turtle_vel = Twist()
        turtle_vel.linear.x = 0.15
        turtle_vel.angular.z = -0.01
        return turtle_vel

    def find_wall(self):
        turtle_vel =Twist()
        turtle_vel.linear.x = 0.15
        turtle_vel.angular.z = -0.03
        return turtle_vel
    def go(self):
        turtle_vel = Twist()
        turtle_vel.linear.x = 0.15
        return turtle_vel







    # def lds_callback(self, scan):
    #     front, front_left, front_right, left_side, right_side, hyp = self.init_ranges(scan.ranges)
    #     if hyp - 3 <= front_right <= hyp + 3 and 23 <= right_side <= 27:
    #         print("Go straight mode")
    #         if right_side >= 25 and front_right >= hyp:
    #             print("go around right")
    #         elif right_side < 25 and front_right <= hyp:
    #             print("go around left")
    #     else:
    #         print('front_right minimum', np.round(((hyp) - 3), 2))
    #         print('front_right maximum', np.round(((hyp) + 3), 2))
    #         print('right_side minimum', right_side)
    #         print("Find walls")
    #     self.publisher.publish(turtle_vel)

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



def main():
    rospy.init_node('self_drive')
    publisher = rospy.Publisher('cmd_vel', Twist, queue_size=1)
    driver = SelfDrive(publisher)
    subscriber = rospy.Subscriber('scan', LaserScan,
                                  lambda scan: driver.act_ros(scan))
    rospy.spin()

if __name__ == "__main__":
    main()