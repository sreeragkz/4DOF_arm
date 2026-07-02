import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy, JointState

class ArmJoyMap(Node):
    def __init__(self):
        super().__init__('arm_joy_mapper')
        self.publisher = self.create_publisher(JointState,'/joint_states',10)
        self.subscriber = self.create_subscription(Joy,'/joy',self.joy_callback,10)

        self.base_angle = 0.0
        self.shoulder_angle = 0.0
        self.elbow_angle = 0.0
        self.wrist_angle = 0.0

    def joy_callback(self,joy_msg):
        self.base_angle += (joy_msg.axes[0]*0.05)
        self.shoulder_angle += (joy_msg.axes[1]*0.05)
        self.elbow_angle += (joy_msg.axes[4] * 0.05) 
        self.wrist_angle += (joy_msg.axes[3] * 0.05)

        self.shoulder_angle = max(min(self.shoulder_angle, 1.57),-1.57)
        self.elbow_angle = max(min(self.elbow_angle, 1.57),-1.57)
        self.wrist_angle = max(min(self.wrist_angle, 1.57),-1.57)

        joint_msg = JointState()

        joint_msg.header.stamp = self.get_clock().now().to_msg()

        joint_msg.name=(['base_rotate_joint','shoulder_joint','elbow_joint','wrist_joint'])
        joint_msg.position=([self.base_angle,self.shoulder_angle,self.elbow_angle,self.wrist_angle])

        self.publisher.publish(joint_msg)

def main(args=None):
    rclpy.init(args=args)
    arm_joy_mapper = ArmJoyMap()
    try:
        rclpy.spin(arm_joy_mapper)
    except KeyboardInterrupt:
        pass
    if rclpy.ok():
        arm_joy_mapper.destroy_node()
        rclpy.shutdown()

if __name__=="__main__":
    main()
