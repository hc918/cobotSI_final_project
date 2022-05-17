# 시뮬레이션 컨트롤 부분, import해서 사용할 것.

import sim
# from PIL import Image, ImageFilter, ImageDraw
import time


class MyError(Exception):
    pass


class env:
    # 시뮬레이션과 연결을 수립합니다.
    # 시뮬레이션과 Python 프로그램이 같은 컴퓨터에서 실행된다면 변경할 필요가 없습니다. 
    # 만약 Coppliasim에서 설정이 바뀌었거나, 다른 컴퓨터에서 실행된다면 해당 부분을 정의해 주세요.
    def __init__(self, ip="127.0.0.1", port=19997):  # "114.70.60.219", "127.0.0.1","192.168.9.2"
        self.id = sim.simxStart(ip, port, False, False, 5000, 5)
        self.logdata = []
        self.realtime = True

    # 시뮬레이션을 시작합니다.
    def start(self):
        if sim.simxStartSimulation(self.id, sim.simx_opmode_blocking) != 0:
            sim.simxStopSimulation(self.id, sim.simx_opmode_blocking)
            sim.simxFinish(self.id)
            raise MyError()
        else:
            return sim.simxStartSimulation(self.id, sim.simx_opmode_blocking)

    # 시뮬레이션을 중단합니다.
    def stop(self):
        return sim.simxStopSimulation(self.id, sim.simx_opmode_blocking)

    # 시뮬레이션 내의 특정 오브젝트를 return합니다. name에는 오브젝트의 이름을 입력받습니다. 반환갑이 0이 아닌 수라면 정상적으로 실행된 것입니다.
    def getobject(self, name):
        rtn, handle = sim.simxGetObjectHandle(self.id, name, sim.simx_opmode_blocking)
        # print("핸들 : ",handle)
        return handle

    # 시뮬레이션 내의 특정 센서의 handle을 입력 받아 읽은 값을 return합니다.
    def readproximitysensor(self, handle):
        rtn1, value, rtn2, rtn3, rtn4 = sim.simxReadProximitySensor(
            self.id, handle, sim.simx_opmode_blocking)
        return value

    # 시뮬레이션 내에 실수 신호를 읽습니다.
    def getfloatsignal(self, name):
        rtn, value = sim.simxGetFloatSignal(self.id, name, sim.simx_opmode_streaming)
        return value

    # 시뮬레이션 내에 32비트 정수 신호를 읽습니다.
    def getintegersignal(self, name):
        rtn, value = sim.simxGetIntegerSignal(
            self.id, name, sim.simx_opmode_blocking)
        return value

    # 시뮬레이션 내에 32비트 정수 신호를 입력합니다.
    def setintegersignal(self, name, value):
        rtn = sim.simxSetIntegerSignal(
            self.id, name, value, sim.simx_opmode_blocking)
        return rtn

    # 시뮬레이션 내에 문자열 신호를 set합니다.
    def setstringsignal(self, name, data):
        rtn = sim.simxSetStringSignal(self.id, name, data, sim.simx_opmode_blocking)
        return rtn

    # 시뮬레이션 내에 문자열 신호를 읽습니다.
    def getstringsignal(self, name):
        rtn, data = sim.simxGetStringSignal(self.id, name, sim.simx_opmode_blocking)
        return data

    def clearstringsignal(self, name):
        rtn = sim.simxClearStringSignal(self.id, name, sim.simx_opmode_blocking)
        return rtn

    # 특정 오브젝트와 좌표값(x,y,z) 을 입력받아서 해당 오브젝트의 좌표를 변경합니다.
    def setobjectpos(self, handle, pos):
        rtn = sim.simxSetObjectPosition(
            self.id, handle, -1, pos, sim.simx_opmode_blocking)
        return rtn

    # 특정 오브젝트를 입력받아서 해당 오브젝트의 좌표 (x,y,z)를 반환합니다.
    def getobjectpos(self, handle):
        rtn, pos = sim.simxGetObjectPosition(
            self.id, handle, -1, sim.simx_opmode_blocking)
        return pos

    # 비전 센서 핸들을 입력받아서 비전 센서 해상도와 이미지를 반환합니다. 
    # def getvision(self, handle):
    #     rtn = 1
    #     while rtn != 0:
    #         rtn, res, img = sim.simxGetVisionSensorImage(self.id, handle, 0, sim.simx_opmode_blocking)
    #         time.sleep(0.01)
    #         if len(res) <= 2:
    #             continue
    #     image_byte_array = np.array(img, dtype=np.uint8)
    #     #print(res)
    #     im = Image.frombytes("RGB", res, image_byte_array, "raw", "RGB", 0, 1)
    #     return res, im.crop((0, 100, res[0], res[1]-100))

    # 상대 좌표를 출력합니다. 원래 좌표 (x,y,z)와 이동할 좌표 (x,y,z)를 입력받으면 원래 좌표로부터 상대 좌표를 반환합니다.
    def transpose(self, pos, offset):
        rtn = []
        for i in range(3):
            rtn.append(pos[i] + offset[i])
        return rtn

    # 내장된 log list에 특정 로그를 남깁니다.
    def log(self, text):
        logdata = {}
        try:
            logdata['logtime'] = time.strftime('%X/%Y%m%d', time.localtime(time.time()))
            logdata['text'] = text
            self.logdata.append(logdata)
            return True
        except:
            print("로그 기록 실패")
            return False

    # 시뮬레이션과의 연결을 종료합니다.
    def finish(self):
        sim.simxFinish(self.id)


