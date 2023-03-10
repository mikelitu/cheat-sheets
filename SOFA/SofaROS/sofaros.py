# coding: utf8
# Code based on the example provided at the SoftRobots plugin
import Sofa.Core as SC
import rclpy


class RosSender(SC.Controller):

    def __init__(self, *args, **kwargs) -> None:
        SC.Controller.__init__(self, *args, **kwargs)
        self.name = "RosSender"

        #Args
        self.node = args[0]
        rosname = args[1]
        self.datafield = args[2]
        msgtype = args[3]
        self.sendingcb = args[4]

        # Create or connect to the topic rosname as a publisher
        self.pub = self.node.create_publisher(msgtype, rosname, 1)

        print("Publisher created!")
        

    def onAnimateEndEvent(self, event):
        data = self.sendingcb(self.datafield)
        self.pub.publish(data)
        


class RosReceiver(SC.Controller):

    def __init__(self, *args, **kwargs) -> None:
        SC.Controller.__init__(self, *args, **kwargs)
        self.name = "RosReceiver"

        self.node = args[0]
        rosname = args[1]
        self.datafield = args[2]
        msgtype = args[3]
        self.recvcb = args[4]

        # Create or connect to the topic rosname as a subscription
        self.sub = self.node.create_subscription(msgtype, rosname, self.callback, 1)
        # rclpy.spin(self.node)

        self.data = None

    
    def callback(self, data):
        self.data = data.data
    
    def onAnimateBeginEvent(self, event):
        rclpy.spin_once(self.node, timeout_sec=0.001) # This line invokes the subscriber callback once for 0.001 seconds
        if self.data is not None:
            self.recvcb(self.data, self.datafield)
            self.data = None


def init(nodeName="Sofa"):
    rclpy.init()
    node = rclpy.create_node(nodeName)
    node.get_logger().info('Created node')
    return node
