import os                         # 현재 디렉토리 확인 기능
import sys                        # system specific parameters and functions : 파이썬 스크립트 관리
from PyQt5.QtWidgets import *     # GUI의 그래픽적 요소를 제어       하단의 terminal 선택, activate py37_32,  pip install pyqt5,   전부다 y
from PyQt5 import uic             # ui 파일을 가져오기위한 함수
from PyQt5.QtCore import *        # eventloop/스레드를 사용 할 수 있는 함수 가져옴.

################# 부가 기능 수행(일꾼) #####################################
from kiwoom import Kiwoom          # 키움증권 함수/공용 방 (싱글턴)
from Qthread_1 import Thread1      # 계좌평가잔고내역 가져오기
from Qthread_2 import Thread2      # 계좌 관리
from Qthread_3 import Thread3      # 자동매매 시작

#=================== 프로그램 실행 프로그램 =========================#

form_class = uic.loadUiType("ALBA.ui")[0]             # 만들어 놓은 ui 불러오기

class Login_Machnine(QMainWindow, QWidget, form_class):       # QMainWindow : PyQt5에서 윈도우 생성시 필요한 함수

    def __init__(self, *args, **kwargs):                      # Main class의 self를 초기화 한다.

        print("Login Machine 실행합니다.")
        super(Login_Machnine, self).__init__(*args, **kwargs)
        form_class.__init__(self)                            # 상속 받은 from_class를 실행하기 위한 초기값(초기화)
        self.setUI()                                         # UI 초기값 셋업 반드시 필요

        ### 초기 셋팅 : 계좌평가잔고내역
        self.label_11.setText(str("총매입금액"))
        self.label_12.setText(str("총평가금액"))
        self.label_13.setText(str("추정예탁자산"))
        self.label_14.setText(str("총평가손익금액"))
        self.label_15.setText(str("총수익률(%)"))

        ########## 종목 추가 하기 우측 정렬
        self.searchItemTextEdit2.setAlignment(Qt.AlignRight)

        self.buy_price.setAlignment(Qt.AlignRight)
        self.buy_price.setDecimals(0)
        self.n_o_stock.setAlignment(Qt.AlignRight)
        self.n_o_stock.setDecimals(0)
        self.profit_price.setAlignment(Qt.AlignRight)
        self.profit_price.setDecimals(0)
        self.loss_price.setAlignment(Qt.AlignRight)
        self.loss_price.setDecimals(0)

        #### 기타 함수
        self.login_event_loop = QEventLoop()  # 이때 QEventLoop()는 block 기능을 가지고 있다.

        ####키움증권 로그인 하기
        self.k = Kiwoom()                     # Kiwoom()을 실행하며 상속 받는다. Kiwoom()은 전지적인 아이다.
        self.set_signal_slot()                # 키움로그인을 위한 명령어 전송 시 받는 공간을 미리 생성한다.
        self.signal_login_commConnect()

        #####이벤트 생성 및 진행
        self.call_account.clicked.connect(self.c_acc)         # 계좌정보가져오기
        self.acc_manage.clicked.connect(self.a_manage)        # 계좌관리하기
        self.Auto_start.clicked.connect(self.auto)            # 자동매매 시작


        ################# 부가기능 1 : 종목선택하기 새로운 종목 추가 및 삭제
        self.k.kiwoom.OnReceiveTrData.connect(self.trdata_slot)           # 키움서버 데이터 받는 곳
        self.additmelast.clicked.connect(self.searchItem2)                # 종목 추가
        self.Deletcode.clicked.connect(self.deltecode)                        # 종목 삭제


        ################# 부가기능 2 : 데이터베이스화 하기, 저장, 삭제, 불러오기
        self.Getanal_code = []                                                 # 불러온 파일 저장
        self.Save_Stock.clicked.connect(self.Save_selected_code)               # 종목 저장
        self.Del_Stock.clicked.connect(self.delet_code)                        # 종목 삭제
        self.Load_Stock.clicked.connect(self.Load_code)                        # 종목 불러오기
        ####################

    def Load_code(self):

        if os.path.exists("dist/Selected_code.txt"):
            f = open("dist/Selected_code.txt", "r", encoding="utf8")
            lines = f.readlines()  # 여러 종목이 저장되어 있다면 모든 항목을 가져온다.
            for line in lines:
                if line != "":                     # 만약에 line이 비어 있지 않다면
                    ls = line.split("\t")          # \t(tap)로 구분을 지어 놓는다.
                    t_code = ls[0]
                    t_name = ls[1]
                    curren_price = ls[2]
                    dept = ls[3]
                    mesu = ls[4]
                    n_o_stock = ls[5]
                    profit = ls[6]
                    loss = ls[7].split("\n")[0]
                    self.Getanal_code.append([t_code, t_name, curren_price, dept, mesu, n_o_stock, profit, loss])
            f.close()

        column_head = ["종목코드", "종목명", "현재가", "신용비율", "매수가", "매수수량", "익절가", "손절가"]
        colCount = len(column_head)
        rowCount = len(self.Getanal_code)
        self.buylast.setColumnCount(colCount)  # 행 갯수
        self.buylast.setRowCount(rowCount)  # 열 갯수 (종목 수)
        self.buylast.setHorizontalHeaderLabels(column_head)  # 행의 이름 삽입
        self.buylast.setSelectionMode(QAbstractItemView.SingleSelection)

        for index in range(rowCount):
            self.buylast.setItem(index, 0, QTableWidgetItem(str(self.Getanal_code[index][0])))
            self.buylast.setItem(index, 1, QTableWidgetItem(str(self.Getanal_code[index][1])))
            self.buylast.setItem(index, 2, QTableWidgetItem(str(self.Getanal_code[index][2])))
            self.buylast.setItem(index, 3, QTableWidgetItem(str(self.Getanal_code[index][3])))
            self.buylast.setItem(index, 4, QTableWidgetItem(str(self.Getanal_code[index][4])))
            self.buylast.setItem(index, 5, QTableWidgetItem(str(self.Getanal_code[index][5])))
            self.buylast.setItem(index, 6, QTableWidgetItem(str(self.Getanal_code[index][6])))
            self.buylast.setItem(index, 7, QTableWidgetItem(str(self.Getanal_code[index][7])))



    def Save_selected_code(self):

        for row in range(self.buylast.rowCount()):

            code_n = self.buylast.item(row, 0).text()
            name = self.buylast.item(row, 1).text().strip()
            price = self.buylast.item(row, 2).text()
            dept = self.buylast.item(row, 3).text()
            mesu = self.buylast.item(row, 4).text()
            n_o_stock = self.buylast.item(row, 5).text()
            profit = self.buylast.item(row, 6).text()
            loss = self.buylast.item(row, 7).text()

            f = open("dist/Selected_code.txt", "a",encoding="utf8")  # "a" 달아 쓴다. "w" 덮어 쓴다. files라느 파이썬 페키지 볼더를 만든다.
            f.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (code_n, name, price, dept, mesu, n_o_stock, profit, loss))  # t는 tap을 의미한다.
            f.close()

    def delet_code(self):

        if os.path.exists("dist/Selected_code.txt"):
            os.remove("dist/Selected_code.txt")

    def deltecode(self):
        x = self.buylast.selectedIndexes()  # 리스트로 선택된 행번호와 열번호가 x에 입력된다.
        self.buylast.removeRow(x[0].row())


    def searchItem2(self):            # 종목추가시 사용됨.
        itemName = self.searchItemTextEdit2.toPlainText()
        if itemName != "":
            for code in self.k.All_Stock_Code.keys():  # 포트폴리오에 저장된 코드들을 실시간 등록
                # 주식체결 정보 가져오기(틱 데이터) : 현재가, 전일대비, 등락률, 매도호가, 매수호가, 거래량, 누적거래량, 고가, 시가, 저가
                if itemName == self.k.All_Stock_Code[code]['종목명']:
                    self.new_code = code


        column_head = ["종목코드", "종목명", "현재가", "신용비율", "매수 가격", "매수 수량", "익절 가격", "손절 가격"]
        colCount = len(column_head)
        row_count = self.buylast.rowCount()

        self.buylast.setColumnCount(colCount)  # 행 갯수
        self.buylast.setRowCount(row_count+1)  # colum_haed가 한 행을 잡아 먹는다. 실제 입력 되는 값은 1행 부터이다.
        self.buylast.setHorizontalHeaderLabels(column_head)  # 행의 이름 삽입

        self.buylast.setItem(row_count, 0, QTableWidgetItem(str(self.new_code))) # 실제 입력값은 1행부터이나 0부터 들어가야 된다.
        self.buylast.setItem(row_count, 1, QTableWidgetItem(str(itemName)))
        ################## 더블 스핀 박스 내용 읽기
        self.buylast.setItem(row_count, 4, QTableWidgetItem(str(int(self.buy_price.value()))))
        self.buylast.setItem(row_count, 5, QTableWidgetItem(str(int(self.n_o_stock.value()))))
        self.buylast.setItem(row_count, 6, QTableWidgetItem(str(int(self.profit_price.value()))))
        self.buylast.setItem(row_count, 7, QTableWidgetItem(str(int(self.loss_price.value()))))


        self.getItemInfo(self.new_code)



    def getItemInfo(self, new_code):
        self.k.kiwoom.dynamicCall("SetInputValue(QString, QString)", "종목코드", new_code)
        self.k.kiwoom.dynamicCall("CommRqData(QString, QString, int, QString)", "주식기본정보요청", "opt10001", 0, "100")

    def setUI(self):
        self.setupUi(self)                # UI 초기값 셋업

    def set_signal_slot(self):
        self.k.kiwoom.OnEventConnect.connect(self.login_slot)  # 내가 알고 있는 login_slot에다가 특정 값을 던져 준다.

    def signal_login_commConnect(self):
        self.k.kiwoom.dynamicCall("CommConnect()")  # 네트워크적 서버 응용프로그램에 데이터를 전송할 수 있게 만든 함수
        self.login_event_loop.exec_()  # 로그인이 완료될 때까지 계속 반복됨. 꺼지지 않음.

    def login_slot(self, errCode):
        if errCode == 0:
            print("로그인 성공")
            self.statusbar.showMessage("로그인 성공")
            self.get_account_info()                    # 로그인시 계좌정보 가져오기

        elif errCode == 100:
            print("사용자 정보교환 실패")
        elif errCode == 101:
            print("서버접속 실패")
        elif errCode == 102:
            print("버전처리 실패")
        self.login_event_loop.exit()  # 로그인이 완료되면 로그인 창을 닫는다.

    def get_account_info(self):
        account_list = self.k.kiwoom.dynamicCall("GetLoginInfo(String)", "ACCNO")

        for n in account_list.split(';'):
            self.accComboBox.addItem(n)

    def c_acc(self):
        print("선택 계좌 정보 가져오기")
        ##### 1번 일꾼 실행
        h1 = Thread1(self)
        h1.start()

    def a_manage(self):
        print("계좌 관리")
        h2 = Thread2(self)
        h2.start()


    def auto(self):
        print("자동매매 시작")
        h3 = Thread3(self)
        h3.start()



    def trdata_slot(self, sScrNo, sRQName, sTrCode, sRecordName, sPrevNext):

        if sTrCode == "opt10001":
            if sRQName == "주식기본정보요청":
                currentPrice = abs(int(self.k.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "현재가")))
                D_R = (self.k.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "신용비율")).strip()
                row_count = self.buylast.rowCount()
                self.buylast.setItem(row_count - 1, 2, QTableWidgetItem(str(currentPrice)))
                self.buylast.setItem(row_count - 1, 3, QTableWidgetItem(str(D_R)))



if __name__=='__main__':             # import된 것들을 실행시키지 않고 __main__에서 실행하는 것만 실행 시킨다.
                                     # 즉 import된 다른 함수의 코드를 이 화면에서 실행시키지 않겠다는 의미이다.

    app = QApplication(sys.argv)     # PyQt5로 실행할 파일명을 자동으로 설정, PyQt5에서 자동으로 프로그램 실행
    CH = Login_Machnine()            # Main 클래스 myApp으로 인스턴스화
    CH.show()                        # myApp에 있는 ui를 실행한다.
    app.exec_()                      # 이벤트 루프
