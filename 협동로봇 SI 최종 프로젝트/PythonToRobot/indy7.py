from indy_utils import indydcp_client as client
from profunc import *
from server import *
import time


class Indy7(client.IndyDCPClient):

    def __init__(self, IP, robot_name="NRMK-Indy7"):
        super().__init__(IP, robot_name)
        self.queue = MyQueue()
        t = Thread(target=self.action, args=())
        t.setDaemon(True)
        t.start()
        self.lift = LiftConnect()

        self.set_task_vel_level(3)
        self.set_joint_vel_level(3)

        self.J_our_home()
        self.wait_movedone()

    def action(self):
        while True:
            temp = self.queue.dequeue()
            if temp[0] == -1:
                pass
            elif temp[0] == 0:
                self.home()
            elif temp[0] == 1:
                self.pick_basket1()
                self.place_basket()
            elif temp[0] == 2:
                self.lift.sendData(0, 0)
                self.pick_basket2()
                self.slide()
                self.hang_basket()

    def home(self):
        print("홈위치")
        time.sleep(10)

    def pick_basket1(self):
        self.T_pick_basket1_approach()
        self.wait_movedone()

        self.set_task_vel_level(1)
        self.set_joint_vel_level(1)

        self.T_pick_basket1()
        self.wait_movedone()

        self.Endtool_on()
        self.wait_movedone()
        print("바스켓 pick")

        self.T_pick_basket1_retreat()
        self.wait_movedone()

    def place_basket(self, frytime=10):
        print("바스켓 배치")
        self.J_passpoint_to_fryer()
        self.wait_movedone()

        self.T_place_fryer_approach()
        self.wait_movedone()
        self.lift.sendData(1, frytime)
        input("다음 실행하려면 아무키나 누르세요")
        self.lift.sendData(0, frytime)
        self.pick_basket2()

    def pick_basket2(self):
        print("바스켓 회수")
        time.sleep(3)
        self.slide()

    def slide(self):
        self.T_passpoint_to_2nd_floor()
        self.wait_movedone()

        self.T_passpoint_slide()
        self.wait_movedone()

        self.T_pour_to_2nd_floor()
        self.wait_movedone()

        print("완성품 세팅")

        self.T_passpoint1_sort_basket()
        self.wait_movedone()

        self.J_passpoint2_sort_basket()
        self.wait_movedone()

        self.J_passpoint3_sort_basket()
        self.wait_movedone()
        self.hang_basket()

    def hang_basket(self):
        self.J_passpoint4_sort_basket()
        self.wait_movedone()

        self.J_passpoint5_sort_basket()
        self.wait_movedone()

        self.J_passpoint6_sort_basket()
        self.wait_movedone()

        self.J_passpoint7_sort_basket()
        self.wait_movedone()

        self.Endtool_off()
        self.wait_movedone()

        self.T_fall_out()
        self.wait_movedone()
        print("바스켓 반납")
        self.set_task_vel_level(3)
        self.set_joint_vel_level(3)

        self.J_Reset1()
        self.wait_movedone()

        self.J_Reset2()
        self.wait_movedone()

        self.J_our_home()

    # ------------------------------------------------------------------------------------
    def J_our_home(self):
        j_our_home = [-89.99981840780552, -0.0037226401084713193, -90.01103172618103, 0.0003263265779703185,
                      -90.03002204517921, -179.99989122448588]
        self.joint_move_to(j_our_home)

    def T_pick_basket1_approach(self):
        t_pick_basket1_approach = [-0.14087330865584913, -0.346308065184281, 0.527268842188829, 3.48242442648169,
                                   178.6218358474947, 87.45428187903917]
        self.task_move_to(t_pick_basket1_approach)

    def T_pick_basket1(self):
        t_pick_basket1 = [-0.1365803176928659, -0.34063943342912456, 0.19705038846129055, 2.8603028677505886,
                          178.49196609680894, 87.43113320736424]
        self.task_move_to(t_pick_basket1)
        sleep(2)

    def Endtool_on(self):
        endtool_type = 0  # endtool의 타입 NPN, PNP 주의!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.set_endtool_do(endtool_type, 1)  # val: 0(off), 1(on)
        sleep(2)

    def T_pick_basket1_retreat(self):
        t_pick_basket1_retreat = [-0.1368622812699031, -0.3381326135203002, 0.5297096288527345, 2.840312047926441,
                                  177.93190060845183, 87.33751655124492]
        self.task_move_to(t_pick_basket1_retreat)

    def J_passpoint_to_fryer(self):
        j_passpoint_to_fryer = [-24.554806543777445, -8.634618333549122, -77.30298255101233, 3.527971022200109,
                                -92.42661882155622, -116.68894550588641]
        self.joint_move_to(j_passpoint_to_fryer)

    def T_place_fryer_approach(self):
        t_place_fryer_approach = [0.3119623584986179, -0.020689869774128827, 0.5244105142035682, 2.0376272047752226,
                                  177.59452909010582, 86.9390412179323]
        self.task_move_to(t_place_fryer_approach)

    def T_passpoint_to_2nd_floor(self):
        t_passpoint_to_2nd_floor = [0.1385888590918166, -0.41709087635494546, 0.5669264557049524, 2.047925721035945,
                                    179.35041708467875, 88.46534629673086]
        self.task_move_to(t_passpoint_to_2nd_floor)

    def T_passpoint_slide(self):
        t_passpoint_slide = [0.03745110556135746, -0.4855739785391268, 0.3888675625703806, 83.99488623087684,
                             112.60233430569355, 64.99350617219253]
        self.task_move_to(t_passpoint_slide)

    def T_pour_to_2nd_floor(self):
        t_pour_to_2nd_floor = [-0.08232755397954138, -0.57931247215668, 0.2780599737170836, -167.38849262372878,
                               111.4343771469606, 170.22225783673193]
        self.task_move_to(t_pour_to_2nd_floor)

    def T_passpoint1_sort_basket(self):
        t_passpoint1_sort_basket = [0.008150948277363937, -0.4826226628135446, 0.5265838682080016, 67.73305246893793,
                                    123.40028444862132, 43.36388755584706]
        self.task_move_to(t_passpoint1_sort_basket)

    def J_passpoint2_sort_basket(self):
        j_passpoint2_sort_basket = [-58.6881022808019, 10.161627146824017, -98.70062709840526, 52.57697681389579,
                                    -13.156889358370297, -100.50853162709511]
        self.joint_move_to(j_passpoint2_sort_basket)

    def J_passpoint3_sort_basket(self):
        j_passpoint3_sort_basket = [-41.35594391626048, 10.775771968621578, -92.73023873321893, 28.769059889389272,
                                    13.233195389852357, -73.03319345606917]
        self.joint_move_to(j_passpoint3_sort_basket)

    def J_passpoint4_sort_basket(self):
        j_passpoint4_sort_basket = [-37.71574666677676, 10.778087269176847, -88.79023276085296, 34.06403494353566,
                                    57.41933690439735, -0.7167763285118046]
        self.joint_move_to(j_passpoint4_sort_basket)

    def J_passpoint5_sort_basket(self):
        j_passpoint5_sort_basket = [-57.13644232632091, -5.112864596784944, -107.75712951156443, 30.716413743427143,
                                    95.69429001006199, 45.62970151995969]
        self.joint_move_to(j_passpoint5_sort_basket)

    def J_passpoint6_sort_basket(self):
        j_passpoint6_sort_basket = [-57.35694065567269, -27.419105718945506, -94.25284393563379, 34.03635157217118,
                                    115.2080211072941, 67.47916948677734]
        self.joint_move_to(j_passpoint6_sort_basket)

    def J_passpoint7_sort_basket(self):
        j_passpoint7_sort_basket = [-56.19529534962922, -33.56513913998155, -95.96702890948463, 33.806889600095055,
                                    118.96050481513778, 76.66705745282064]
        self.joint_move_to(j_passpoint7_sort_basket)
        sleep(2)

    def Endtool_off(self):
        endtool_type = 0  # endtool의 타입 NPN, PNP 주의!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.set_endtool_do(endtool_type, 0)  # val: 0(off), 1(on)

    def T_fall_out(self):
        t_fall_out = [-0.007068528382587114, -0.4888100994476967, 0.48283164697999825, -143.17062262369143,
                      -157.2828952853706, 159.71316323524456]
        self.task_move_to(t_fall_out)
        sleep(2)

    def J_Reset1(self):
        j_Reset1 = [-67.19592386041249, -32.99294211647945, -104.32617187500688, -69.73892665145881, 90.25676462910558,
                    76.66596969756074]
        self.joint_move_to(j_Reset1)

    def J_Reset2(self):
        j_Reset2 = [-41.89981255649811, -14.310600343815508, -81.65692794422026, 1.398309386602815, -84.01315821279947,
                    76.66194500309912]
        self.joint_move_to(j_Reset2)

    def wait_movedone(self):
        while True:
            status = self.get_robot_status()
            if status['movedone'] == 1:
                return


