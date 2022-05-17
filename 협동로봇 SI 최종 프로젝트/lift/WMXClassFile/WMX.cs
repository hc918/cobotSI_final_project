using WMX3ApiCLR;

namespace WMXClassFile
{
    class WMX
    {
        public Communication communication;
        public MotorControl motor;

        // 모터 축 번호
        public enum Motor
        {
            AlignPusher = 0
        }

        public WMX()
        {
            communication = new Communication();
            motor = new MotorControl(communication.GetHandler());
        }

        /// <summary>
        /// 통신과 관련된 Class
        /// </summary>
        public class Communication
        {
            private WMX3Api wmxApi;
            private EngineStatus eStatus;
            private string EnginePath = @"C:\\Program Files\\SoftServo\\WMX3\\";

            public Communication()
            {
                wmxApi = new WMX3Api();
                eStatus = new EngineStatus();
            }

            /// <summary>
            /// 데이터를 주고 받을 통로 생성 함수.
            /// </summary>
            /// <returns></returns>
            public bool Open()
            {
                int ret = wmxApi.CreateDevice(EnginePath, DeviceType.DeviceTypeNormal);

                if (ret == ErrorCode.None)
                    return true;
                else
                    return false;
            }

            /// <summary>
            /// 생성한 통로 제거하는 함수.
            /// </summary>
            /// <returns></returns>
            public bool Close()
            {
                int ret = wmxApi.CloseDevice();

                if (ret == ErrorCode.None)
                    return true;
                else
                    return false;
            }

            /// <summary>
            /// Slave(모터,I/O)와 통신 연결 함수.
            /// </summary>
            /// <returns></returns>
            public bool StartCommunication()
            {
                if (!wmxApi.IsDeviceValid())
                    return false;

                int ret = wmxApi.StartCommunication();

                if (ret == ErrorCode.None)
                    return true;
                else
                    return false;
            }

            /// <summary>
            ///  Slave(모터,I/O)와 통신 연결 중지 함수.
            /// </summary>
            /// <returns></returns>
            public bool StopCommunication()
            {
                if (!wmxApi.IsDeviceValid())
                    return false;

                int ret = wmxApi.StopCommunication();

                if (ret == ErrorCode.None)
                    return true;
                else
                    return false;
            }

            public WMX3Api GetHandler()
            {
                return wmxApi;
            }
        }

        /// <summary>
        /// 모터를 제어하는 Class
        /// </summary>
        public class MotorControl
        {
            private WMX3Api wmxApi;
            private CoreMotion cMotion;

            public MotorControl(WMX3Api _wmxApi)
            {
                wmxApi = _wmxApi;
                cMotion = new CoreMotion(wmxApi);
            }
            public bool ClearError()
            {
                int ret = cMotion.AxisControl.ClearAmpAlarm((int)Motor.AlignPusher);

                if (ret == ErrorCode.None)
                    return true;
                else
                    return false;
            }

            /// <summary>
            /// AlignPusher 모터 서보 온 함수.
            /// </summary>
            /// <returns></returns>
            public int AlignPusherServoOn()
            {
                int ret = cMotion.AxisControl.SetServoOn((int)Motor.AlignPusher, 1);
                return ret;
            }

            /// <summary>
            /// AlignPusher 모터 서보 오프 함수
            /// </summary>
            /// <returns></returns>
            public int AlignPusherServoOff()
            {
                int ret = cMotion.AxisControl.SetServoOn((int)Motor.AlignPusher, 0);
                return ret;
            }

            /// <summary>
            /// AlignPusher 원점 좌표계 형성
            /// </summary>
            public void AlignPusherHome()
            {
                cMotion.Home.StartHome((int)Motor.AlignPusher);
            }

            /// <summary>
            /// AlignPusher 모터 상대이동 함수.
            /// </summary>
            /// <param name="target">목표위치</param>
            /// <param name="velocity">속도</param>
            /// <param name="acc">가속도</param>
            /// <param name="dec">감속도</param>
            /// <returns></returns>
            public int AlignPusherRelativeMove(double target, double velocity, double acc, double dec)
            {
                Motion.PosCommand pCmd = new Motion.PosCommand();

                pCmd.Axis = (int)Motor.AlignPusher;
                pCmd.Target = target;
                pCmd.Profile.Velocity = velocity;
                pCmd.Profile.Acc = acc;
                pCmd.Profile.Dec = dec;
                pCmd.Profile.Type = ProfileType.Trapezoidal;

                int ret = cMotion.Motion.StartMov(pCmd);
                return ret;
            }

            /// <summary>
            /// AlignPusher 모터 정지 함수.
            /// </summary>
            /// <returns></returns>
            public int AlignPusherStop()
            {
                int ret = cMotion.Motion.Stop((int)Motor.AlignPusher);
                return ret;
            }
        }
    }
}
