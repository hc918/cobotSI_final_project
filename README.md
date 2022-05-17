# cobotSI_final_project
협동로봇 SI 최종 프로젝트

*주의사항

협동로봇 SI 최종 프로젝트/Robot/test_v3는 CoppeliaSim v4.0.0과 호환됩니다. %다른 버전과는 호환 장담 못합니다!

lift를 움직일 컴퓨터에는 WMX3가 설치되어 있어야 합니다.

키오스크 파일 Mock_Up은 CIMON SCADA 3.90에 호환됩니다.(듀얼 모니터 또는 main_v5와 다른 컴퓨터 사용 추천)

네트워크상에 협동로봇이 없다면 CoppeliaSim 시뮬레이션만 작동시킬 수 있습니다.

*실행방법

1.lift 폴더는 lift를 움직일 컴퓨터에 넣습니다.

2.orderlist.txt는 네트워크 상 공유폴더에 추가합니다.

3.Mock_Up 폴더는 C:\CIMON\SCADA 3.90에 추가합니다.

4.CIMOND를 실행하여 Mock_Up을 찾아서 엽니다.

5.스크립트의 record order 부분에서 파일 저장 경로를 공유 폴더의 orderlist.txt로 바꿉니다.

6.Mock_Up에서 CIMONX를 실행시켜줍니다.

7.main_v5의 파일 저장 경로 부분도 공유 폴더의 orderlist.txt로 바꿉니다.

8.lift를 움직일 컴퓨터에서 WMX3를 실행하고 Alert창을 열어놓습니다. 

9.lift를 움직일 컴퓨터에서 lift 폴더 내의 WMXconnectPython.sln을 열고 실행시켜줍니다.

10.PythonToRobot의 main_v5를 실행합니다.

11.창이 뜨면 접속할 로봇 또는 CoppeliaSim 실행 컴퓨터의 IP를 입력하고 로봇의 경우 PORT번호 0, CoppeliaSim의 경우 19997입력후 확인을 눌러줍니다.

12.키오스크에서 메뉴를 주문 후 main_v5에서 조리시작을 눌러주면 시뮬레이션 또는 로봇이 동작합니다.
