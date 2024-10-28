from PyQt5.QtWidgets import *                 # GUI의 그래픽적 요소를 제어       하단의 terminal 선택, activate py37_32,  pip install pyqt5,   전부다 y
from PyQt5.QtCore import *                    # eventloop/쓰레드를 사용할 수 있는 함수 가져옴
from PyQt5.QAxContainer import *              # 키움증권의 클레스를 사용할 수 있게 한다.(QAxWidget)
from PyQt5Singleton import Singleton

class Kiwoom(QWidget, metaclass=Singleton):       # QMainWindow : PyQt5에서 윈도우 생성시 필요한 함수

    # class Kiwoom(QWidget):

    def __init__(self, parent=None, **kwargs):  # Main class의 self를 초기화 한다.

        print("로그인 프로그램을 실행합니다.")

        super().__init__(parent, **kwargs)  # 상속 받은 from_class를 실행하기 위한 초기값(초기화)

        ################ 로그인 관련 정보
        self.kiwoom = QAxWidget('KHOPENAPI.KHOpenAPICtrl.1')  # CLSID

        ################# 전체 공유 데이터
        self.All_Stock_Code = {}  # 코스피, 코스닥 전체 코드넘버 입력
        self.acc_portfolio = {}  # 계좌에 들어있는 종목의 코드, 수익률 등등 입력
        self.portfolio_stock_dict = {}  # 매매에 관한 모든 종목(현재계좌 종목/금일 등록종목)이 모두 들어간다.
        self.today_meme = []  # 금일 매매하는 종목에 대하여 들어간다.
        self.not_account_stock_dict = {}  # 미체결잔고

        ################# 실시간데이터 처리 변수
        self.Real_30Tic_Save = {}  # 틱봉 데이터를 계속 저장한다.
        self.Real_bun_save = {}  # 궂이 필요 없는것 같다. 나중에 삭제 할꺼다~!
        self.save_code_for_bun = {}  # 5분봉의 5분을 알기위한 곳
        self.hoga_meme = {}  # 금일 호가 데이터를 받아올 데이터를 저장한는 곳

        self.Five_bun_portfolio = {}  # 5분봉의 5일선 데이터를 저장(계속 하나를 넣고 빼고 한다. 중요)
        self.Ave_Five_bun_portfolio = {}  # 5일선 평균값 저장 : 5일선
        self.Twenty_bun_portfolio = {}  # 분봉의 20일선 데이터 저장
        self.Ave_Twenty_bun_portfolio = {}  # 20일선 평균값 저장 : 20일선

        self.Five_tic_portfolio = {}  # 선택틱의 5일선 데이터를 저장
        self.Ave_Five_tic_portfolio = {}  # 5일선 틱의 평균값
        self.Twenty_tic_portfolio = {}  # 선택틱의 20일선 데이터를 저장
        self.Ave_Twenty_tic_portfolio = {}  # 20일선 틱의 평균값
        self.Mingam_tic_portfolio = {}  # 선택틱의 민감도선 데이터를 저장
        self.Ave_Mingam_tic_portfolio = {}  # 민감도선 틱의 평균값

        ################## 오늘 산 잔고

        self.jango_dict = {}
        self.buy_jogon = {}  # 미체결 잔고