class bot:
    # 타겟과 비전 객체의 이름을 받습니다. env 객체를 먼저 생성해서 초기화해야 합니다.
    def __init__(self, env, target, tip, vision=False):
        self.env = env
        self.target = self.env.getobject(target)
        self.tip = self.env.getobject(tip)
        self.tickimg = None
        self.currentvision = None
        self.lasttime = 0
        self.lock = False
        self.vision = False
        if (vision != False):
            self.vision = self.env.getobject(vision)

    # 현재 시점의 vision센서 값을 return합니다. 비전 센서 값이 정의되어 있지 않으면 False를 Return합니다.
    def getcurrentvision(self, rqtime, realtime=False):
        if (self.vision != False):
            # 실시간 이미지를 Return할건지 여부를 결정합니다. 기본은 0.1초 제한이 걸려 있습니다.
            if realtime == False:
                # 전에 저장된 값보다 0.1초는 뒤에 호출되어야 합니다.
                if (rqtime > self.lasttime + 100):
                    if self.currentvision == None:
                        res, img = self.env.getvision(self.vision)
                        self.currentvision = img
                    self.lasttime = rqtime
            else:
                res, img = self.env.getvision(self.vision)
                self.currentvision = img
            return self.currentvision
        return False

    # 특정한 시점의 이미지를 고정합니다.
    # 해당 이미지를 객체 안에 저장하고 해상도 값을 반환합니다.
    def setvision(self):
        res, img = self.env.getvision(self.vision)
        self.tickimg = img
        return res

    # 위에서 저장한 이미지를 호출합니다.
    def gettickimg(self):
        if self.tickimg == None:
            self.setvision()
        return self.tickimg

    # 현재 target의 좌표를 출력합니다.
    def getrobotposition(self):
        return self.env.getobjectpos(self.target)

    # 로봇을 절대 좌표 (x,y,z) 로 이동합니다. sleep은 target을 이동한 후에 대기할 시간을 지정합니다.
    def moveabs(self, pos, sleep=0):
        self.env.setobjectpos(self.target, pos)
        tipos = self.env.getobjectpos(self.tip)
        done = False
        while self.lock == True:
            time.sleep(0.1)

        while done == False:
            print(tipos)
            print(pos)
            for i in range(3):
                # if False:
                if round(pos[i], 5) != round(tipos[i], 5):
                    tipos = self.env.getobjectpos(self.tip)
                    done = False
                    break
                else:
                    done = True
            time.sleep(sleep)
        return

    # 현재 로봇을 상대 좌표만큼 이동합니다. (x,y,z) sleep은 target을 이동한 후에 대기할 시간을 지정합니다.
    def moverelative(self, pos, sleep=0):
        relpos = self.env.transpose(self.env.getobjectpos(self.target), pos)
        self.moveabs(relpos, sleep)
        return
