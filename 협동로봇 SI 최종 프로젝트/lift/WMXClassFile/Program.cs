using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using WMXClassFile;


namespace WMXClassFile
{
    static class Program
    {
        /// <summary>
        /// The main entry point for the application.
        /// </summary>
        [STAThread]

        static void Main()
        {
            //리프트 초기 세팅
            WMX.Communication lift = new WMX.Communication();
            WMX.MotorControl moter = new WMX.MotorControl(lift.GetHandler());

            double up = 42000;
            double down = -42000;
            double vel = 10000;
            double acc = 10000;
            double dec = 10000;

            lift.Open();
            lift.StartCommunication();
            moter.ClearError();
            Thread.Sleep(1000);
            moter.AlignPusherServoOn();
            Thread.Sleep(1000);
            moter.AlignPusherRelativeMove(-50000, vel, acc, dec);
            Thread.Sleep(10000);
            moter.ClearError();
            Thread.Sleep(1000);
            moter.AlignPusherServoOn();
            Thread.Sleep(1000);
            moter.AlignPusherRelativeMove(up, vel, acc, dec);
            Thread.Sleep(10000);

            // server 소켓을 생성한다.
            using (var server = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp))
            {
                server.Bind(new IPEndPoint(IPAddress.Any, 9999));
                server.Listen(20);

                Console.WriteLine("Server Start... Listen port 9999...");

                try
                {
                    while (true)
                    {
                        ThreadPool.QueueUserWorkItem(c =>
                        {
                            Socket client = (Socket)c;
                            try
                            {
                                while (true)
                                {
                                    var data = new byte[4];
                                    client.Receive(data, 4, SocketFlags.None);
                                    Array.Reverse(data);
                                    data = new byte[BitConverter.ToInt32(data, 0)];
                                    client.Receive(data, data.Length, SocketFlags.None);

                                    var in_data = Encoding.UTF8.GetString(data);
                                    string[] result = in_data.Split(new char[] { '-' });
                                    if (result[0] == "1")
                                    {
                                        moter.AlignPusherRelativeMove(down, vel, acc, dec);
                                        Thread.Sleep(10000);
                                        moter.ClearError();
                                        Thread.Sleep(1000);
                                        moter.AlignPusherServoOn();
                                        Thread.Sleep(1000);
                                    }
                                    else if (result[0]=="0")
                                    {
                                        moter.AlignPusherRelativeMove(up, vel, acc, dec);
                                        Thread.Sleep(10000);
                                        moter.ClearError();
                                        Thread.Sleep(1000);
                                        moter.AlignPusherServoOn();
                                        Thread.Sleep(1000);
                                    }
                                    string out_data = "1";
                                    data = Encoding.UTF8.GetBytes(out_data);
                                    client.Send(BitConverter.GetBytes(data.Length));
                                    client.Send(data, data.Length, SocketFlags.None);
                                }

                            }
                            catch (Exception)
                            {
                                client.Close();
                            }
                        }, server.Accept());
                    }
                }
                catch (Exception e)
                {
                    Console.WriteLine(e);
                }
            }
            Console.WriteLine("Press any key...");
            Console.ReadLine();
            lift.StopCommunication();
            lift.Close();
        }
    }
}