class MyQueue:
    head = 0
    tail = 0

    def __init__(self):
        self.head = 0
        self.tail = 0
        self.queue = {0: []}

    def enqueue(self, value):
        tailPoint = self.tail
        self.queue[tailPoint] = value
        self.tail = tailPoint + 1

    def dequeue(self):
        if self.head == self.tail:
            return [-1, 0]
        headPoint = self.head
        retValue = self.queue.pop(headPoint)
        self.head = headPoint + 1
        return retValue

    def cut_in_queue(self, value):
        cp = self.head
        while cp < self.tail:
            if self.queue[cp][0] == 1:
                mp = self.tail
                self.tail = mp + 1
                while cp < mp:
                    self.queue[mp] = self.queue[mp - 1]
                    mp = mp - 1
                self.queue[cp] = value
                return
            else:
                cp = cp + 1
        self.queue[cp] = value

    def append_queue(self, value):
        if value[0] == 2:
            self.cut_in_queue(value)
        else:
            self.enqueue(value)
        print(self.queue)

# print(status)
#
# indy.set_task_vel_level(3)
# indy.set_joint_vel_level(3)
#
# J_our_home()
# wait_movedone()
#
# T_pick_basket1_approach()
# wait_movedone()
#
# indy.set_task_vel_level(1)
# indy.set_joint_vel_level(1)
#
# T_pick_basket1()
# wait_movedone()
#
# Endtool_on()
# wait_movedone()
#
# T_pick_basket1_retreat()
# wait_movedone()
#
# J_passpoint_to_fryer()
# wait_movedone()
#
# T_place_fryer_approach()
# wait_movedone()
#
# explanation = input()
#
# if explanation == 1:
#     pass
#
# T_passpoint_to_2nd_floor()
# wait_movedone()
#
# T_passpoint_slide()
# wait_movedone()
#
# T_pour_to_2nd_floor()
# wait_movedone()
#
# T_passpoint1_sort_basket()
# wait_movedone()
#
# J_passpoint2_sort_basket()
# wait_movedone()
#
# J_passpoint3_sort_basket()
# wait_movedone()
#
# J_passpoint4_sort_basket()
# wait_movedone()
#
# J_passpoint5_sort_basket()
# wait_movedone()
#
# J_passpoint6_sort_basket()
# wait_movedone()
#
# J_passpoint7_sort_basket()
# wait_movedone()
#
# Endtool_off()
# wait_movedone()
#
# T_fall_out()
# wait_movedone()
#
# indy.set_task_vel_level(3)
# indy.set_joint_vel_level(3)
#
# J_Reset1()
# wait_movedone()
#
# J_Reset2()
# wait_movedone()
#
# J_our_home()
#
# indy.disconnect()
