from profunc import *
from tkinter import *
from tkinter.ttk import Treeview, Progressbar
from indy7 import *
import platform
import sys
import time


class Manager:
    __font = ("Helvetica", 15)
    count = 0
    frame = []
    l1 = []
    ml = []
    l2 = []
    t = []
    progbar = []
    progress = []
    thr = []
    ready = False

    def __init__(self):
        if platform.system() == 'Windows':
            self.__font = ("Helvetica", 10)
        else:
            self.__font = ("Helvetica", 15)
        window = Tk()
        window.title("주문 관리")
        window.resizable(width=False, height=False)

        orderlist_frame = Frame(window, relief='solid')
        orderlist_frame.grid(row=0, column=0, rowspan=4, padx=4)
        Label(window, text="Pot 상태", font=self.__font, anchor="center").grid(row=0, column=1, columnspan=4, sticky=N,
                                                                             pady=4)
        for i in range(fryer.potNum):
            self.frame.append(Frame(window, relief='solid', bd=2, height=160, width=120))
            self.frame[i].grid(row=i // 4 + 1, column=i % 4 + 1, padx=4, pady=4, sticky=N)
            self.frame[i].propagate(0)

        Label(orderlist_frame, text="주문 목록", font=self.__font).grid(row=0, column=0, padx=4, pady=4, columnspan=2)
        tv = Treeview(orderlist_frame, columns=["one", "two"], displaycolumns=["one", "two"], height=20)
        tv.grid(row=1, sticky=W, padx=4, pady=4, rowspan=2, columnspan=2)
        tv.yview()

        tv.column("#0", width=60, anchor="center")
        tv.heading("#0", text="주문 번호", anchor="center")
        tv.column("#1", width=100, anchor="center")
        tv.heading("one", text="메뉴", anchor="center")
        tv.column("#2", width=50, anchor="center")
        tv.heading("two", text="수량", anchor="center")

        scroll = Scrollbar(orderlist_frame, orient="vertical", command=tv.yview)
        scroll.grid(row=1, rowspan=2, column=2, sticky=N + S, pady=4)
        tv.configure(yscrollcommand=scroll.set)

        def list_update():
            while Manager.ready:
                with open("/Users/jeonghyeonchae/Documents/kiosk/orderlist.txt", 'r') as fin:
                    temp = fin.read().splitlines(True)
                    if len(temp) > 0 and temp[0]:
                        menu = int(temp[0][0:1])
                        num = int(temp[0][2:])
                        if menu == 1:
                            name = "로스카츠"
                        elif menu == 2:
                            name = "치즈카츠"
                        elif menu == 3:
                            name = "카레카츠"
                        tv.insert('', 'end', text=str(self.count + 1), values=[name, num, menu], iid=str(self.count))
                        self.count += 1
                    with open("/Users/jeonghyeonchae/Documents/kiosk/orderlist.txt", 'w') as fout:
                        fout.writelines(temp[1:])

        def click_item(event=None):
            choice = tv.focus()
            if choice:
                insert_btn.configure(state=NORMAL)
                delete_btn.configure(state=NORMAL)

        def insert(event=None):
            choice = tv.focus()
            getValue = tv.item(choice).get('values')
            menu = int(getValue[2])
            num = int(getValue[1])
            fryer.setMenu(num, menu)
            if robot:
                indy.queue.append_queue([1, 0])
            tv.focus(tv.next(choice))
            tv.delete(choice)
            time.sleep(0.1)
            tv.selection_toggle(tv.focus())

        def delete(event=None):
            def yes(event=None):
                choice = tv.focus()
                tv.focus(tv.next(choice))
                tv.selection_toggle(tv.focus())
                tv.delete(choice)

            dt = Toplevel()
            dt.title("삭제 확인")
            Label(dt, text="삭제하시겠습니까?", font=self.__font).grid(row=0, column=0, padx=4, pady=4, columnspan=2)
            b1 = Button(dt, text="확인", command=lambda: [yes(), dt.destroy()], font=self.__font)
            b1.grid(row=1, column=0, padx=4, pady=4)
            b2 = Button(dt, text="취소", command=dt.destroy, font=self.__font)
            b2.grid(row=1, column=1, padx=4, pady=4)

        insert_btn = Button(orderlist_frame, text="조리 시작", command=insert, font=self.__font, state=DISABLED)
        insert_btn.grid(row=3, column=0, sticky=E, padx=4, pady=4)
        delete_btn = Button(orderlist_frame, text="삭제", command=delete, fg="red", font=self.__font, state=DISABLED)
        delete_btn.grid(row=3, column=1, sticky=W, padx=4, pady=4)
        tv.bind('<ButtonRelease-1>', click_item)
        tv.bind('<Return>', insert)
        tv.bind('<Escape>', delete)

        def set_pot(potnum):
            for i in range(potnum):
                self.l1.append(Label(self.frame[i], text=f"{i + 1}번 Pot", font=self.__font, anchor="center"))
                self.l1[i].pack(side='top', pady=4)
                self.ml.append(Label(self.frame[i], text="", font=self.__font, anchor="center"))
                self.ml[i].pack(pady=4)
                self.l2.append(Label(self.frame[i], text="", font=self.__font, anchor="center"))
                self.l2[i].pack(pady=4)
                self.t.append(Label(self.frame[i], text="", font=self.__font, anchor="center"))
                self.t[i].pack(pady=4)
                self.progress.append(DoubleVar())
                self.progbar.append(Progressbar(self.frame[i], maximum=100, length=100, variable=self.progress[i]))
                self.progbar[i].pack(side='bottom', pady=4)

        def update_status(num, i):
            while Manager.ready:
                fryer.getReadyInfo(0, i)
                fryer.getTimerInfo(0, i)
                self.t[i].configure(
                    text=f"{int(fryer.timer[0][i] // 60):0>2}:{int(fryer.timer[0][i] % 60) // 1:0>2}")
                if fryer.ready[0][i] == -1:
                    if robot:
                        indy.queue.append_queue([2, 0])
                    self.frame[i].configure(bg="blue")
                    self.l1[i].configure(bg="blue")
                    self.ml[i].configure(bg="blue")
                    self.l2[i].configure(text="조리 완료", bg="blue")
                    self.t[i].configure(bg="blue")
                    self.progress[i].set(100)
                    lock.acquire()
                    if sim.getintegersignal(f"fryTime1_{i + 1}") != 0:
                        fryer.get_count(fryer.menu[i])
                        sim.setintegersignal(f"fryTime1_{i + 1}", 0)
                    lock.release()
                elif fryer.ready[0][i] == 2:
                    self.frame[i].configure(bg="gray")
                    self.l1[i].configure(bg="gray")
                    self.ml[i].configure(text="", bg="gray")
                    self.l2[i].configure(text="대기 중", bg="gray")
                    self.t[i].configure(bg="gray")
                    self.progbar[i].stop()
                    self.progress[i].set(0)
                elif fryer.ready[0][i] == 3:
                    lock.acquire()
                    fryer.menu[i] = sim.getintegersignal(f"fryTime1_{i + 1}")
                    lock.release()
                    if fryer.menu[i] == 1:
                        self.ml[i].configure(text="로스카츠")
                    elif fryer.menu[i] == 2:
                        self.ml[i].configure(text="치즈카츠")
                    elif fryer.menu[i] == 3:
                        self.ml[i].configure(text="카레카츠")
                    if fryer.timer[0][i] > 0:
                        self.frame[i].configure(bg="green")
                        self.l1[i].configure(bg="green")
                        self.ml[i].configure(bg="green")
                        self.l2[i].configure(text="조리 중", bg="green")
                        self.t[i].configure(bg="green")
                        self.progbar[i].configure(mode="determinate")
                        if fryer.fryingTime[0][i] != 0:
                            self.progress[i].set(100 - fryer.timer[0][i] * 100 / fryer.fryingTime[0][i])
                        self.progbar[i].update()

        done_frame = Frame(window, relief='solid')
        done_frame.grid(row=3, column=1, columnspan=4, padx=4)
        cl1 = Label(done_frame, text=f"로스: {fryer.doneCount[0]:>3} 개", font=self.__font, anchor="e")
        cl1.grid(row=0, column=0, padx=4)
        cl2 = Label(done_frame, text=f"치즈: {fryer.doneCount[1]:>3} 개", font=self.__font, anchor="e")
        cl2.grid(row=0, column=1, padx=4)
        cl3 = Label(done_frame, text=f"카레: {fryer.doneCount[2]:>3} 개", font=self.__font, anchor="e")
        cl3.grid(row=0, column=2, padx=4)
        gl = Label(done_frame, text=f"수량: {fryer.getDoneGram():>6} gram", font=self.__font, anchor="e")
        gl.grid(row=0, column=3, padx=4)

        def count():
            while Manager.ready:
                cl1.configure(text=f"로스: {fryer.doneCount[0]:>3} 개")
                cl2.configure(text=f"치즈: {fryer.doneCount[1]:>3} 개")
                cl3.configure(text=f"카레: {fryer.doneCount[2]:>3} 개")
                gl.configure(text=f"수량: {fryer.getDoneGram():>6} gram")

        set_pot(fryer.potNum)
        for i in range(fryer.potNum):
            self.thr.append(Thread(target=update_status, args=(0, i)))
            self.thr[i].setDaemon(True)
            self.thr[i].start()
        ult = Thread(target=list_update, args=())
        ult.setDaemon(True)
        ult.start()
        c = Thread(target=count, args=())
        c.setDaemon(True)
        c.start()
        window.mainloop()


def ip_set():
    w = Tk()
    w.title("로봇 통신 설정")
    w.resizable(width=False, height=False)

    IP, PORT = StringVar(), StringVar()

    def check_data():
        global fryer
        global robot
        global indy
        try:
            if int(PORT.get()) == 0:
                robot = True
                fryer = Fryer()
                indy = Indy7(IP.get())
                indy.connect()
            else:
                fryer = Fryer(1, 8)
                sim = env(IP.get(), int(PORT.get()))
                sim.start()
            save_IP(IP.get())
            w.destroy()
            Manager.ready = True
        except:
            message = Toplevel()
            message.title("에러!")
            message.resizable(width=False, height=False)
            Label(message, text="입력값을 확인해주세요!").grid(row=0, column=0, padx=10, pady=10)

    def get_saved_IP():
        with open("IP_list.txt", 'r') as fin:
            temp = fin.read().splitlines(True)
            return temp[0]

    def save_IP(IP):
        with open("IP_list.txt", 'w') as fout:
            fout.writelines(IP)

    Label(w, text=f"IP : ").grid(row=0, column=0, padx=10, pady=10, sticky=E)
    Label(w, text=f"PORT : ").grid(row=1, column=0, padx=10, pady=10, sticky=E)
    ipe = Entry(w, textvariable=IP)
    ipe.grid(row=0, column=1, padx=10, pady=10)
    ipe.insert(0, str(get_saved_IP()))
    pwe = Entry(w, textvariable=PORT)
    pwe.grid(row=1, column=1, padx=10, pady=10)
    pwe.insert(0, "19997")
    f = Frame(w, relief='solid')
    f.grid(row=2, column=0, columnspan=2)
    Button(f, text="연결", command=check_data).pack(side="left", padx=10, pady=10)
    Button(f, text="종료", command=lambda: [w.destroy(), sys.exit(0)]).pack(side="right", padx=10, pady=10)

    w.mainloop()


if __name__ == '__main__':
    try:
        ip_set()
        if Manager.ready:
            Manager()
            if robot:
                indy.disconnect()
            else:
                sim.stop()
                sim.finish()
    except:
        message = Toplevel()
        message.title("Error!")
        message.resizable(width=False, height=False)
        Label(message, text="관리자에게 문의하세요.\ntel)010-6220-9618").grid(row=0, column=0, padx=10, pady=10)
