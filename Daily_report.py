#==== 영상의학과 일일 보고서
import sys
from PyQt6 import uic, QtGui
from PyQt6.QtWidgets import QApplication, QMainWindow, QProgressBar, QTableWidgetItem
from PyQt6.QtCore import Qt, QDate
import ctypes
from PyQt6.QtWidgets import QMessageBox
import pymysql
from PyQt6.QtGui import QDoubleValidator
import pyautogui

# ----- 한글 입력 체크 하여 한글키 활성화
# 한글 입력 모드 체크
def get_hanguel_state():
    return hllDll.GetKeyState(VK_HANGUEL)
    # get_hanguel.state() == 1 한글
    # get_hanguel.state() == 0 영어
    # 바꿀때는 change_state()


hllDll = ctypes.WinDLL('User32.dll', use_last_error=True)
VK_HANGUEL = 0x15   # VK_HANGUEL = 0x15(한글키) 활성화

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # UI 로드
        self.ui = uic.loadUi("format/daily_report.ui", self)

        # # 전체 화면으로 설정
        self.resize(1650, 1000)
        # self.setWindowState(Qt.WindowState.WindowMaximized)

        # 윈도우 스타일 변경 (최대화 버튼 제거)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowMaximizeButtonHint)
        # 닫기 버튼을 비활성화하는 플래그 설정
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowCloseButtonHint)

        #--- 오늘 날짜로 설정 후 입력 대기 상태
        self.dateEdit_report.setCalendarPopup(True)
        # self.dateEdit_report.setFocus()

        #--- cursor pushButton_insert
        self.ui.pushButton_insert.setCursor(QtGui.QCursor(Qt.CursorShape.PointingHandCursor))


        #--- 과장 체크박스 비활성      
        self.checkBox_exaggeration.setEnabled(False)

        #--- 입력 창 close 
        self.InputClose()

        #=== Edit Clear
        #----- 날짜 오늘 날짜로
        today = QDate.currentDate() # QDate.currentDate(): 현재 날짜를 반환
        self.dateEdit_report.setDate(today) # setDate(): 'QDateEdit' 위젯에 날짜를 설정
        #---- checkBox (Default unchecked)
        self.EditClear()

        # 한글입력
        QApplication.instance().focusChanged.connect(self.on_x_n) # 한글입력

        #--- 버튼 비활성화
        self.ui.pushButton_save.setEnabled(False)
        self.ui.pushButton_update.setEnabled(False)
        self.ui.pushButton_update_save.setEnabled(False)

        
        #=== 버튼 연결
        self.ui.pushButton_insert.clicked.connect(self.insertData)
        self.ui.pushButton_reset.clicked.connect(self.resetData)

        self.ui.pushButton_save.clicked.connect(self.saveData)
        
        self.ui.pushButton_update.clicked.connect(self.updateData)
        
        self.ui.pushButton_update_save.clicked.connect(self.updateData_save)
        
        self.ui.pushButton_quit.clicked.connect(self.ProgramQuit)

        # 스타일 시트 설정
        self.setButtonStyles()

        # 테이블 위젯 설정
        self.TableWidgetShow()
        
    def updateData(self):
        self.InputOpen()
        self.ui.pushButton_update.setEnabled(False) #--- 수정버튼 비활성화
        self.ui.pushButton_save.setEnabled(False) #--- 저장버튼 비활성화
        self.ui.pushButton_update_save.setEnabled(True) #--- 수정저장버튼 활성화
        
        
        
  
        
    def updateData_save(self):
      
        self.dateEdit_report.setEnabled(False)
        #--- 데이터 수정 후 저장하는 updata문 작성
        #---- date(시술일)
        self.dateVar = self.dateEdit_report.date()
        i_dateEdit_report = self.dateVar.toString('yyyy-MM-dd')

        #---- checkBox (Default unchecked)
        i_team_leader = "ok" if self.checkBox_team.isChecked() else "no"
        i_exaggeration = "ok" if self.checkBox_exaggeration.isChecked() else "no"
        
        # # lineEdit 데이터 가져오기
        i_x1 = self.lineEdit_x1.text()
        i_x2 = self.lineEdit_x2.text()
        i_x3 = self.lineEdit_x3.text()
        i_x5 = self.lineEdit_x5.text()
        i_x10 = self.lineEdit_x10.text()
        i_r6 = self.lineEdit_r6.text()
        i_rs = self.lineEdit_rs.text()
        i_re = self.lineEdit_re.text()
        i_a9 = self.lineEdit_a9.text()
        i_ak = self.lineEdit_ak.text()
        i_ah = self.lineEdit_ah.text()
        i_od = self.lineEdit_od.text()
        i_o_n = self.lineEdit_on.text()
        i_pd = self.lineEdit_pd.text()
        i_ed = self.lineEdit_ed.text()
        i_xn = self.lineEdit_xn.text()
        i_pn = self.lineEdit_pn.text()
        i_en = self.lineEdit_en.text()
        i_xm = self.lineEdit_xm.text()
        i_so = self.lineEdit_so.text()
        i_sm = self.lineEdit_sm.text()
        i_hc = self.lineEdit_hc.text()
        i_hb = self.lineEdit_hb.text()
        i_hm = self.lineEdit_hm.text()
        i_cd = self.lineEdit_cd.text()
        i_cn = self.lineEdit_cn.text()
        i_md = self.lineEdit_md.text()
        i_mn = self.lineEdit_mn.text()
        i_x1_p = self.lineEdit_x1_p.text()
        i_x2_p = self.lineEdit_x2_p.text()
        i_x3_p = self.lineEdit_x3_p.text()
        i_x5_p = self.lineEdit_x5_p.text()
        i_x10_p = self.lineEdit_x10_p.text()
        i_r6_p = self.lineEdit_r6_p.text()
        i_rs_p = self.lineEdit_rs_p.text()
        i_re_p = self.lineEdit_re_p.text()
        i_a9_p = self.lineEdit_a9_p.text()
        i_ak_p = self.lineEdit_ak_p.text()
        i_ah_p = self.lineEdit_ah_p.text()
        i_od_p = self.lineEdit_od_p.text()
        i_on_p = self.lineEdit_on_p.text()
        i_pd_p = self.lineEdit_pd_p.text()
        i_ed_p = self.lineEdit_ed_p.text()      
        i_xn_p = self.lineEdit_xn_p.text()
        i_pn_p = self.lineEdit_pn_p.text()
        i_en_p = self.lineEdit_en_p.text()
        i_xm_p = self.lineEdit_xm_p.text()
        i_so_p = self.lineEdit_so_p.text()
        i_he_p = self.lineEdit_he_p.text()
        i_ct_p = self.lineEdit_ct_p.text()
        i_mr_p = self.lineEdit_mr_p.text()  
        i_x1_m = self.lineEdit_x1_m.text()
        i_x2_m = self.lineEdit_x2_m.text()
        i_x3_m = self.lineEdit_x3_m.text()
        i_x5_m = self.lineEdit_x5_m.text()
        i_x10_m = self.lineEdit_x10_m.text()
        i_r6_m = self.lineEdit_r6_m.text()
        i_rs_m = self.lineEdit_rs_m.text()
        i_re_m = self.lineEdit_re_m.text()
        i_a9_m = self.lineEdit_a9_m.text()
        i_ak_m = self.lineEdit_ak_m.text()
        i_ah_m = self.lineEdit_ah_m.text()
        i_or_m = self.lineEdit_or_m.text()
        i_pd_m = self.lineEdit_pd_m.text()
        i_ed_m = self.lineEdit_ed_m.text()
        i_xn_m = self.lineEdit_xn_m.text()
        i_pn_m = self.lineEdit_pn_m.text()
        i_en_m = self.lineEdit_en_m.text()
        i_xm_m = self.lineEdit_xm_m.text()
        i_so_m = self.lineEdit_so_m.text()
        i_he_m = self.lineEdit_he_m.text()
        i_ct_m = self.lineEdit_ct_m.text()
        i_mr_m = self.lineEdit_mr_m.text()
        i_x1_n = self.lineEdit_x1_n.text()
        i_x2_n = self.lineEdit_x2_n.text()
        i_x3_n = self.lineEdit_x3_n.text()
        i_x5_n = self.lineEdit_x5_n.text()
        i_x10_n = self.lineEdit_x10_n.text()
        i_r6_n = self.lineEdit_r6_n.text()
        i_rs_n = self.lineEdit_rs_n.text()
        i_re_n = self.lineEdit_re_n.text()
        i_a9_n = self.lineEdit_a9_n.text()
        i_ak_n = self.lineEdit_ak_n.text()
        i_ah_n = self.lineEdit_ah_n.text()
        i_or_n = self.lineEdit_or_n.text()
        i_pd_n = self.lineEdit_pd_n.text()
        i_ed_n = self.lineEdit_ed_n.text()
        i_xn_n = self.lineEdit_xn_n.text()
        i_pn_n = self.lineEdit_pn_n.text()
        i_en_n = self.lineEdit_en_n.text()
        i_xm_n = self.lineEdit_xm_n.text()
        i_so_n = self.lineEdit_so_n.text()
        i_he_n = self.lineEdit_he_n.text()
        i_ct_n = self.lineEdit_ct_n.text()
        i_mr_n = self.lineEdit_mr_n.text()
        i_x_d_n = self.lineEdit_x_d_n.text()
        i_x_e_n = self.lineEdit_x_e_n.text()
        i_x_n_n = self.lineEdit_x_n_n.text()
        i_e_d_n = self.lineEdit_e_d_n.text()
        i_e_e_n = self.lineEdit_e_e_n.text()
        i_e_n_n = self.lineEdit_e_n_n.text()
        i_c_d_n = self.lineEdit_c_d_n.text()
        i_c_e_n = self.lineEdit_c_e_n.text()
        i_c_n_n = self.lineEdit_c_n_n.text()
        i_m_d_n = self.lineEdit_m_d_n.text()
        i_m_e_n = self.lineEdit_m_e_n.text()
        i_m_n_n = self.lineEdit_m_n_n.text()
        i_m2_n = self.lineEdit_m2_n.text()

        i_p1 = self.lineEdit_p1.text()
        i_ts1 = self.lineEdit_ts1.text()
        i_te1 = self.lineEdit_te1.text()
        i_ti1 = self.lineEdit_ti1.text()
        i_tn1 = self.lineEdit_tn1.text()
        i_p2 = self.lineEdit_p2.text()
        i_ts2 = self.lineEdit_ts2.text()
        i_te2 = self.lineEdit_te2.text()
        i_ti2 = self.lineEdit_ti2.text()
        i_tn2 = self.lineEdit_tn2.text()
        i_p3 = self.lineEdit_p3.text()
        i_ts3 = self.lineEdit_ts3.text()
        i_te3 = self.lineEdit_te3.text()
        i_ti3 = self.lineEdit_ti3.text()
        i_tn3 = self.lineEdit_tn3.text()    
        i_p4 = self.lineEdit_p4.text()
        i_ts4 = self.lineEdit_ts4.text()
        i_te4 = self.lineEdit_te4.text()
        i_ti4 = self.lineEdit_ti4.text()
        i_tn4 = self.lineEdit_tn4.text()
        i_p5 = self.lineEdit_p5.text()
        i_ts5 = self.lineEdit_ts5.text()
        i_te5 = self.lineEdit_te5.text()
        i_ti5 = self.lineEdit_ti5.text()
        i_tn5 = self.lineEdit_tn5.text()
        i_p6 = self.lineEdit_p6.text()
        i_ts6 = self.lineEdit_ts6.text()
        i_te6 = self.lineEdit_te6.text()
        i_ti6 = self.lineEdit_ti6.text()
        i_tn6 = self.lineEdit_tn6.text()
        i_p7 = self.lineEdit_p7.text()
        i_ts7 = self.lineEdit_ts7.text()
        i_te7 = self.lineEdit_te7.text()
        i_ti7 = self.lineEdit_ti7.text()
        i_tn7 = self.lineEdit_tn7.text()
        i_p8 = self.lineEdit_p8.text()
        i_ts8 = self.lineEdit_ts8.text()
        i_te8 = self.lineEdit_te8.text()
        i_ti8 = self.lineEdit_ti8.text()
        i_tn8 = self.lineEdit_tn8.text()
        i_vac = self.textEdit_vac.toPlainText()
        i_ev = self.textEdit_ev.toPlainText()
        i_edu = self.textEdit_edu.toPlainText()
        i_rep = self.textEdit_rep.toPlainText()

        i_i9 = self.lineEdit_i9.text()
        i_ik = self.lineEdit_ik.text()
        i_ih = self.lineEdit_ih.text()

            
        data = (
                i_team_leader, i_exaggeration,  i_x1, i_x2, 
                i_x3, i_x5, i_x10, i_r6, i_rs, 
                i_re, i_a9, i_ak, i_ah, i_od,
                i_o_n, i_pd, i_ed, i_xn, i_pn,
                i_en, i_xm, i_so, i_sm, i_hc, 
                i_hb, i_hm, i_cd, i_cn, i_md, 
                i_mn,
                i_x1_p, i_x2_p, i_x3_p, i_x5_p, i_x10_p,  
                i_r6_p, i_rs_p, i_re_p, i_a9_p, i_ak_p, 
                i_ah_p, i_od_p, i_on_p, i_pd_p, i_ed_p, 
                i_xn_p, i_pn_p, i_en_p, i_xm_p, i_so_p,
                i_he_p, i_ct_p, i_mr_p,
                i_x1_m, i_x2_m, i_x3_m, i_x5_m, i_x10_m, 
                i_r6_m, i_rs_m, i_re_m, i_a9_m, i_ak_m, 
                i_ah_m, i_or_m, i_pd_m, i_ed_m, i_xn_m, 
                i_pn_m, i_en_m, i_xm_m, i_so_m, i_he_m, 
                i_ct_m, i_mr_m,   
                i_x1_n, i_x2_n, i_x3_n, i_x5_n, i_x10_n, 
                i_r6_n, i_rs_n, i_re_n, i_a9_n, i_ak_n, 
                i_ah_n, i_or_n, i_pd_n, i_ed_n, i_xn_n, 
                i_pn_n, i_en_n, i_xm_n, i_so_n, i_he_n, 
                i_ct_n, i_mr_n,
                i_x_d_n, i_x_e_n, i_x_n_n, i_e_d_n, i_e_e_n, 
                i_e_n_n, i_c_d_n, i_c_e_n, i_c_n_n, i_m_d_n, 
                i_m_e_n, i_m_n_n, i_m2_n,
                i_p1, i_ts1, i_te1, i_ti1, i_tn1,
                i_p2, i_ts2, i_te2, i_ti2, i_tn2,
                i_p3, i_ts3, i_te3, i_ti3, i_tn3,
                i_p4, i_ts4, i_te4, i_ti4, i_tn4,
                i_p5, i_ts5, i_te5, i_ti5, i_tn5,
                i_p6, i_ts6, i_te6, i_ti6, i_tn6,
                i_p7, i_ts7, i_te7, i_ti7, i_tn7,
                i_p8, i_ts8, i_te8, i_ti8, i_tn8,
                i_vac, i_ev, i_edu, i_rep, 
                i_i9, i_ik, i_ih,
                
                i_dateEdit_report            
            ) 

        try:
            conn = pymysql.connect(host="211.186.169.70", user="root", password="1024", db="Daily_report", charset="utf8")
            curs = conn.cursor()
            sql = """
                UPDATE report
                SET  team_leader = %s, exaggeration = %s, x1 = %s, x2 = %s, 
                x3 = %s, x5 = %s, x10 = %s, r6 = %s, rs = %s, 
                re = %s, a9 = %s, ak = %s, ah = %s, od = %s,
                o_n = %s, pd = %s, ed = %s, xn = %s, pn = %s,
                en = %s, xm = %s, so = %s, sm = %s, hc = %s, 
                hb = %s, hm = %s, cd = %s, cn = %s, md = %s, 
                mn = %s,
                x1_p = %s, x2_p = %s, x3_p = %s, x5_p = %s, x10_p = %s,  
                r6_p = %s, rs_p = %s, re_p = %s, a9_p = %s, ak_p = %s,
                ah_p = %s, od_p = %s, on_p = %s, pd_p = %s, ed_p = %s,
                xn_p = %s, pn_p = %s, en_p = %s, xm_p = %s, so_p = %s,
                he_p = %s, ct_p = %s, mr_p = %s,
                x1_m = %s, x2_m = %s, x3_m = %s, x5_m = %s, x10_m = %s, 
                r6_m = %s, rs_m = %s, re_m = %s, a9_m = %s, ak_m = %s, 
                ah_m = %s, or_m = %s, pd_m = %s, ed_m = %s, xn_m = %s, 
                pn_m = %s, en_m = %s, xm_m = %s, so_m = %s, he_m = %s, 
                ct_m = %s, mr_m = %s,
                x1_n = %s, x2_n = %s, x3_n = %s, x5_n = %s, x10_n = %s, 
                r6_n = %s, rs_n = %s, re_n = %s, a9_n = %s, ak_n = %s,
                ah_n = %s, or_n = %s, pd_n = %s, ed_n = %s, xn_n = %s,
                pn_n = %s, en_n = %s, xm_n = %s, so_n = %s, he_n = %s, 
                ct_n = %s, mr_n = %s,
                x_d_n = %s, x_e_n = %s, x_n_n = %s, e_d_n = %s, e_e_n = %s,
                e_n_n = %s, c_d_n = %s, c_e_n = %s, c_n_n = %s, m_d_n = %s,
                m_e_n = %s, m_n_n = %s, m2_n = %s,
                p1 = %s, ts1 = %s, te1 = %s, ti1 = %s, tn1 = %s,
                p2 = %s, ts2 = %s, te2 = %s, ti2 = %s, tn2 = %s,
                p3 = %s, ts3 = %s, te3 = %s, ti3 = %s, tn3 = %s,
                p4 = %s, ts4 = %s, te4 = %s, ti4 = %s, tn4 = %s,
                p5 = %s, ts5 = %s, te5 = %s, ti5 = %s, tn5 = %s,
                p6 = %s, ts6 = %s, te6 = %s, ti6 = %s, tn6 = %s,
                p7 = %s, ts7 = %s, te7 = %s, ti7 = %s, tn7 = %s,
                p8 = %s, ts8 = %s, te8 = %s, ti8 = %s, tn8 = %s,
                vac = %s, ev = %s, edu = %s, rep = %s, i9 = %s, ik = %s, ih = %s
                WHERE report_date = %s
                """

            curs.execute(sql, data)
            conn.commit()

            #----- 날짜 오늘 날짜로 
            today = QDate.currentDate() # QDate.currentDate(): 현재 날짜를 반환
            self.dateEdit_report.setDate(today) # setDate(): 'QDateEdit' 위젯에 날짜를 설정 
            self.EditClear()
            self.InputClose()

                
        except pymysql.MySQLError as e:
            QMessageBox.critical(self, "데이터베이스 오류", f"데이터 삽입 중 오류가 발생했습니다: {e}")
        finally:
            conn.close() 
        
        self.pushButton_update_save.setEnabled(False)
    #--- 데이터 입력

    def TableWidgetShow(self):
        self.tableWidget.clear() 
        
        # QTableWidget 행수를 0으로 설정하여 데이블 위젯에서 모든 행을 제거하는데 사용된다. 즉, 테이블을 초기화하고 기존의 모든 데이터를 지우는 역활을 한다.
        self.tableWidget.setRowCount(0)

        self.tableWidget.setColumnCount(1)  # 열 수 설정
        self.tableWidget.verticalHeader().setFixedWidth(35)

        # 테이블의 가로 헤더의 레이블을 설정
        self.tableWidget.setHorizontalHeaderLabels(['    재료명']) 

        
        # 헤더의 정렬 설정 (왼쪽 설정):  기본 중앙 정렬
        header = self.tableWidget.horizontalHeader()
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignLeft)
        
        # 첫 번째 열의 너비를 230픽셀로 정의함
        self.tableWidget.setColumnWidth(0, 500)

        try:
            conn = pymysql.connect(host="211.186.169.70", user="root", password="1024", db="Daily_report", charset="utf8")
            curs = conn.cursor()
            sql = """
                SELECT * FROM report
            """
            curs.execute(sql)

            mylist = curs.fetchall()
            mylist = sorted(mylist, key=lambda x: x[1], reverse=True)  # 인덱스 2를 기준으로 정렬

            self.db_data = []

            for i, row in enumerate(mylist):
                self.db_data.append(row)
                self.tableWidget.insertRow(i)

                # 첫 번째 column 출력
                item_text = " " * 5 + str(row[1])  # row[2]를 문자열로 변환
                item = QTableWidgetItem(item_text)
                item.setFlags(item.flags() ^ Qt.ItemFlag.ItemIsEditable)
                item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)  # 수직 중간, 수평 왼쪽 정렬
                self.tableWidget.setItem(i, 0, item)
                
            conn.commit()
        except pymysql.MySQLError as e:
            QMessageBox.critical(self, "데이터베이스 오류", f"데이터를 가져오는 중 오류가 발생했습니다: {e}")
        finally:
            if conn:
                conn.close()
            


    def setButtonStyles(self):
        # pushButton_insert 스타일 시트 설정
        buttons = [
        self.ui.pushButton_insert,
        self.ui.pushButton_reset,
        self.ui.pushButton_save,
        self.ui.pushButton_quit,
        self.ui.pushButton_update,
        self.ui.pushButton_update_save
        ]

        style_sheet = """
            QPushButton {
                background-color: #f3f3f3;                
            }
            QPushButton:hover {
                background-color: #c4e1c5;
            }
        """
        for button in buttons:
            button.setStyleSheet(style_sheet)

    #--- 한글입력    
    def on_x_n(self, old, new):
        if new in [self.lineEdit_x1_n, self.lineEdit_x2_n, self.lineEdit_x3_n, self.lineEdit_x5_n, self.lineEdit_x10_n, self.lineEdit_r6_n, self.lineEdit_rs_n, self.lineEdit_re_n, self.lineEdit_a9_n, self.lineEdit_ak_n, self.lineEdit_ah_n, self.lineEdit_or_n, self.lineEdit_pd_n, self.lineEdit_ed_n, self.lineEdit_xn_n, self.lineEdit_pn_n, self.lineEdit_en_n, self.lineEdit_xm_n, self.lineEdit_so_n, self.lineEdit_he_n, self.lineEdit_ct_n, self.lineEdit_mr_n, self.lineEdit_x_d_n, self.lineEdit_x_e_n, self.lineEdit_x_n_n, self.lineEdit_e_d_n, self.lineEdit_e_e_n, self.lineEdit_e_n_n, self.lineEdit_c_d_n, self.lineEdit_c_e_n, self.lineEdit_c_n_n, self.lineEdit_m_d_n, self.lineEdit_m_e_n, self.lineEdit_m_n_n, self.lineEdit_m2_n, self.lineEdit_tn1,  self.lineEdit_tn2,  self.lineEdit_tn3,  self.lineEdit_tn4, self.lineEdit_tn5,   self.lineEdit_tn6,  self.lineEdit_tn7,  self.lineEdit_tn8, self.textEdit_vac, self.textEdit_ev, self.textEdit_edu, self.textEdit_rep ] and get_hanguel_state() != 1:
            pyautogui.press('hangul')
    def on_x_e(self, old, new):
        if new in [self.lineEdit_i9, self.lineEdit_ik, self.lineEdit_ih, self.lineEdit_ep_d, self.lineEdit_ep_n] and get_hanguel_state() != 0:
            pyautogui.press('hangul')

    def resetData(self):
        #--- 버튼 비활성화
        self.ui.pushButton_save.setEnabled(False)
        self.ui.pushButton_update.setEnabled(False)
        self.ui.pushButton_update_save.setEnabled(False)

        self.ui.pushButton_insert.setEnabled(True)

        today = QDate.currentDate() # QDate.currentDate(): 현재 날짜를 반환
        self.dateEdit_report.setDate(today) # setDate(): 'QDateEdit' 위젯에 날짜를 설정

        self.EditClear()

    #===데이터 저장
    def saveData(self):
        #--- lineEdit 데이터 가져오기
        #---- date(시술일)
        self.dateVar = self.dateEdit_report.date()
        i_dateEdit_report = self.dateVar.toString('yyyy-MM-dd')

        #---- checkBox (Default unchecked)
        i_team_leader = "ok" if self.checkBox_team.isChecked() else "no"
        i_exaggeration = "ok" if self.checkBox_exaggeration.isChecked() else "no"

        # # lineEdit 데이터 가져오기
        i_x1 = self.lineEdit_x1.text()
        i_x2 = self.lineEdit_x2.text()
        i_x3 = self.lineEdit_x3.text()
        i_x5 = self.lineEdit_x5.text()
        i_x10 = self.lineEdit_x10.text()
        i_r6 = self.lineEdit_r6.text()
        i_rs = self.lineEdit_rs.text()
        i_re = self.lineEdit_re.text()
        i_a9 = self.lineEdit_a9.text()
        i_ak = self.lineEdit_ak.text()
        i_ah = self.lineEdit_ah.text()
        i_od = self.lineEdit_od.text()
        i_o_n = self.lineEdit_on.text()
        i_pd = self.lineEdit_pd.text()
        i_ed = self.lineEdit_ed.text()
        i_xn = self.lineEdit_xn.text()
        i_pn = self.lineEdit_pn.text()
        i_en = self.lineEdit_en.text()
        i_xm = self.lineEdit_xm.text()
        i_so = self.lineEdit_so.text()
        i_sm = self.lineEdit_sm.text()
        i_hc = self.lineEdit_hc.text()
        i_hb = self.lineEdit_hb.text()
        i_hm = self.lineEdit_hm.text()
        i_cd = self.lineEdit_cd.text()
        i_cn = self.lineEdit_cn.text()
        i_md = self.lineEdit_md.text()
        i_mn = self.lineEdit_mn.text()
        i_x1_p = self.lineEdit_x1_p.text()
        i_x2_p = self.lineEdit_x2_p.text()
        i_x3_p = self.lineEdit_x3_p.text()
        i_x5_p = self.lineEdit_x5_p.text()
        i_x10_p = self.lineEdit_x10_p.text()
        i_r6_p = self.lineEdit_r6_p.text()
        i_rs_p = self.lineEdit_rs_p.text()
        i_re_p = self.lineEdit_re_p.text()
        i_a9_p = self.lineEdit_a9_p.text()
        i_ak_p = self.lineEdit_ak_p.text()
        i_ah_p = self.lineEdit_ah_p.text()
        i_od_p = self.lineEdit_od_p.text()
        i_on_p = self.lineEdit_on_p.text()
        i_pd_p = self.lineEdit_pd_p.text()
        i_ed_p = self.lineEdit_ed_p.text()      
        i_xn_p = self.lineEdit_xn_p.text()
        i_pn_p = self.lineEdit_pn_p.text()
        i_en_p = self.lineEdit_en_p.text()
        i_xm_p = self.lineEdit_xm_p.text()
        i_so_p = self.lineEdit_so_p.text()
        i_he_p = self.lineEdit_he_p.text()
        i_ct_p = self.lineEdit_ct_p.text()
        i_mr_p = self.lineEdit_mr_p.text()  
        i_x1_m = self.lineEdit_x1_m.text()
        i_x2_m = self.lineEdit_x2_m.text()
        i_x3_m = self.lineEdit_x3_m.text()
        i_x5_m = self.lineEdit_x5_m.text()
        i_x10_m = self.lineEdit_x10_m.text()
        i_r6_m = self.lineEdit_r6_m.text()
        i_rs_m = self.lineEdit_rs_m.text()
        i_re_m = self.lineEdit_re_m.text()
        i_a9_m = self.lineEdit_a9_m.text()
        i_ak_m = self.lineEdit_ak_m.text()
        i_ah_m = self.lineEdit_ah_m.text()
        i_or_m = self.lineEdit_or_m.text()
        i_pd_m = self.lineEdit_pd_m.text()
        i_ed_m = self.lineEdit_ed_m.text()
        i_xn_m = self.lineEdit_xn_m.text()
        i_pn_m = self.lineEdit_pn_m.text()
        i_en_m = self.lineEdit_en_m.text()
        i_xm_m = self.lineEdit_xm_m.text()
        i_so_m = self.lineEdit_so_m.text()
        i_he_m = self.lineEdit_he_m.text()
        i_ct_m = self.lineEdit_ct_m.text()
        i_mr_m = self.lineEdit_mr_m.text()
        i_x1_n = self.lineEdit_x1_n.text()
        i_x2_n = self.lineEdit_x2_n.text()
        i_x3_n = self.lineEdit_x3_n.text()
        i_x5_n = self.lineEdit_x5_n.text()
        i_x10_n = self.lineEdit_x10_n.text()
        i_r6_n = self.lineEdit_r6_n.text()
        i_rs_n = self.lineEdit_rs_n.text()
        i_re_n = self.lineEdit_re_n.text()
        i_a9_n = self.lineEdit_a9_n.text()
        i_ak_n = self.lineEdit_ak_n.text()
        i_ah_n = self.lineEdit_ah_n.text()
        i_or_n = self.lineEdit_or_n.text()
        i_pd_n = self.lineEdit_pd_n.text()
        i_ed_n = self.lineEdit_ed_n.text()
        i_xn_n = self.lineEdit_xn_n.text()
        i_pn_n = self.lineEdit_pn_n.text()
        i_en_n = self.lineEdit_en_n.text()
        i_xm_n = self.lineEdit_xm_n.text()
        i_so_n = self.lineEdit_so_n.text()
        i_he_n = self.lineEdit_he_n.text()
        i_ct_n = self.lineEdit_ct_n.text()
        i_mr_n = self.lineEdit_mr_n.text()
        i_x_d_n = self.lineEdit_x_d_n.text()
        i_x_e_n = self.lineEdit_x_e_n.text()
        i_x_n_n = self.lineEdit_x_n_n.text()
        i_e_d_n = self.lineEdit_e_d_n.text()
        i_e_e_n = self.lineEdit_e_e_n.text()
        i_e_n_n = self.lineEdit_e_n_n.text()
        i_c_d_n = self.lineEdit_c_d_n.text()
        i_c_e_n = self.lineEdit_c_e_n.text()
        i_c_n_n = self.lineEdit_c_n_n.text()
        i_m_d_n = self.lineEdit_m_d_n.text()
        i_m_e_n = self.lineEdit_m_e_n.text()
        i_m_n_n = self.lineEdit_m_n_n.text()
        i_m2_n = self.lineEdit_m2_n.text()

        i_p1 = self.lineEdit_p1.text()
        i_ts1 = self.lineEdit_ts1.text()
        i_te1 = self.lineEdit_te1.text()
        i_ti1 = self.lineEdit_ti1.text()
        i_tn1 = self.lineEdit_tn1.text()
        i_p2 = self.lineEdit_p2.text()
        i_ts2 = self.lineEdit_ts2.text()
        i_te2 = self.lineEdit_te2.text()
        i_ti2 = self.lineEdit_ti2.text()
        i_tn2 = self.lineEdit_tn2.text()
        i_p3 = self.lineEdit_p3.text()
        i_ts3 = self.lineEdit_ts3.text()
        i_te3 = self.lineEdit_te3.text()
        i_ti3 = self.lineEdit_ti3.text()
        i_tn3 = self.lineEdit_tn3.text()    
        i_p4 = self.lineEdit_p4.text()
        i_ts4 = self.lineEdit_ts4.text()
        i_te4 = self.lineEdit_te4.text()
        i_ti4 = self.lineEdit_ti4.text()
        i_tn4 = self.lineEdit_tn4.text()
        i_p5 = self.lineEdit_p5.text()
        i_ts5 = self.lineEdit_ts5.text()
        i_te5 = self.lineEdit_te5.text()
        i_ti5 = self.lineEdit_ti5.text()
        i_tn5 = self.lineEdit_tn5.text()
        i_p6 = self.lineEdit_p6.text()
        i_ts6 = self.lineEdit_ts6.text()
        i_te6 = self.lineEdit_te6.text()
        i_ti6 = self.lineEdit_ti6.text()
        i_tn6 = self.lineEdit_tn6.text()
        i_p7 = self.lineEdit_p7.text()
        i_ts7 = self.lineEdit_ts7.text()
        i_te7 = self.lineEdit_te7.text()
        i_ti7 = self.lineEdit_ti7.text()
        i_tn7 = self.lineEdit_tn7.text()
        i_p8 = self.lineEdit_p8.text()
        i_ts8 = self.lineEdit_ts8.text()
        i_te8 = self.lineEdit_te8.text()
        i_ti8 = self.lineEdit_ti8.text()
        i_tn8 = self.lineEdit_tn8.text()
        i_vac = self.textEdit_vac.toPlainText()
        i_ev = self.textEdit_ev.toPlainText()
        i_edu = self.textEdit_edu.toPlainText()
        i_rep = self.textEdit_rep.toPlainText()
        
        i_i9 = self.lineEdit_i9.text()
        i_ik = self.lineEdit_ik.text()
        i_ih = self.lineEdit_ih.text()
        i_ep_d = self.lineEdit_ep_d.text()
        i_ep_n = self.lineEdit_ep_n.text()

        data = (
            i_dateEdit_report, i_team_leader, i_exaggeration,  i_x1, i_x2, 
            i_x3, i_x5, i_x10, i_r6, i_rs, 
            i_re, i_a9, i_ak, i_ah, i_od,
            i_o_n, i_pd, i_ed, i_xn, i_pn,
            i_en, i_xm, i_so, i_sm, i_hc, 
            i_hb, i_hm, i_cd, i_cn, i_md, 
            i_mn,
            i_x1_p, i_x2_p, i_x3_p, i_x5_p, i_x10_p, 
            i_r6_p, i_rs_p, i_re_p, i_a9_p, i_ak_p, 
            i_ah_p, i_od_p, i_on_p, i_pd_p, i_ed_p, 
            i_xn_p, i_pn_p, i_en_p, i_xm_p, i_so_p, 
            i_he_p, i_ct_p, i_mr_p,
            i_x1_m, i_x2_m, i_x3_m, i_x5_m, i_x10_m, 
            i_r6_m, i_rs_m, i_re_m, i_a9_m, i_ak_m, 
            i_ah_m, i_or_m, i_pd_m, i_ed_m, i_xn_m, 
            i_pn_m, i_en_m, i_xm_m, i_so_m, i_he_m, 
            i_ct_m, i_mr_m,
            i_x1_n, i_x2_n, i_x3_n, i_x5_n, i_x10_n, 
            i_r6_n, i_rs_n, i_re_n, i_a9_n, i_ak_n, 
            i_ah_n, i_or_n, i_pd_n, i_ed_n, i_xn_n, 
            i_pn_n, i_en_n, i_xm_n, i_so_n, i_he_n, 
            i_ct_n, i_mr_n,
            i_x_d_n, i_x_e_n, i_x_n_n, i_e_d_n, i_e_e_n, 
            i_e_n_n, i_c_d_n, i_c_e_n, i_c_n_n, i_m_d_n, 
            i_m_e_n, i_m_n_n, i_m2_n,
            i_p1, i_ts1, i_te1, i_ti1, i_tn1,
            i_p2, i_ts2, i_te2, i_ti2, i_tn2,
            i_p3, i_ts3, i_te3, i_ti3, i_tn3,
            i_p4, i_ts4, i_te4, i_ti4, i_tn4,
            i_p5, i_ts5, i_te5, i_ti5, i_tn5,
            i_p6, i_ts6, i_te6, i_ti6, i_tn6,
            i_p7, i_ts7, i_te7, i_ti7, i_tn7,
            i_p8, i_ts8, i_te8, i_ti8, i_tn8,
            i_vac, i_ev, i_edu, i_rep,
            i_i9, i_ik, i_ih, i_ep_d, i_ep_n
        )

        try:
          conn = pymysql.connect(host="211.186.169.70", user="root", password="1024", db="Daily_report", charset="utf8")
          curs = conn.cursor()
          sql = """
            INSERT INTO report (
                report_date, team_leader, exaggeration, x1, x2, 
                x3, x5, x10, r6, rs, 
                re, a9, ak, ah, od,
                o_n, pd, ed, xn, pn,
                en, xm, so, sm, hc,
                hb, hm, cd, cn, md,
                mn,
                x1_p, x2_p, x3_p, x5_p, x10_p, 
                r6_p, rs_p, re_p, a9_p, ak_p, 
                ah_p, od_p, on_p, pd_p, ed_p, 
                xn_p, pn_p, en_p, xm_p, so_p,
                he_p, ct_p, mr_p,
                x1_m, x2_m, x3_m, x5_m, x10_m, 
                r6_m, rs_m, re_m, a9_m, ak_m, 
                ah_m, or_m, pd_m, ed_m, xn_m, 
                pn_m, en_m, xm_m, so_m, he_m, 
                ct_m, mr_m,
                x1_n, x2_n, x3_n, x5_n, x10_n, 
                r6_n, rs_n, re_n, a9_n, ak_n, 
                ah_n, or_n, pd_n, ed_n, xn_n, 
                pn_n, en_n, xm_n, so_n, he_n, 
                ct_n, mr_n,
                x_d_n, x_e_n, x_n_n, e_d_n, e_e_n, 
                e_n_n, c_d_n, c_e_n, c_n_n, m_d_n, 
                m_e_n, m_n_n, m2_n,
                p1, ts1, te1, ti1, tn1,
                p2, ts2, te2, ti2, tn2,
                p3, ts3, te3, ti3, tn3,
                p4, ts4, te4, ti4, tn4,
                p5, ts5, te5, ti5, tn5,
                p6, ts6, te6, ti6, tn6,
                p7, ts7, te7, ti7, tn7,
                p8, ts8, te8, ti8, tn8,
                vac, ev, edu, rep,
                i9, ik, ih, ep_d, ep_n
                
            ) VALUES (
                %s, %s, %s, %s, %s, 
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s,                    
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s, %s
              )
              """
          curs.execute(sql, data)
          conn.commit()
          
          self.pushButton_save.setEnabled(False)
          

        except pymysql.MySQLError as e:
          QMessageBox.critical(self, "데이터베이스 오류", f"데이터 삽입 중 오류가 발생했습니다: {e}")
        finally:
          conn.close()

                # 재료 데이터 삽입 로직
        QMessageBox.about(self, "재료", "재료 데이터가 입력되었습니다.")

        #----- 날짜 오늘 날짜로
        today = QDate.currentDate() # QDate.currentDate(): 현재 날짜를 반환
        self.dateEdit_report.setDate(today) # setDate(): 'QDateEdit' 위젯에 날짜를 설정
        #--- 저장버튼 비활성화
        self.pushButton_save.setEnabled(False)
        #--- input button 활성화
        self.pushButton_insert.setEnabled(True)

        self.EditClear()
        self.InputClose()

        self.dateEdit_report.setEnabled(True)
        self.pushButton_insert.setEnabled(True)


    #--- 데이터 입력
    def insertData(self):

        #=== 기존 데이터에서 동일한 날짜가 있는지 확인
        # --- 입력날짜
        self.dateVar = self.dateEdit_report.date()
        i_dateEdit_report = self.dateVar.toString('yyyy-MM-dd')

        # 현재 날짜
        current_date = QDate.currentDate().toString('yyyy-MM-dd')

        # 미래 날짜인지 확인
        if i_dateEdit_report > current_date:
            QMessageBox.warning(self, "입력 오류", "미래 날짜는 입력할 수 없습니다.")
            return

        conn = pymysql.connect(
            host="211.186.169.70",
            user="root",
            password="1024",
            db="Daily_report",
            charset="utf8"
        )

        try:
            with conn.cursor() as curs:
                # Check if data for the given date already exists
                check_sql = "SELECT * FROM report WHERE report_date = %s"
                curs.execute(check_sql, (i_dateEdit_report,))
                existing_data = curs.fetchone()

                if existing_data:
                    #--- 데이터 수정 버튼 활성화
                    # self.pushButton_save.setEnabled(True)
                    self.pushButton_update.setEnabled(True)
                    self.DataShow()  # Show existing data
                else:
                    # 새로운 데이터를 입력하시겠습니까?
                    reply = QMessageBox.question(
                        self, "데이터 확인", "새로운 데이터를 입력하시겠습니까?",
                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                        QMessageBox.StandardButton.No
                    )
                    if reply == QMessageBox.StandardButton.Yes:
                        #--- 데이터 저장버튼 활성화
                        self.pushButton_update.setEnabled(False)
                        self.pushButton_save.setEnabled(True)
                        self.EditClear()

                        self.InputOpen()
                        self.LineEditFormat()
                        self.TableWidgetShow()

                        # 장비 기본 값
                        default_text = "이상무"
                        line_edits = [
                            self.lineEdit_x1_m, self.lineEdit_x2_m, self.lineEdit_x3_m, self.lineEdit_x5_m, self.lineEdit_x10_m,
                            self.lineEdit_r6_m, self.lineEdit_rs_m, self.lineEdit_re_m, self.lineEdit_a9_m, self.lineEdit_ak_m,
                            self.lineEdit_ah_m, self.lineEdit_or_m, self.lineEdit_pd_m, self.lineEdit_ed_m, self.lineEdit_xn_m,
                            self.lineEdit_pn_m, self.lineEdit_en_m, self.lineEdit_xm_m, self.lineEdit_so_m, self.lineEdit_he_m,
                            self.lineEdit_ct_m, self.lineEdit_mr_m
                        ]
                        for line_edit in line_edits:
                            line_edit.setText(default_text)

                        self.pushButton_save.setDisabled(False)
                        self.lineEdit_x1.setFocus()
                    else:
                        #--- 루틴 종료
                        return
                    
        except pymysql.MySQLError as e:
            QMessageBox.critical(self, "데이터베이스 오류", f"데이터베이스 연결 중 오류가 발생했습니다: {e}")
        finally:
            conn.close()

    #--- lineEdit 포맷 설정
    def LineEditFormat(self):
        #--- all lineEdit Right Alignment
        self.lineEdit_xt_d.setAlignment(Qt.AlignmentFlag.AlignRight)        
        self.lineEdit_xt_n.setAlignment(Qt.AlignmentFlag.AlignRight) 
        self.lineEdit_xt_d_p.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_xt_n_p.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.lineEdit_et_d.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_et_n.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_et_d_p.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_et_n_p.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.lineEdit_ot_d.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_ot_n.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_ot_d_p.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_ot_n_p.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.lineEdit_pt_d.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_pt_n.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_pt_d_p.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_pt_n_p.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.lineEdit_st_d.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_st_n.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_st_d_p.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_st_n_p.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.lineEdit_at_d.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_at_n.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_at_d_p.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_at_n_p.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.lineEdit_it_d.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_it_n.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_it_d_p.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_it_n_p.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.lineEdit_mt_d.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_mt_n.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_mt_d_p.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_mt_n_p.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.lineEdit_sot_d.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_sot_n.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_sot_d_p.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_sot_n_p.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.lineEdit_ht_d.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_ht_n.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_ht_d_p.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_ht_n_p.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.lineEdit_x_sub.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_x_sub_p.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.lineEdit_s_sub.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_s_sub_p.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.lineEdit_d_sub.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_d_sub_p.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.lineEdit_d_tot.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_d_tot_p.setAlignment(Qt.AlignmentFlag.AlignRight)        

        self.lineEdit_x1.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_x2.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_x3.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_x5.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_x10.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_r6.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_rs.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_re.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_a9.setAlignment(Qt.AlignmentFlag.AlignRight)  
        self.lineEdit_ak.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_ah.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_od.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_on.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_pd.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_ed.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_xn.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_pn.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_en.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_xm.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_so.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_sm.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_hc.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_hb.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_hm.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_cd.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_cn.setAlignment(Qt.AlignmentFlag.AlignRight)  
        self.lineEdit_md.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_mn.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_x1_p.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_x2_p.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_x3_p.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_x5_p.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_x10_p.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_r6_p.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_rs_p.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_re_p.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_a9_p.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_ak_p.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_ah_p.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_od_p.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_on_p.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_pd_p.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_ed_p.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_xn_p.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_pn_p.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_en_p.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_xm_p.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_so_p.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_he_p.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_ct_p.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_mr_p.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_x1_m.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_x2_m.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_x3_m.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_x5_m.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_x10_m.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_r6_m.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_rs_m.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_re_m.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_a9_m.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_ak_m.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_ah_m.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_or_m.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_pd_m.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_ed_m.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_xn_m.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_pn_m.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_en_m.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_xm_m.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_so_m.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_he_m.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_ct_m.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_mr_m.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_x1_n.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_x2_n.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_x3_n.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_x5_n.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_x10_n.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_r6_n.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_rs_n.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_re_n.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_a9_n.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_ak_n.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_ah_n.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_or_n.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_pd_n.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_ed_n.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_xn_n.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_pn_n.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_en_n.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_xm_n.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_so_n.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_he_n.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_ct_n.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_mr_n.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_x_d_n.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_x_e_n.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_x_n_n.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_e_d_n.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_e_e_n.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_e_n_n.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_c_d_n.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_c_e_n.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_c_n_n.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_m_d_n.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_m_e_n.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_m_n_n.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_p1.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_ts1.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_te1.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_ti1.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_tn1.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_p2.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_ts2.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_te2.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_ti2.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_tn2.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_p3.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_ts3.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_te3.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_ti3.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_tn3.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_p4.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_ts4.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_te4.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_ti4.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_tn4.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_p5.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_ts5.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_te5.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_ti5.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_tn5.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_p6.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_ts6.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_te6.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_ti6.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_tn6.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_p7.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_ts7.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_te7.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_ti7.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_tn7.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_p8.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_ts8.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_te8.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_ti8.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_tn8.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_ep_d.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lineEdit_ep_n.setAlignment(Qt.AlignmentFlag.AlignRight)

        #--- lineEdit 숫자만 입력 가능
        self.lineEdit_xt_d.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_xt_n.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_xt_d_p.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_xt_n_p.setValidator(QtGui.QIntValidator(0, 9999))

        self.lineEdit_et_d.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_et_n.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_et_d_p.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_et_n_p.setValidator(QtGui.QIntValidator(0, 9999))

        self.lineEdit_ot_d.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_ot_n.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_ot_d_p.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_ot_n_p.setValidator(QtGui.QIntValidator(0, 9999))

        self.lineEdit_pt_d.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_pt_n.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_pt_d_p.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_pt_n_p.setValidator(QtGui.QIntValidator(0, 9999))

        self.lineEdit_st_d.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_st_n.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_st_d_p.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_st_n_p.setValidator(QtGui.QIntValidator(0, 9999))

        self.lineEdit_at_d.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_at_n.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_at_d_p.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_at_n_p.setValidator(QtGui.QIntValidator(0, 9999))

        self.lineEdit_it_d.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_it_n.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_it_d_p.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_it_n_p.setValidator(QtGui.QIntValidator(0, 9999))

        self.lineEdit_mt_d.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_mt_n.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_mt_d_p.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_mt_n_p.setValidator(QtGui.QIntValidator(0, 9999))

        self.lineEdit_sot_d.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_sot_n.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_sot_d_p.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_sot_n_p.setValidator(QtGui.QIntValidator(0, 9999))

        self.lineEdit_ht_d.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_ht_n.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_ht_d_p.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_ht_n_p.setValidator(QtGui.QIntValidator(0, 9999))

        self.lineEdit_x_sub.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_x_sub_p.setValidator(QtGui.QIntValidator(0, 9999))

        self.lineEdit_s_sub.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_s_sub_p.setValidator(QtGui.QIntValidator(0, 9999))

        self.lineEdit_d_sub.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_d_sub_p.setValidator(QtGui.QIntValidator(0, 9999))

        self.lineEdit_d_tot.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_d_tot_p.setValidator(QtGui.QIntValidator(0, 9999))        
        
        self.lineEdit_x1.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_x2.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_x3.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_x5.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_x10.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_r6.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_rs.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_re.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_a9.setValidator(QtGui.QIntValidator(0, 9999)) 
        self.lineEdit_ak.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_ah.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_od.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_on.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_pd.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_ed.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_xn.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_pn.setValidator(QtGui.QIntValidator(0, 9999)) 
        self.lineEdit_en.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_xm.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_so.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_sm.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_hc.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_hb.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_hm.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_cd.setValidator(QtGui.QIntValidator(0, 9999))     
        self.lineEdit_cn.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_md.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_mn.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_x1_p.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_x2_p.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_x3_p.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_x5_p.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_x10_p.setValidator(QtGui.QIntValidator(0, 9999))  
        self.lineEdit_r6_p.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_rs_p.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_re_p.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_a9_p.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_ak_p.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_ah_p.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_od_p.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_on_p.setValidator(QtGui.QIntValidator(0, 9999))   
        self.lineEdit_pd_p.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_ed_p.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_xn_p.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_pn_p.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_en_p.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_xm_p.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_so_p.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_he_p.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_ct_p.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_mr_p.setValidator(QtGui.QIntValidator(0, 9999))
        
        # self.lineEdit_x1_m.setValidator(QtGui.QIntValidator(0, 9999))
        # self.lineEdit_x2_m.setValidator(QtGui.QIntValidator(0, 9999))
        # self.lineEdit_x3_m.setValidator(QtGui.QIntValidator(0, 9999))
        # self.lineEdit_x5_m.setValidator(QtGui.QIntValidator(0, 9999))
        # self.lineEdit_x10_m.setValidator(QtGui.QIntValidator(0, 9999))
        # self.lineEdit_r6_m.setValidator(QtGui.QIntValidator(0, 9999))   
        # self.lineEdit_rs_m.setValidator(QtGui.QIntValidator(0, 9999))
        # self.lineEdit_re_m.setValidator(QtGui.QIntValidator(0, 9999))
        # self.lineEdit_a9_m.setValidator(QtGui.QIntValidator(0, 9999))
        # self.lineEdit_ak_m.setValidator(QtGui.QIntValidator(0, 9999))
        # self.lineEdit_ah_m.setValidator(QtGui.QIntValidator(0, 9999))
        # self.lineEdit_or_m.setValidator(QtGui.QIntValidator(0, 9999))
        # self.lineEdit_pd_m.setValidator(QtGui.QIntValidator(0, 9999))
        # self.lineEdit_ed_m.setValidator(QtGui.QIntValidator(0, 9999))
        # self.lineEdit_xn_m.setValidator(QtGui.QIntValidator(0, 9999))
        # self.lineEdit_pn_m.setValidator(QtGui.QIntValidator(0, 9999))
        # self.lineEdit_en_m.setValidator(QtGui.QIntValidator(0, 9999))
        # self.lineEdit_xm_m.setValidator(QtGui.QIntValidator(0, 9999))
        # self.lineEdit_so_m.setValidator(QtGui.QIntValidator(0, 9999))
        # self.lineEdit_he_m.setValidator(QtGui.QIntValidator(0, 9999))
        # self.lineEdit_ct_m.setValidator(QtGui.QIntValidator(0, 9999))
        # self.lineEdit_mr_m.setValidator(QtGui.QIntValidator(0, 9999))   
        # self.lineEdit_x1_n.setValidator(QtGui.QIntValidator(0, 9999))
        # self.lineEdit_x2_n.setValidator(QtGui.QIntValidator(0, 9999))
        # self.lineEdit_x3_n.setValidator(QtGui.QIntValidator(0, 9999))
        # self.lineEdit_x5_n.setValidator(QtGui.QIntValidator(0, 9999))
        # self.lineEdit_x10_n.setValidator(QtGui.QIntValidator(0, 9999))
        # self.lineEdit_r6_n.setValidator(QtGui.QIntValidator(0, 9999))
        # self.lineEdit_rs_n.setValidator(QtGui.QIntValidator(0, 9999))
        # self.lineEdit_re_n.setValidator(QtGui.QIntValidator(0, 9999))
        # self.lineEdit_a9_n.setValidator(QtGui.QIntValidator(0, 9999))
        # self.lineEdit_ak_n.setValidator(QtGui.QIntValidator(0, 9999))
        # self.lineEdit_ah_n.setValidator(QtGui.QIntValidator(0, 9999))
        # self.lineEdit_or_n.setValidator(QtGui.QIntValidator(0, 9999))
        # self.lineEdit_pd_n.setValidator(QtGui.QIntValidator(0, 9999))
        # self.lineEdit_ed_n.setValidator(QtGui.QIntValidator(0, 9999))
        # self.lineEdit_xn_n.setValidator(QtGui.QIntValidator(0, 9999))
        # self.lineEdit_pn_n.setValidator(QtGui.QIntValidator(0, 9999))
        # self.lineEdit_en_n.setValidator(QtGui.QIntValidator(0, 9999))
        # self.lineEdit_xm_n.setValidator(QtGui.QIntValidator(0, 9999))
        # self.lineEdit_so_n.setValidator(QtGui.QIntValidator(0, 9999))
        # self.lineEdit_he_n.setValidator(QtGui.QIntValidator(0, 9999))
        # self.lineEdit_ct_n.setValidator(QtGui.QIntValidator(0, 9999))
        # self.lineEdit_mr_n.setValidator(QtGui.QIntValidator(0, 9999))
        # self.lineEdit_x_d_n.setValidator(QtGui.QIntValidator(0, 9999))
        # self.lineEdit_x_e_n.setValidator(QtGui.QIntValidator(0, 9999))
        # self.lineEdit_x_n_n.setValidator(QtGui.QIntValidator(0, 9999))
        # self.lineEdit_e_d_n.setValidator(QtGui.QIntValidator(0, 9999))
        # self.lineEdit_e_e_n.setValidator(QtGui.QIntValidator(0, 9999))
        # self.lineEdit_e_n_n.setValidator(QtGui.QIntValidator(0, 9999))
        # self.lineEdit_c_d_n.setValidator(QtGui.QIntValidator(0, 9999))
        # self.lineEdit_c_e_n.setValidator(QtGui.QIntValidator(0, 9999))
        # self.lineEdit_c_n_n.setValidator(QtGui.QIntValidator(0, 9999))
        # self.lineEdit_m_d_n.setValidator(QtGui.QIntValidator(0, 9999))
        # self.lineEdit_m_e_n.setValidator(QtGui.QIntValidator(0, 9999))
        # self.lineEdit_m_n_n.setValidator(QtGui.QIntValidator(0, 9999))
        # self.lineEdit_p1.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_ts1.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_te1.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_ti1.setValidator(QDoubleValidator(0.0, 99.9, 1))
        # self.lineEdit_tn1.setValidator(QtGui.QIntValidator(0, 9999))
        # self.lineEdit_p2.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_ts2.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_te2.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_ti2.setValidator(QDoubleValidator(0.0, 99.9, 1))
        # self.lineEdit_tn2.setValidator(QtGui.QIntValidator(0, 9999))
        # self.lineEdit_p3.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_ts3.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_te3.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_ti3.setValidator(QDoubleValidator(0.0, 99.9, 1))
        # self.lineEdit_tn3.setValidator(QtGui.QIntValidator(0, 9999))
        # self.lineEdit_p4.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_ts4.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_te4.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_ti4.setValidator(QDoubleValidator(0.0, 99.9, 1))
        # self.lineEdit_tn4.setValidator(QtGui.QIntValidator(0, 9999))
        # self.lineEdit_p5.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_ts5.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_te5.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_ti5.setValidator(QDoubleValidator(0.0, 99.9, 1))
        # self.lineEdit_tn5.setValidator(QtGui.QIntValidator(0, 9999))
        # self.lineEdit_p6.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_ts6.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_te6.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_ti6.setValidator(QDoubleValidator(0.0, 99.9, 1))
        # self.lineEdit_tn6.setValidator(QtGui.QIntValidator(0, 9999))
        # self.lineEdit_p7.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_ts7.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_te7.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_ti7.setValidator(QDoubleValidator(0.0, 99.9, 1))
        # self.lineEdit_tn7.setValidator(QtGui.QIntValidator(0, 9999))
        # self.lineEdit_p8.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_ts8.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_te8.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_ti8.setValidator(QDoubleValidator(0.0, 9999.9, 1))
        # self.lineEdit_tn8.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_ep_d.setValidator(QtGui.QIntValidator(0, 9999))
        self.lineEdit_ep_n.setValidator(QtGui.QIntValidator(0, 9999))

    #---입력창 활성
    def InputOpen(self):
        self.dateEdit_report.setEnabled(False)
        self.lineEdit_x1.setReadOnly(False)
        self.lineEdit_x2.setReadOnly(False)
        self.lineEdit_x3.setReadOnly(False)
        self.lineEdit_x5.setReadOnly(False)
        self.lineEdit_x10.setReadOnly(False)
        self.lineEdit_r6.setReadOnly(False)
        self.lineEdit_rs.setReadOnly(False)
        self.lineEdit_re.setReadOnly(False)
        self.lineEdit_a9.setReadOnly(False)
        self.lineEdit_ak.setReadOnly(False)
        self.lineEdit_ah.setReadOnly(False)
        self.lineEdit_od.setReadOnly(False)
        self.lineEdit_on.setReadOnly(False)
        self.lineEdit_pd.setReadOnly(False)
        self.lineEdit_ed.setReadOnly(False)
        self.lineEdit_xn.setReadOnly(False)
        self.lineEdit_pn.setReadOnly(False)
        self.lineEdit_en.setReadOnly(False)
        self.lineEdit_xm.setReadOnly(False)
        self.lineEdit_so.setReadOnly(False)
        self.lineEdit_sm.setReadOnly(False)
        self.lineEdit_hc.setReadOnly(False)
        self.lineEdit_hb.setReadOnly(False)
        self.lineEdit_hm.setReadOnly(False)
        self.lineEdit_cd.setReadOnly(False)
        self.lineEdit_cn.setReadOnly(False)
        self.lineEdit_md.setReadOnly(False)
        self.lineEdit_mn.setReadOnly(False)
        self.lineEdit_x1_p.setReadOnly(False)
        self.lineEdit_x2_p.setReadOnly(False)
        self.lineEdit_x3_p.setReadOnly(False)
        self.lineEdit_x5_p.setReadOnly(False)
        self.lineEdit_x10_p.setReadOnly(False)
        self.lineEdit_r6_p.setReadOnly(False)
        self.lineEdit_rs_p.setReadOnly(False)
        self.lineEdit_re_p.setReadOnly(False)
        self.lineEdit_a9_p.setReadOnly(False)
        self.lineEdit_ak_p.setReadOnly(False)
        self.lineEdit_ah_p.setReadOnly(False)
        self.lineEdit_od_p.setReadOnly(False)
        self.lineEdit_on_p.setReadOnly(False)
        self.lineEdit_pd_p.setReadOnly(False)
        self.lineEdit_ed_p.setReadOnly(False)
        self.lineEdit_xn_p.setReadOnly(False)
        self.lineEdit_pn_p.setReadOnly(False)
        self.lineEdit_en_p.setReadOnly(False)
        self.lineEdit_xm_p.setReadOnly(False)
        self.lineEdit_so_p.setReadOnly(False)
        self.lineEdit_he_p.setReadOnly(False)
        self.lineEdit_ct_p.setReadOnly(False)
        self.lineEdit_mr_p.setReadOnly(False)
        self.lineEdit_x1_m.setReadOnly(False)
        self.lineEdit_x2_m.setReadOnly(False)
        self.lineEdit_x3_m.setReadOnly(False)
        self.lineEdit_x5_m.setReadOnly(False)
        self.lineEdit_x10_m.setReadOnly(False)
        self.lineEdit_r6_m.setReadOnly(False)
        self.lineEdit_rs_m.setReadOnly(False)
        self.lineEdit_re_m.setReadOnly(False)
        self.lineEdit_a9_m.setReadOnly(False)
        self.lineEdit_ak_m.setReadOnly(False)
        self.lineEdit_ah_m.setReadOnly(False)
        self.lineEdit_or_m.setReadOnly(False)
        self.lineEdit_pd_m.setReadOnly(False)
        self.lineEdit_ed_m.setReadOnly(False)
        self.lineEdit_xn_m.setReadOnly(False)
        self.lineEdit_pn_m.setReadOnly(False)
        self.lineEdit_en_m.setReadOnly(False)
        self.lineEdit_xm_m.setReadOnly(False)
        self.lineEdit_so_m.setReadOnly(False)
        self.lineEdit_he_m.setReadOnly(False)
        self.lineEdit_ct_m.setReadOnly(False)
        self.lineEdit_mr_m.setReadOnly(False)
        self.lineEdit_x1_n.setReadOnly(False)
        self.lineEdit_x2_n.setReadOnly(False)
        self.lineEdit_x3_n.setReadOnly(False)
        self.lineEdit_x5_n.setReadOnly(False)
        self.lineEdit_x10_n.setReadOnly(False)
        self.lineEdit_r6_n.setReadOnly(False)
        self.lineEdit_rs_n.setReadOnly(False)
        self.lineEdit_re_n.setReadOnly(False)
        self.lineEdit_a9_n.setReadOnly(False)
        self.lineEdit_ak_n.setReadOnly(False)
        self.lineEdit_ah_n.setReadOnly(False)
        self.lineEdit_or_n.setReadOnly(False)
        self.lineEdit_pd_n.setReadOnly(False)
        self.lineEdit_ed_n.setReadOnly(False)
        self.lineEdit_xn_n.setReadOnly(False)
        self.lineEdit_pn_n.setReadOnly(False)
        self.lineEdit_en_n.setReadOnly(False)
        self.lineEdit_xm_n.setReadOnly(False)
        self.lineEdit_so_n.setReadOnly(False)
        self.lineEdit_he_n.setReadOnly(False)
        self.lineEdit_ct_n.setReadOnly(False)
        self.lineEdit_mr_n.setReadOnly(False)
        self.lineEdit_x_d_n.setReadOnly(False)
        self.lineEdit_x_e_n.setReadOnly(False)
        self.lineEdit_x_n_n.setReadOnly(False)
        self.lineEdit_e_d_n.setReadOnly(False)
        self.lineEdit_e_e_n.setReadOnly(False)
        self.lineEdit_e_n_n.setReadOnly(False)
        self.lineEdit_c_d_n.setReadOnly(False)
        self.lineEdit_c_e_n.setReadOnly(False)
        self.lineEdit_c_n_n.setReadOnly(False)
        self.lineEdit_m_d_n.setReadOnly(False)
        self.lineEdit_m_e_n.setReadOnly(False)
        self.lineEdit_m_n_n.setReadOnly(False)
        self.lineEdit_p1.setReadOnly(False)
        self.lineEdit_ts1.setReadOnly(False)
        self.lineEdit_te1.setReadOnly(False)
        self.lineEdit_ti1.setReadOnly(False)
        self.lineEdit_tn1.setReadOnly(False)
        self.lineEdit_p2.setReadOnly(False)
        self.lineEdit_ts2.setReadOnly(False)
        self.lineEdit_te2.setReadOnly(False)
        self.lineEdit_ti2.setReadOnly(False)
        self.lineEdit_tn2.setReadOnly(False)
        self.lineEdit_p3.setReadOnly(False)
        self.lineEdit_ts3.setReadOnly(False)
        self.lineEdit_te3.setReadOnly(False)
        self.lineEdit_ti3.setReadOnly(False)
        self.lineEdit_tn3.setReadOnly(False)
        self.lineEdit_p4.setReadOnly(False)
        self.lineEdit_ts4.setReadOnly(False)
        self.lineEdit_te4.setReadOnly(False)
        self.lineEdit_ti4.setReadOnly(False)
        self.lineEdit_tn4.setReadOnly(False)
        self.lineEdit_p5.setReadOnly(False)
        self.lineEdit_ts5.setReadOnly(False)
        self.lineEdit_te5.setReadOnly(False)
        self.lineEdit_ti5.setReadOnly(False)
        self.lineEdit_tn5.setReadOnly(False)
        self.lineEdit_p6.setReadOnly(False)
        self.lineEdit_ts6.setReadOnly(False)
        self.lineEdit_te6.setReadOnly(False)
        self.lineEdit_ti6.setReadOnly(False)
        self.lineEdit_tn6.setReadOnly(False)
        self.lineEdit_p7.setReadOnly(False)
        self.lineEdit_ts7.setReadOnly(False)
        self.lineEdit_te7.setReadOnly(False)
        self.lineEdit_ti7.setReadOnly(False)
        self.lineEdit_tn7.setReadOnly(False)
        self.lineEdit_p8.setReadOnly(False)
        self.lineEdit_ts8.setReadOnly(False)
        self.lineEdit_te8.setReadOnly(False)
        self.lineEdit_ti8.setReadOnly(False)
        self.lineEdit_tn8.setReadOnly(False)
        self.textEdit_vac.setReadOnly(False)
        self.textEdit_ev.setReadOnly(False)
        self.textEdit_edu.setReadOnly(False)
        self.textEdit_rep.setReadOnly(False)
        self.lineEdit_ep_d.setReadOnly(False)
        self.lineEdit_ep_n.setReadOnly(False)

        self.lineEdit_i9.setReadOnly(False)
        self.lineEdit_ik.setReadOnly(False)
        self.lineEdit_ih.setReadOnly(False)
        #--- 버튼 활성 및 비활성
        self.pushButton_save.setDisabled(False)
        self.pushButton_insert.setDisabled(True)
    
    #--- 입력창 비활성
    def InputClose(self):

        #--- 오늘 날짜로 설정 후 입력 대기 상태
        self.dateEdit_report.setCalendarPopup(True)
        # self.dateEdit_report.setFocus()

        self.lineEdit_xt_d.setReadOnly(True)
        self.lineEdit_xt_n.setReadOnly(True)
        self.lineEdit_xt_d_p.setReadOnly(True)
        self.lineEdit_xt_n_p.setReadOnly(True)

        self.lineEdit_et_d.setReadOnly(True)
        self.lineEdit_et_n.setReadOnly(True)
        self.lineEdit_et_d_p.setReadOnly(True)
        self.lineEdit_et_n_p.setReadOnly(True)

        self.lineEdit_ot_d.setReadOnly(True)
        self.lineEdit_ot_n.setReadOnly(True)
        self.lineEdit_ot_d_p.setReadOnly(True)
        self.lineEdit_ot_n_p.setReadOnly(True)

        self.lineEdit_pt_d.setReadOnly(True)
        self.lineEdit_pt_n.setReadOnly(True)
        self.lineEdit_pt_d_p.setReadOnly(True)
        self.lineEdit_pt_n_p.setReadOnly(True)

        self.lineEdit_st_d.setReadOnly(True)
        self.lineEdit_st_n.setReadOnly(True)
        self.lineEdit_st_d_p.setReadOnly(True)
        self.lineEdit_st_n_p.setReadOnly(True)

        self.lineEdit_at_d.setReadOnly(True)
        self.lineEdit_at_n.setReadOnly(True)
        self.lineEdit_at_d_p.setReadOnly(True)
        self.lineEdit_at_n_p.setReadOnly(True)

        self.lineEdit_it_d.setReadOnly(True)
        self.lineEdit_it_n.setReadOnly(True)
        self.lineEdit_it_d_p.setReadOnly(True)
        self.lineEdit_it_n_p.setReadOnly(True)

        self.lineEdit_mt_d.setReadOnly(True)
        self.lineEdit_mt_n.setReadOnly(True)
        self.lineEdit_mt_d_p.setReadOnly(True)
        self.lineEdit_mt_n_p.setReadOnly(True)

        self.lineEdit_sot_d.setReadOnly(True)
        self.lineEdit_sot_n.setReadOnly(True)
        self.lineEdit_sot_d_p.setReadOnly(True)
        self.lineEdit_sot_n_p.setReadOnly(True)

        self.lineEdit_ht_d.setReadOnly(True)
        self.lineEdit_ht_n.setReadOnly(True)
        self.lineEdit_ht_d_p.setReadOnly(True)
        self.lineEdit_ht_n_p.setReadOnly(True)

        self.lineEdit_x_sub.setReadOnly(True)
        self.lineEdit_x_sub_p.setReadOnly(True)

        self.lineEdit_s_sub.setReadOnly(True)
        self.lineEdit_s_sub_p.setReadOnly(True)

        self.lineEdit_d_sub.setReadOnly(True)
        self.lineEdit_d_sub_p.setReadOnly(True)

        self.lineEdit_d_tot.setReadOnly(True)
        self.lineEdit_d_tot_p.setReadOnly(True)
    
        self.lineEdit_x1.setReadOnly(True)
        self.lineEdit_x2.setReadOnly(True)
        self.lineEdit_x3.setReadOnly(True)
        self.lineEdit_x5.setReadOnly(True)
        self.lineEdit_x10.setReadOnly(True)
        self.lineEdit_r6.setReadOnly(True)
        self.lineEdit_rs.setReadOnly(True)
        self.lineEdit_re.setReadOnly(True)
        self.lineEdit_a9.setReadOnly(True)
        self.lineEdit_ak.setReadOnly(True)
        self.lineEdit_ah.setReadOnly(True)
        self.lineEdit_od.setReadOnly(True)
        self.lineEdit_on.setReadOnly(True)
        self.lineEdit_pd.setReadOnly(True)
        self.lineEdit_ed.setReadOnly(True)
        self.lineEdit_xn.setReadOnly(True)
        self.lineEdit_pn.setReadOnly(True)
        self.lineEdit_en.setReadOnly(True)
        self.lineEdit_xm.setReadOnly(True)
        self.lineEdit_so.setReadOnly(True)
        self.lineEdit_sm.setReadOnly(True)
        self.lineEdit_hc.setReadOnly(True)
        self.lineEdit_hb.setReadOnly(True)
        self.lineEdit_hm.setReadOnly(True)
        self.lineEdit_cd.setReadOnly(True)
        self.lineEdit_cn.setReadOnly(True)
        self.lineEdit_md.setReadOnly(True)
        self.lineEdit_mn.setReadOnly(True)
        self.lineEdit_x1_p.setReadOnly(True)
        self.lineEdit_x2_p.setReadOnly(True)
        self.lineEdit_x3_p.setReadOnly(True)
        self.lineEdit_x5_p.setReadOnly(True)
        self.lineEdit_x10_p.setReadOnly(True)
        self.lineEdit_r6_p.setReadOnly(True)
        self.lineEdit_rs_p.setReadOnly(True)
        self.lineEdit_re_p.setReadOnly(True)
        self.lineEdit_a9_p.setReadOnly(True)
        self.lineEdit_ak_p.setReadOnly(True)
        self.lineEdit_ah_p.setReadOnly(True)
        self.lineEdit_od_p.setReadOnly(True)
        self.lineEdit_on_p.setReadOnly(True)
        self.lineEdit_pd_p.setReadOnly(True)
        self.lineEdit_ed_p.setReadOnly(True)
        self.lineEdit_xn_p.setReadOnly(True)
        self.lineEdit_pn_p.setReadOnly(True)
        self.lineEdit_en_p.setReadOnly(True)
        self.lineEdit_xm_p.setReadOnly(True)
        self.lineEdit_so_p.setReadOnly(True)
        self.lineEdit_he_p.setReadOnly(True)
        self.lineEdit_ct_p.setReadOnly(True)
        self.lineEdit_mr_p.setReadOnly(True)
        self.lineEdit_x1_m.setReadOnly(True)
        self.lineEdit_x2_m.setReadOnly(True)
        self.lineEdit_x3_m.setReadOnly(True)
        self.lineEdit_x5_m.setReadOnly(True)
        self.lineEdit_x10_m.setReadOnly(True)
        self.lineEdit_r6_m.setReadOnly(True)
        self.lineEdit_rs_m.setReadOnly(True)
        self.lineEdit_re_m.setReadOnly(True)
        self.lineEdit_a9_m.setReadOnly(True)
        self.lineEdit_ak_m.setReadOnly(True)
        self.lineEdit_ah_m.setReadOnly(True)
        self.lineEdit_or_m.setReadOnly(True)
        self.lineEdit_pd_m.setReadOnly(True)
        self.lineEdit_ed_m.setReadOnly(True)
        self.lineEdit_xn_m.setReadOnly(True)
        self.lineEdit_pn_m.setReadOnly(True)
        self.lineEdit_en_m.setReadOnly(True)
        self.lineEdit_xm_m.setReadOnly(True)
        self.lineEdit_so_m.setReadOnly(True)
        self.lineEdit_he_m.setReadOnly(True)
        self.lineEdit_ct_m.setReadOnly(True)
        self.lineEdit_mr_m.setReadOnly(True)
        self.lineEdit_x1_n.setReadOnly(True)
        self.lineEdit_x2_n.setReadOnly(True)
        self.lineEdit_x3_n.setReadOnly(True)
        self.lineEdit_x5_n.setReadOnly(True)
        self.lineEdit_x10_n.setReadOnly(True)
        self.lineEdit_r6_n.setReadOnly(True)
        self.lineEdit_rs_n.setReadOnly(True)
        self.lineEdit_re_n.setReadOnly(True)
        self.lineEdit_a9_n.setReadOnly(True)
        self.lineEdit_ak_n.setReadOnly(True)
        self.lineEdit_ah_n.setReadOnly(True)
        self.lineEdit_or_n.setReadOnly(True)
        self.lineEdit_pd_n.setReadOnly(True)
        self.lineEdit_ed_n.setReadOnly(True)
        self.lineEdit_xn_n.setReadOnly(True)
        self.lineEdit_pn_n.setReadOnly(True)
        self.lineEdit_en_n.setReadOnly(True)
        self.lineEdit_xm_n.setReadOnly(True)
        self.lineEdit_so_n.setReadOnly(True)
        self.lineEdit_he_n.setReadOnly(True)
        self.lineEdit_ct_n.setReadOnly(True)
        self.lineEdit_mr_n.setReadOnly(True)
        self.lineEdit_x_d_n.setReadOnly(True)
        self.lineEdit_x_e_n.setReadOnly(True)
        self.lineEdit_x_n_n.setReadOnly(True)
        self.lineEdit_e_d_n.setReadOnly(True)
        self.lineEdit_e_e_n.setReadOnly(True)
        self.lineEdit_e_n_n.setReadOnly(True)
        self.lineEdit_c_d_n.setReadOnly(True)
        self.lineEdit_c_e_n.setReadOnly(True)
        self.lineEdit_c_n_n.setReadOnly(True)
        self.lineEdit_m_d_n.setReadOnly(True)
        self.lineEdit_m_e_n.setReadOnly(True)
        self.lineEdit_m_n_n.setReadOnly(True)
        self.lineEdit_p1.setReadOnly(True)
        self.lineEdit_ts1.setReadOnly(True)
        self.lineEdit_te1.setReadOnly(True)
        self.lineEdit_ti1.setReadOnly(True)
        self.lineEdit_tn1.setReadOnly(True)
        self.lineEdit_p2.setReadOnly(True)
        self.lineEdit_ts2.setReadOnly(True)
        self.lineEdit_te2.setReadOnly(True)
        self.lineEdit_ti2.setReadOnly(True)
        self.lineEdit_tn2.setReadOnly(True)
        self.lineEdit_p3.setReadOnly(True)
        self.lineEdit_ts3.setReadOnly(True)
        self.lineEdit_te3.setReadOnly(True)
        self.lineEdit_ti3.setReadOnly(True)
        self.lineEdit_tn3.setReadOnly(True)
        self.lineEdit_p4.setReadOnly(True)
        self.lineEdit_ts4.setReadOnly(True)
        self.lineEdit_te4.setReadOnly(True)
        self.lineEdit_ti4.setReadOnly(True)
        self.lineEdit_tn4.setReadOnly(True)
        self.lineEdit_p5.setReadOnly(True)
        self.lineEdit_ts5.setReadOnly(True)
        self.lineEdit_te5.setReadOnly(True)
        self.lineEdit_ti5.setReadOnly(True)
        self.lineEdit_tn5.setReadOnly(True)
        self.lineEdit_p6.setReadOnly(True)
        self.lineEdit_ts6.setReadOnly(True)
        self.lineEdit_te6.setReadOnly(True)
        self.lineEdit_ti6.setReadOnly(True)
        self.lineEdit_tn6.setReadOnly(True)
        self.lineEdit_p7.setReadOnly(True)
        self.lineEdit_ts7.setReadOnly(True)
        self.lineEdit_te7.setReadOnly(True)
        self.lineEdit_ti7.setReadOnly(True)
        self.lineEdit_tn7.setReadOnly(True)
        self.lineEdit_p8.setReadOnly(True)
        self.lineEdit_ts8.setReadOnly(True)
        self.lineEdit_te8.setReadOnly(True)
        self.lineEdit_ti8.setReadOnly(True)
        self.lineEdit_tn8.setReadOnly(True)
        self.textEdit_vac.setReadOnly(True)
        self.textEdit_ev.setReadOnly(True)
        self.textEdit_edu.setReadOnly(True)
        self.textEdit_rep.setReadOnly(True)
        self.lineEdit_ep_d.setReadOnly(True)
        self.lineEdit_ep_n.setReadOnly(True)

        self.lineEdit_i9.setReadOnly(True)
        self.lineEdit_ik.setReadOnly(True)
        self.lineEdit_ih.setReadOnly(True)  
        
        #--- 버튼 활성 및 비활성
        self.pushButton_save.setDisabled(True)
        self.pushButton_insert.setDisabled(False)
        self.pushButton_quit.setDisabled(False)

    def insert1Data(self):
        
        #---- date(시술일)
        self.dateVar = self.dateEdit_report.date()
        i_dateEdit_report = self.dateVar.toString('yyyy-MM-dd')

        #---- checkBox (Default unchecked)
        i_team_leader = "ok" if self.checkBox_team.isChecked() else ""
        i_exaggeration = "ok" if self.checkBox_exaggeration.isChecked() else ""

        self.lineEdit_x1.setFocus()

        # # lineEdit 데이터 가져오기
        i_x1 = self.lineEdit_x1.text()
        i_x2 = self.lineEdit_x2.text()
        i_x3 = self.lineEdit_x3.text()
        i_x5 = self.lineEdit_x5.text()
        i_x10 = self.lineEdit_x10.text()
        i_r6 = self.lineEdit_r6.text()
        i_rs = self.lineEdit_rs.text()
        i_re = self.lineEdit_re.text()
        i_a9 = self.lineEdit_a9.text()
        i_ak = self.lineEdit_ak.text()
        i_ah = self.lineEdit_ah.text()
        i_od = self.lineEdit_od.text()
        i_on = self.lineEdit_on.text()
        i_pd = self.lineEdit_pd.text()
        i_ed = self.lineEdit_ed.text()
        i_xn = self.lineEdit_xn.text()
        i_pn = self.lineEdit_pn.text()
        i_en = self.lineEdit_en.text()
        i_xm = self.lineEdit_xm.text()
        i_so = self.lineEdit_so.text()
        i_sm = self.lineEdit_sm.text()
        i_hc = self.lineEdit_hc.text()
        i_hb = self.lineEdit_hb.text()
        i_hm = self.lineEdit_hm.text()
        i_cd = self.lineEdit_cd.text()
        i_cn = self.lineEdit_cn.text()
        i_md = self.lineEdit_md.text()
        i_mn = self.lineEdit_mn.text()
        i_x1_p = self.lineEdit_x1_p.text()
        i_x2_p = self.lineEdit_x2_p.text()
        i_x3_p = self.lineEdit_x3_p.text()
        i_x5_p = self.lineEdit_x5_p.text()
        i_x10_p = self.lineEdit_x10_p.text()
        i_r6_p = self.lineEdit_r6_p.text()
        i_rs_p = self.lineEdit_rs_p.text()
        i_re_p = self.lineEdit_re_p.text()
        i_a9_p = self.lineEdit_a9_p.text()
        i_ak_p = self.lineEdit_ak_p.text()
        i_ah_p = self.lineEdit_ah_p.text()
        i_od_p = self.lineEdit_od_p.text()
        i_on_p = self.lineEdit_on_p.text()
        i_pd_p = self.lineEdit_pd_p.text()
        i_ed_p = self.lineEdit_ed_p.text()      
        i_xn_p = self.lineEdit_xn_p.text()
        i_pn_p = self.lineEdit_pn_p.text()
        i_en_p = self.lineEdit_en_p.text()
        i_xm_p = self.lineEdit_xm_p.text()
        i_so_p = self.lineEdit_so_p.text()
        i_he_p = self.lineEdit_he_p.text()
        i_ct_p = self.lineEdit_ct_p.text()
        i_mr_p = self.lineEdit_mr_p.text()  
        i_x1_m = self.lineEdit_x1_m.text()
        i_x2_m = self.lineEdit_x2_m.text()
        i_x3_m = self.lineEdit_x3_m.text()
        i_x5_m = self.lineEdit_x5_m.text()
        i_x10_m = self.lineEdit_x10_m.text()
        i_r6_m = self.lineEdit_r6_m.text()
        i_rs_m = self.lineEdit_rs_m.text()
        i_re_m = self.lineEdit_re_m.text()
        i_a9_m = self.lineEdit_a9_m.text()
        i_ak_m = self.lineEdit_ak_m.text()
        i_ah_m = self.lineEdit_ah_m.text()
        i_or_m = self.lineEdit_or_m.text()
        i_pd_m = self.lineEdit_pd_m.text()
        i_ed_m = self.lineEdit_ed_m.text()
        i_xn_m = self.lineEdit_xn_m.text()
        i_pn_m = self.lineEdit_pn_m.text()
        i_en_m = self.lineEdit_en_m.text()
        i_xm_m = self.lineEdit_xm_m.text()
        i_so_m = self.lineEdit_so_m.text()
        i_he_m = self.lineEdit_he_m.text()
        i_ct_m = self.lineEdit_ct_m.text()
        i_mr_m = self.lineEdit_mr_m.text()
        i_x1_n = self.lineEdit_x1_n.text()
        i_x2_n = self.lineEdit_x2_n.text()
        i_x3_n = self.lineEdit_x3_n.text()
        i_x5_n = self.lineEdit_x5_n.text()
        i_x10_n = self.lineEdit_x10_n.text()
        i_r6_n = self.lineEdit_r6_n.text()
        i_rs_n = self.lineEdit_rs_n.text()
        i_re_n = self.lineEdit_re_n.text()
        i_a9_n = self.lineEdit_a9_n.text()
        i_ak_n = self.lineEdit_ak_n.text()
        i_ah_n = self.lineEdit_ah_n.text()
        i_or_n = self.lineEdit_or_n.text()
        i_pd_n = self.lineEdit_pd_n.text()
        i_ed_n = self.lineEdit_ed_n.text()
        i_xn_n = self.lineEdit_xn_n.text()
        i_pn_n = self.lineEdit_pn_n.text()
        i_en_n = self.lineEdit_en_n.text()
        i_xm_n = self.lineEdit_xm_n.text()
        i_so_n = self.lineEdit_so_n.text()
        i_he_n = self.lineEdit_he_n.text()
        i_ct_n = self.lineEdit_ct_n.text()
        i_mr_n = self.lineEdit_mr_n.text()
        i_x_d_n = self.lineEdit_x_d_n.text()
        i_x_e_n = self.lineEdit_x_e_n.text()
        i_x_n_n = self.lineEdit_x_n_n.text()
        i_e_d_n = self.lineEdit_e_d_n.text()
        i_e_e_n = self.lineEdit_e_e_n.text()
        i_e_n_n = self.lineEdit_e_n_n.text()
        i_c_d_n = self.lineEdit_c_d_n.text()
        i_c_e_n = self.lineEdit_c_e_n.text()
        i_c_n_n = self.lineEdit_c_n_n.text()
        i_m_d_n = self.lineEdit_m_d_n.text()
        i_m_e_n = self.lineEdit_m_e_n.text()
        i_m_n_n = self.lineEdit_m_n_n.text()
        i_p1 = self.lineEdit_p1.text()
        i_ts1 = self.lineEdit_ts1.text()
        i_te1 = self.lineEdit_te1.text()
        i_ti1 = self.lineEdit_ti1.text()
        i_tn1 = self.lineEdit_tn1.text()
        i_p2 = self.lineEdit_p2.text()
        i_ts2 = self.lineEdit_ts2.text()
        i_te2 = self.lineEdit_te2.text()
        i_ti2 = self.lineEdit_ti2.text()
        i_tn2 = self.lineEdit_tn2.text()
        i_p3 = self.lineEdit_p3.text()
        i_ts3 = self.lineEdit_ts3.text()
        i_te3 = self.lineEdit_te3.text()
        i_ti3 = self.lineEdit_ti3.text()
        i_tn3 = self.lineEdit_tn3.text()    
        i_p4 = self.lineEdit_p4.text()
        i_ts4 = self.lineEdit_ts4.text()
        i_te4 = self.lineEdit_te4.text()
        i_ti4 = self.lineEdit_ti4.text()
        i_tn4 = self.lineEdit_tn4.text()
        i_p5 = self.lineEdit_p5.text()
        i_ts5 = self.lineEdit_ts5.text()
        i_te5 = self.lineEdit_te5.text()
        i_ti5 = self.lineEdit_ti5.text()
        i_tn5 = self.lineEdit_tn5.text()
        i_p6 = self.lineEdit_p6.text()
        i_ts6 = self.lineEdit_ts6.text()
        i_te6 = self.lineEdit_te6.text()
        i_ti6 = self.lineEdit_ti6.text()
        i_tn6 = self.lineEdit_tn6.text()
        i_p7 = self.lineEdit_p7.text()
        i_ts7 = self.lineEdit_ts7.text()
        i_te7 = self.lineEdit_te7.text()
        i_ti7 = self.lineEdit_ti7.text()
        i_tn7 = self.lineEdit_tn7.text()
        i_p8 = self.lineEdit_p8.text()
        i_ts8 = self.lineEdit_ts8.text()
        i_te8 = self.lineEdit_te8.text()
        i_ti8 = self.lineEdit_ti8.text()
        i_tn8 = self.lineEdit_tn8.text()
        i_vac = self.textEdit_vac.toPlainText()
        i_ev = self.textEdit_ev.toPlainText()
        i_edu = self.textEdit_edu.toPlainText()
        i_rep = self.textEdit_rep.toPlainText()
        i_ep_d = self.lineEdit_ep_d.text()
        i_ep_n = self.lineEdit_ep_n.text()

        #---- 데이터 삽입


        data = (
            i_x1, i_x2, i_x3, i_x5, i_x10, i_r6, i_rs, i_re, i_a9, i_ak,    #1
            i_ah, i_od, i_on, i_pd, i_ed, i_xn, i_pn, i_en, i_xm, i_so,    #2
            i_sm, i_hc, i_hb, i_hm, i_cd, i_cn, i_md, i_mn, i_x1_p, i_x2_p,    #3
            i_x3_p, i_x5_p, i_x10_p, i_r6_p, i_rs_p, i_re_p, i_a9_p, i_ak_p, i_ah_p, i_od_p, #4
            i_re_p, i_a9_p, i_ak_p, i_ah_p, i_on, i_pd, i_ed, i_xn, i_pn, i_en, #5
            i_xm, i_so, i_sm, i_hc, i_hb, i_hm, i_cd, i_cn, i_md, i_mn, #6
            i_x1_p, i_x2_p, i_x3_p, i_x5_p, i_x10_p, i_r6_p, i_rs_p, i_re_p, i_a9_p, i_ak_p, #7
            i_ah_p, i_od_p, i_on_p, i_pd_p, i_ed_p, i_xn_p, i_pn_p, i_en_p, i_xm_p, i_so_p, #8
            i_he_p, i_ct_p, i_mr_p, i_x1_m, i_x2_m, i_x3_m, i_x5_m, i_x10_m, i_r6_m, i_rs_m, #9
            i_re_m, i_a9_m, i_ak_m, i_ah_m, i_or_m, i_pd_m, i_ed_m, i_xn_m, i_pn_m, i_en_m, #10
            i_a9_m, i_ak_m, i_ah_m, i_or_m, i_pd_m, i_ed_m, i_xn_m, i_pn_m, i_en_m, i_xm_m, #11
            i_so_m, i_he_m, i_ct_m, i_mr_m, i_x1_n, i_x2_n, i_x3_n, i_x5_n, i_x10_n, i_r6_n, #12
            i_rs_n, i_re_n, i_a9_n, i_ak_n, i_ah_n, i_or_n, i_pd_n, i_ed_n, i_xn_n, i_pn_n, #13
            i_pn_n, i_en_n, i_xm_n, i_so_n, i_he_n, i_ct_n, i_mr_n, i_x_d_n, i_x_e_n, i_x_n_n, #14
            i_e_d_n, i_e_e_n, i_e_n_n, i_c_d_n, i_c_e_n, i_c_n_n, i_m_d_n, i_m_e_n, i_m_n_n, i_p1,  #15
            i_ts1, i_te1, i_ti1, i_tn1, i_p2, i_ts2, i_te2, i_ti2, i_tn2, i_p3, #16
            i_ts3, i_te3, i_ti3, i_tn3, i_p4, i_ts4, i_te4, i_ti4, i_tn4, i_p5, #17
            i_ts5, i_te5, i_ti5, i_tn5, i_p6, i_ts6, i_te6, i_ti6, i_tn6, i_p7, #18
            i_ts7, i_te7, i_ti7, i_tn7, i_p8, i_ts8, i_te8, i_ti8, i_tn8, i_vac,  #19
            i_ev, i_edu, i_rep, i_dateEdit_report, i_team_leader, i_exaggeration , i_ep_d, i_ep_n #20           
        )
        try:
            conn = pymysql.connect(host="211.186.169.70", user="root", password="1024", db="Daily_report", charset="utf8")
            curs = conn.cursor()
            sql = """
                INSERT INTO report (
                    x1, x2, x3, x5, x10, r6, rs, re, a9, ak,                        
                    ah, od, on, pd, ed, xn, pn, en, xm, so,                         
                    sm, hc, hb, hm, cd, cn, md, mn, x1_p, x2_p,                     
                    x3_p, x5_p, x10_p, r6_p, rs_p, re_p, a9_p, ak_p, ah_p, od_p,    
                    re_p, a9_p, ak_p, ah_p, on, pd, ed, xn, pn, en,                 
                    xm, so, sm, hc, hb, hm, cd, cn, md, mn,                        
                    x1_p, x2_p, x3_p, x5_p, x10_p, r6_p, rs_p, re_p, a9_p, ak_p,   
                    ah_p, od_p, on_p, pd_p, ed_p, xn_p, pn_p, en_p, xm_p, so_p,    
                    he_p, ct_p, mr_p, x1_m, x2_m, x3_m, x5_m, x10m, r6_m, rs_m,    
                    re_m, a9_m, ak_m, ah_m, or_m, pd_m, ed_m, xn_m, pn_m, en_m,     
                    a9_m, ak_m, ah_m, or_m, pd_m, ed_m, xn_m, pn_m, en_m, xm_m,     
                    so_m, he_m, ct_m, mr_m, x1_n, x2_n, x3_n, x5_n, x10n, r6_n,     
                    rs_n, re_n, a9_n, ak_n, ah_n, or_n, pd_n, ed_n, xn_n, pn_n,     
                    en_n, xm_n, so_n, he_n, ct_n, mr_n, x_d_n, x_e_n, x_n_n, e_d_n, 
                    e_e_n, e_n_n, c_d_n, c_e_n, c_n_n, m_d_n, m_e_n, m_n_n, p1,     
                    ts1, te1, ti1, tn1, p2, ts2, te2, ti2, tn2, p3,                 
                    ts3, te3, ti3, tn3, p4, ts4, te4, ti4, tn4, p5,                 
                    ts5, te5, ti5, tn5, p6, ts6, te6, ti6, tn6, p7,                 
                    ts7, te7, ti7, tn7, p8, ts8, te8, ti8, tn8, vac,                
                    ev, edu, rep, report_date, team_leader, exaggeration, ep_d, ep_n         
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,   #1
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, #2
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s  #3
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s  #4
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s  #5
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s  #6
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s  #7
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s  #8
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s  #9
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s  #10
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s  #11
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s  #12
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s  #13
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s  #14
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s  #15
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s  #16
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s  #17
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s  #18
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s  #19
                            %s, %s, %s, %s, %s, %s, %s, %s          #20

                )
            """
            curs.execute(sql, data)
            conn.commit()
        except pymysql.MySQLError as e:
            QMessageBox.critical(self, "데이터베이스 오류", f"데이터 삽입 중 오류가 발생했습니다: {e}")
        finally:
            conn.close()

        # 재료 데이터 삽입 로직
        QMessageBox.about(self, "재료", "재료 데이터가 입력되었습니다.")
    

    def DataShow(self):
        # 모래시계 커서로 변경
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        QApplication.processEvents()  # UI 업데이트


        # # "잠시 기다려 주세요" 메시지 표시
        # loading_message = QMessageBox(self)
        # loading_message.setWindowTitle("로딩 중")
        # loading_message.setText("잠시 기다려 주세요...")
        # loading_message.setStandardButtons(QMessageBox.StandardButton.NoButton)
        # loading_message.setModal(True)
        # loading_message.show()
        # QApplication.processEvents()  # UI 업데이트

        #--- 데이터 불러오기 진행화면
        # self.progressBar.setValue(30)

        #---- 기존 데이터 출력
        self.dateVar = self.dateEdit_report.date()
        i_dateEdit_report = self.dateVar.toString('yyyy-MM-dd')

        #---- i_dateEdit_report 키에 맞게 데이터출력
        conn = pymysql.connect(host="211.186.169.70", user="root", password="1024", db="Daily_report", charset="utf8")
        curs = conn.cursor()
        sql = """
            SELECT * FROM report WHERE report_date = %s
        """
        curs.execute(sql, i_dateEdit_report)
        data = curs.fetchall()
        self.lineEdit_x1.setText(data[0][4])
        self.lineEdit_x2.setText(data[0][5])
        self.lineEdit_x3.setText(data[0][6])
        self.lineEdit_x5.setText(data[0][7])
        self.lineEdit_x10.setText(data[0][8])
        self.lineEdit_r6.setText(data[0][9])
        self.lineEdit_rs.setText(data[0][10])
        self.lineEdit_re.setText(data[0][11])
        self.lineEdit_a9.setText(data[0][12])
        self.lineEdit_ak.setText(data[0][13])
        self.lineEdit_ah.setText(data[0][14])
        self.lineEdit_od.setText(data[0][15])
        self.lineEdit_on.setText(data[0][16])
        self.lineEdit_pd.setText(data[0][17])
        self.lineEdit_ed.setText(data[0][18])
        self.lineEdit_xn.setText(data[0][19])
        self.lineEdit_pn.setText(data[0][20])
        self.lineEdit_en.setText(data[0][21])
        self.lineEdit_xm.setText(data[0][22])
        self.lineEdit_so.setText(data[0][23])
        self.lineEdit_sm.setText(data[0][24])
        self.lineEdit_hc.setText(data[0][25])
        self.lineEdit_hb.setText(data[0][26])
        self.lineEdit_hm.setText(data[0][27])
        self.lineEdit_cd.setText(data[0][28])
        self.lineEdit_cn.setText(data[0][29])
        self.lineEdit_md.setText(data[0][30])
        self.lineEdit_mn.setText(data[0][31])
        self.lineEdit_x1_p.setText(data[0][32])
        self.lineEdit_x2_p.setText(data[0][33])
        self.lineEdit_x3_p.setText(data[0][34])
        self.lineEdit_x5_p.setText(data[0][35])
        self.lineEdit_x10_p.setText(data[0][36])
        self.lineEdit_r6_p.setText(data[0][37])
        self.lineEdit_rs_p.setText(data[0][38])
        self.lineEdit_re_p.setText(data[0][39])
        self.lineEdit_a9_p.setText(data[0][40])
        self.lineEdit_ak_p.setText(data[0][41])
        self.lineEdit_ah_p.setText(data[0][42])
        self.lineEdit_od_p.setText(data[0][43])
        self.lineEdit_on_p.setText(data[0][44])
        self.lineEdit_pd_p.setText(data[0][45])
        self.lineEdit_pn_p.setText(data[0][46])
        self.lineEdit_ed_p.setText(data[0][47])
        self.lineEdit_xn_p.setText(data[0][48])
        self.lineEdit_en_p.setText(data[0][49])
        self.lineEdit_xm_p.setText(data[0][50])
        self.lineEdit_so_p.setText(data[0][51])
        self.lineEdit_he_p.setText(data[0][52])
        self.lineEdit_ct_p.setText(data[0][54])
        self.lineEdit_mr_p.setText(data[0][55])
        self.lineEdit_x1_m.setText(data[0][56])
        self.lineEdit_x2_m.setText(data[0][57])
        self.lineEdit_x3_m.setText(data[0][58])
        self.lineEdit_x5_m.setText(data[0][59])
        self.lineEdit_x10_m.setText(data[0][60])
        self.lineEdit_r6_m.setText(data[0][61])
        self.lineEdit_rs_m.setText(data[0][62])
        self.lineEdit_re_m.setText(data[0][63])
        self.lineEdit_a9_m.setText(data[0][64])
        self.lineEdit_ak_m.setText(data[0][65])
        self.lineEdit_ah_m.setText(data[0][66])
        self.lineEdit_or_m.setText(data[0][67])
        self.lineEdit_pd_m.setText(data[0][68])
        self.lineEdit_ed_m.setText(data[0][69])
        self.lineEdit_xn_m.setText(data[0][70])
        self.lineEdit_pn_m.setText(data[0][71])
        self.lineEdit_en_m.setText(data[0][72])
        self.lineEdit_xm_m.setText(data[0][73])
        self.lineEdit_so_m.setText(data[0][74])
        self.lineEdit_he_m.setText(data[0][75])
        self.lineEdit_ct_m.setText(data[0][76])
        self.lineEdit_mr_m.setText(data[0][77])
        self.lineEdit_x1_n.setText(data[0][78])
        self.lineEdit_x2_n.setText(data[0][79])
        self.lineEdit_x3_n.setText(data[0][80])
        self.lineEdit_x5_n.setText(data[0][81])
        self.lineEdit_x10_n.setText(data[0][82])
        self.lineEdit_r6_n.setText(data[0][83])
        self.lineEdit_rs_n.setText(data[0][84])
        self.lineEdit_re_n.setText(data[0][85])
        self.lineEdit_a9_n.setText(data[0][86])
        self.lineEdit_ak_n.setText(data[0][87])
        self.lineEdit_ah_n.setText(data[0][88])
        self.lineEdit_or_n.setText(data[0][89])
        self.lineEdit_pd_n.setText(data[0][90])
        self.lineEdit_ed_n.setText(data[0][91])
        self.lineEdit_xn_n.setText(data[0][92])
        self.lineEdit_pn_n.setText(data[0][93])
        self.lineEdit_en_n.setText(data[0][94])
        self.lineEdit_xm_n.setText(data[0][95])
        self.lineEdit_so_n.setText(data[0][96])
        self.lineEdit_he_n.setText(data[0][97])
        self.lineEdit_ct_n.setText(data[0][98])
        self.lineEdit_mr_n.setText(data[0][99])
        self.lineEdit_x_d_n.setText(data[0][100])
        self.lineEdit_x_e_n.setText(data[0][101])
        self.lineEdit_x_n_n.setText(data[0][102])
        self.lineEdit_e_d_n.setText(data[0][103])
        self.lineEdit_e_e_n.setText(data[0][104])
        self.lineEdit_e_n_n.setText(data[0][105])
        self.lineEdit_c_d_n.setText(data[0][106])
        self.lineEdit_c_e_n.setText(data[0][107])
        self.lineEdit_c_n_n.setText(data[0][108])
        self.lineEdit_m_d_n.setText(data[0][109])
        self.lineEdit_m_e_n.setText(data[0][110])
        self.lineEdit_m_n_n.setText(data[0][111])
        self.lineEdit_m2_n.setText(data[0][112])
        self.lineEdit_p1.setText(data[0][113])
        self.lineEdit_ts1.setText(data[0][114])
        self.lineEdit_te1.setText(data[0][115])
        self.lineEdit_ti1.setText(data[0][116])
        self.lineEdit_tn1.setText(data[0][117])
        self.lineEdit_p2.setText(data[0][118])
        self.lineEdit_ts2.setText(data[0][119])
        self.lineEdit_te2.setText(data[0][120])
        self.lineEdit_ti2.setText(data[0][121])
        self.lineEdit_tn2.setText(data[0][122])
        self.lineEdit_p3.setText(data[0][123])
        self.lineEdit_ts3.setText(data[0][124])
        self.lineEdit_te3.setText(data[0][125])
        self.lineEdit_ti3.setText(data[0][126])
        self.lineEdit_tn3.setText(data[0][127])
        self.lineEdit_p4.setText(data[0][128])
        self.lineEdit_ts4.setText(data[0][129])
        self.lineEdit_te4.setText(data[0][130])
        self.lineEdit_ti4.setText(data[0][131])
        self.lineEdit_tn4.setText(data[0][132])
        self.lineEdit_p5.setText(data[0][133])
        self.lineEdit_ts5.setText(data[0][134])
        self.lineEdit_te5.setText(data[0][135])
        self.lineEdit_ti5.setText(data[0][136])
        self.lineEdit_tn5.setText(data[0][137])
        self.lineEdit_p6.setText(data[0][138])
        self.lineEdit_ts6.setText(data[0][139])
        self.lineEdit_te6.setText(data[0][140])
        self.lineEdit_ti6.setText(data[0][141])
        self.lineEdit_tn6.setText(data[0][142])
        self.lineEdit_p7.setText(data[0][143])
        self.lineEdit_ts7.setText(data[0][144])
        self.lineEdit_te7.setText(data[0][145])
        self.lineEdit_ti7.setText(data[0][146])
        self.lineEdit_tn7.setText(data[0][147])
        self.lineEdit_p8.setText(data[0][148])
        self.lineEdit_ts8.setText(data[0][149])
        self.lineEdit_te8.setText(data[0][150])
        self.lineEdit_ti8.setText(data[0][151])
        self.lineEdit_tn8.setText(data[0][152])

        self.textEdit_vac.setText(data[0][153])
        self.textEdit_ev.setText(data[0][154])
        self.textEdit_edu.setText(data[0][155])
        self.textEdit_rep.setText(data[0][156])

        self.lineEdit_i9.setText(data[0][157])
        self.lineEdit_ik.setText(data[0][158])
        self.lineEdit_ih.setText(data[0][159])
        self.lineEdit_ep_d.setText(data[0][160])
        self.lineEdit_ep_n.setText(data[0][161])

        #--- 모든 데이터 오른쪽 정렬
        line_edits = [
            self.lineEdit_x1, self.lineEdit_x2, self.lineEdit_x3, self.lineEdit_x5, self.lineEdit_x10,
            self.lineEdit_r6, self.lineEdit_rs, self.lineEdit_re, self.lineEdit_a9, self.lineEdit_ak,
            self.lineEdit_ah, self.lineEdit_od, self.lineEdit_on, self.lineEdit_pd, self.lineEdit_ed,
            self.lineEdit_xn, self.lineEdit_pn, self.lineEdit_en, self.lineEdit_xm, self.lineEdit_so,
            self.lineEdit_sm, self.lineEdit_hc, self.lineEdit_hb, self.lineEdit_hm, self.lineEdit_cd,
            self.lineEdit_cn, self.lineEdit_md, self.lineEdit_mn, self.lineEdit_x1_p, self.lineEdit_x2_p,
            self.lineEdit_x3_p, self.lineEdit_x5_p, self.lineEdit_x10_p, self.lineEdit_r6_p, self.lineEdit_rs_p,
            self.lineEdit_re_p, self.lineEdit_a9_p, self.lineEdit_ak_p, self.lineEdit_ah_p, self.lineEdit_od_p,
            self.lineEdit_on_p, self.lineEdit_pd_p, self.lineEdit_ed_p, self.lineEdit_xn_p, self.lineEdit_pn_p,
            self.lineEdit_en_p, self.lineEdit_xm_p, self.lineEdit_so_p, self.lineEdit_he_p, self.lineEdit_ct_p,
            self.lineEdit_mr_p, self.lineEdit_x1_m, self.lineEdit_x2_m, self.lineEdit_x3_m, self.lineEdit_x5_m,
            self.lineEdit_x10_m, self.lineEdit_r6_m, self.lineEdit_rs_m, self.lineEdit_re_m, self.lineEdit_a9_m,
            self.lineEdit_ak_m, self.lineEdit_ah_m, self.lineEdit_or_m, self.lineEdit_pd_m, self.lineEdit_ed_m,
            self.lineEdit_xn_m, self.lineEdit_pn_m, self.lineEdit_en_m, self.lineEdit_xm_m, self.lineEdit_so_m,
            self.lineEdit_he_m, self.lineEdit_ct_m, self.lineEdit_mr_m, self.lineEdit_x1_n, self.lineEdit_x2_n,
            self.lineEdit_x3_n, self.lineEdit_x5_n, self.lineEdit_x10_n, self.lineEdit_r6_n, self.lineEdit_rs_n,
            self.lineEdit_re_n, self.lineEdit_a9_n, self.lineEdit_ak_n, self.lineEdit_ah_n, self.lineEdit_or_n,
            self.lineEdit_pd_n, self.lineEdit_ed_n, self.lineEdit_xn_n, self.lineEdit_pn_n, self.lineEdit_en_n,
            self.lineEdit_xm_n, self.lineEdit_so_n, self.lineEdit_he_n, self.lineEdit_ct_n, self.lineEdit_mr_n,
            self.lineEdit_x_d_n, self.lineEdit_x_e_n, self.lineEdit_x_n_n, self.lineEdit_e_d_n, self.lineEdit_e_e_n,
            self.lineEdit_e_n_n, self.lineEdit_c_d_n, self.lineEdit_c_e_n, self.lineEdit_c_n_n, self.lineEdit_m_d_n,
            self.lineEdit_m_e_n, self.lineEdit_m_n_n, self.lineEdit_m2_n, self.lineEdit_p1, self.lineEdit_ts1,
            self.lineEdit_te1, self.lineEdit_ti1, self.lineEdit_tn1, self.lineEdit_p2, self.lineEdit_ts2,
            self.lineEdit_te2, self.lineEdit_ti2, self.lineEdit_tn2, self.lineEdit_p3, self.lineEdit_ts3,
            self.lineEdit_te3, self.lineEdit_ti3, self.lineEdit_tn3, self.lineEdit_p4, self.lineEdit_ts4,
            self.lineEdit_te4, self.lineEdit_ti4, self.lineEdit_tn4, self.lineEdit_p5, self.lineEdit_ts5,
            self.lineEdit_te5, self.lineEdit_ti5, self.lineEdit_tn5, self.lineEdit_p6, self.lineEdit_ts6,
            self.lineEdit_te6, self.lineEdit_ti6, self.lineEdit_tn6, self.lineEdit_p7, self.lineEdit_ts7,
            self.lineEdit_te7, self.lineEdit_ti7, self.lineEdit_tn7, self.lineEdit_p8, self.lineEdit_ts8,
            self.lineEdit_te8, self.lineEdit_ti8, self.lineEdit_tn8,
            self.lineEdit_xt_d, self.lineEdit_xt_n, self.lineEdit_xt_d_p, self.lineEdit_xt_n_p,
            self.lineEdit_et_d, self.lineEdit_et_n, self.lineEdit_et_d_p, self.lineEdit_et_n_p,
            self.lineEdit_ot_d, self.lineEdit_ot_n, self.lineEdit_ot_d_p, self.lineEdit_ot_n_p,
            self.lineEdit_pt_d, self.lineEdit_pt_n, self.lineEdit_pt_d_p, self.lineEdit_pt_n_p,
            self.lineEdit_st_d, self.lineEdit_st_n, self.lineEdit_st_d_p, self.lineEdit_st_n_p,
            self.lineEdit_at_d, self.lineEdit_at_n, self.lineEdit_at_d_p, self.lineEdit_at_n_p,
            self.lineEdit_it_d, self.lineEdit_it_n, self.lineEdit_it_d_p, self.lineEdit_it_n_p,
            self.lineEdit_mt_d, self.lineEdit_mt_n, self.lineEdit_mt_d_p, self.lineEdit_mt_n_p,
            self.lineEdit_sot_d, self.lineEdit_sot_n, self.lineEdit_sot_d_p, self.lineEdit_sot_n_p,
            self.lineEdit_ht_d, self.lineEdit_ht_n, self.lineEdit_ht_d_p, self.lineEdit_ht_n_p,
            self.lineEdit_x_sub, self.lineEdit_x_sub_p,
            self.lineEdit_s_sub, self.lineEdit_s_sub_p,
            self.lineEdit_d_sub, self.lineEdit_d_sub_p,
            self.lineEdit_d_tot, self.lineEdit_d_tot_p,
            self.lineEdit_ep_d, self.lineEdit_ep_n
        ]

        for line_edit in line_edits:
            line_edit.setAlignment(Qt.AlignmentFlag.AlignRight)
        

        #--- 재료 합계
        i_x1 = data[0][4]
        i_x2 = data[0][5]
        i_x3 = data[0][6]
        i_x5 = data[0][7]
        i_x10 = data[0][8]
        i_xt_d = int(i_x1 or 0) + int(i_x2 or 0) + int(i_x3 or 0) + int(i_x5 or 0) + int(i_x10 or 0)
        self.lineEdit_xt_d.setText(str(i_xt_d))

        i_x1_p = data[0][32]
        i_x2_p = data[0][33]
        i_x3_p = data[0][34]
        i_x5_p = data[0][35]
        i_x10_p = data[0][36]
        i_xt_d_p = int(i_x1_p or 0) + int(i_x2_p or 0) + int(i_x3_p or 0) + int(i_x5_p or 0) + int(i_x10_p or 0)
        self.lineEdit_xt_d_p.setText(str(i_xt_d_p))

        i_xn = data[0][19]
        self.lineEdit_xt_n.setText(str(i_xn))

        i_xn_p = data[0][48]
        self.lineEdit_xt_n_p.setText(str(i_xn_p))

        i_ed = data[0][18]
        self.lineEdit_et_d.setText(str(i_ed))

        i_ed_p = data[0][47]
        self.lineEdit_et_d_p.setText(str(i_ed_p))

        i_en = data[0][21]
        self.lineEdit_et_n.setText(str(i_en))        
        i_en_p = data[0][49]
        self.lineEdit_et_n_p.setText(str(i_en_p))

        i_od = data[0][15]
        self.lineEdit_ot_d.setText(str(i_od))
        i_od_p = data[0][43]
        self.lineEdit_ot_d_p.setText(str(i_od_p))

        i_on = data[0][16]
        self.lineEdit_ot_n.setText(str(i_on))
        i_on_p = data[0][44]
        self.lineEdit_ot_n_p.setText(str(i_on_p))

        i_pd = data[0][17]
        self.lineEdit_pt_d.setText(str(i_pd))
        i_pd_p = data[0][45]
        self.lineEdit_pt_d_p.setText(str(i_pd_p))

        i_pn = data[0][20]
        self.lineEdit_pt_n.setText(str(i_pn))
        i_pn_p = data[0][46]
        self.lineEdit_pt_n_p.setText(str(i_pn_p))

        i_r6 = data[0][9]
        i_rs = data[0][10]
        i_re = data[0][11]
        i_st_d = int(i_r6 or 0) + int(i_rs or 0) + int(i_re or 0)
        self.lineEdit_st_d.setText(str(i_st_d))
        i_r6_p = data[0][37]
        i_rs_p = data[0][38]
        i_re_p = data[0][39]
        i_st_d_p = int(i_r6_p or 0) + int(i_rs_p or 0) + int(i_re_p or 0)
        self.lineEdit_st_d_p.setText(str(i_st_d_p))

        i_a9 = data[0][12]
        i_ak = data[0][13]
        i_ah = data[0][14]
        i_at_d = int(i_a9 or 0) + int(i_ak or 0) + int(i_ah or 0)
        self.lineEdit_at_d.setText(str(i_at_d))

        i_a9_p = data[0][40]
        i_ak_p = data[0][41]
        i_ah_p = data[0][42]
        i_at_d_p = int(i_a9_p or 0) + int(i_ak_p or 0) + int(i_ah_p or 0)   
        self.lineEdit_at_d_p.setText(str(i_at_d_p))

        i_i9 = data[0][157]
        i_ik = data[0][158]
        i_ih = data[0][159]
        i_it_d = int(i_i9 or 0) + int(i_ik or 0) + int(i_ih or 0)
        self.lineEdit_it_d.setText(str(i_it_d))

        i_xm = data[0][22]
        self.lineEdit_mt_d.setText(str(i_xm))
        i_xm_p = data[0][50]
        self.lineEdit_mt_d_p.setText(str(i_xm_p))

        i_so = data[0][23]
        i_sm = data[0][24]
        i_sot_d = int(i_so or 0) + int(i_sm or 0)
        self.lineEdit_sot_d.setText(str(i_sot_d))
        i_so_p = data[0][51]
        self.lineEdit_sot_d_p.setText(str(i_so_p))

        i_hc = data[0][25]
        i_hb = data[0][26]
        i_hm = data[0][27]
        i_ht_d = int(i_hc or 0) + int(i_hb or 0) + int(i_hm or 0)
        self.lineEdit_ht_d.setText(str(i_ht_d))        
        self.lineEdit_ht_d_p.setText(str(i_hc))

        i_x_sub = i_xt_d + int(i_xn or 0)+int(i_ed or 0)+int(i_en or 0)+int(i_od or 0)+int(i_on or 0)+int(i_pd or 0)+int(i_pn or 0)
        self.lineEdit_x_sub.setText(str(i_x_sub))

        i_x_sub_p = i_xt_d_p + int(i_xn_p or 0)+int(i_ed_p or 0)+int(i_en_p or 0)+int(i_od_p or 0)+int(i_on_p or 0)+int(i_pd_p or 0)+int(i_pn_p or 0)      
        self.lineEdit_x_sub_p.setText(str(i_x_sub_p))

        i_s_sub = i_st_d + i_at_d + i_it_d + int(i_xm or 0) + i_sot_d + i_ht_d
        self.lineEdit_s_sub.setText(str(i_s_sub))
        i_s_sub_p = i_st_d_p + i_at_d_p  + int(i_xm_p or 0) + int(i_so_p or 0) + int(i_hc or 0)
        self.lineEdit_s_sub_p.setText(str(i_s_sub_p))

        i_d_sub = i_x_sub + i_s_sub
        self.lineEdit_d_sub.setText(str(i_d_sub))
        i_d_sub_p = i_x_sub_p + i_s_sub_p
        self.lineEdit_d_sub_p.setText(str(i_d_sub_p))

        i_cd = data[0][28]
        i_cn = data[0][29]
        i_md = data[0][30]
        i_mn = data[0][31]
        i_d_tot = i_d_sub + int(i_cd or 0) + int(i_cn or 0) + int(i_md or 0) + int(i_mn or 0)
        self.lineEdit_d_tot.setText(str(i_d_tot))

        i_ct_p = data[0][54]
        i_mr_p = data[0][55]      
        i_d_tot_p = i_d_sub_p + int(i_ct_p or 0) + int(i_mr_p or 0)
        # self.lineEdit_d_tot_p.setText(str(i_d_tot_p))

        #--- i_d_sub, i_d_sub_p, i_d_tot, i_d_tot_p, i_x_sub, i_xt_d 값을 숫자 3자리마다 , 추가 후 lineEdit_d_tot_p에 넣기
        i_d_sub_str = str(i_d_sub)
        i_d_sub_str_comma = i_d_sub_str.replace(',', '')
        i_d_sub_int = int(i_d_sub_str_comma)
        i_d_sub_str_comma = f"{i_d_sub_int:,}"
        self.lineEdit_d_sub.setText(i_d_sub_str_comma)

        i_d_sub_p_str = str(i_d_sub_p)
        i_d_sub_p_str_comma = i_d_sub_p_str.replace(',', '')
        i_d_sub_p_int = int(i_d_sub_p_str_comma)
        i_d_sub_p_str_comma = f"{i_d_sub_p_int:,}"
        self.lineEdit_d_sub_p.setText(i_d_sub_p_str_comma)

        i_d_tot_str = str(i_d_tot)
        i_d_tot_str_comma = i_d_tot_str.replace(',', '')
        i_d_tot_int = int(i_d_tot_str_comma)
        i_d_tot_str_comma = f"{i_d_tot_int:,}"
        self.lineEdit_d_tot.setText(i_d_tot_str_comma)

        i_d_tot_p_str = str(i_d_tot_p)
        i_d_tot_p_str_comma = i_d_tot_p_str.replace(',', '')
        i_d_tot_p_int = int(i_d_tot_p_str_comma)
        i_d_tot_p_str_comma = f"{i_d_tot_p_int:,}"
        self.lineEdit_d_tot_p.setText(i_d_tot_p_str_comma)

        i_x_sub_str = str(i_x_sub)
        i_x_sub_str_comma = i_x_sub_str.replace(',', '')
        i_x_sub_int = int(i_x_sub_str_comma)
        i_x_sub_str_comma = f"{i_x_sub_int:,}"
        self.lineEdit_x_sub.setText(i_x_sub_str_comma)

        i_xt_d_str = str(i_xt_d)
        i_xt_d_str_comma = i_xt_d_str.replace(',', '')
        i_xt_d_int = int(i_xt_d_str_comma)
        i_xt_d_str_comma = f"{i_xt_d_int:,}"
        self.lineEdit_xt_d.setText(i_xt_d_str_comma)

        conn.commit()
        conn.close()

        # 모래시계 커서를 원래 커서로 복원
        QApplication.restoreOverrideCursor()
        
        # # "잠시 기다려 주세요" 메시지 숨기기
        # loading_message.hide()


    def EditClear(self):
        self.dateEdit_report.setEnabled(True)

        # #----- 날짜 오늘 날짜로
        # today = QDate.currentDate() # QDate.currentDate(): 현재 날짜를 반환
        # self.dateEdit_report.setDate(today) # setDate(): 'QDateEdit' 위젯에 날짜를 설정
        # #---- checkBox (Default unchecked)
        self.checkBox_team.setChecked(False) 
        self.checkBox_exaggeration.setChecked(False) 

        self.lineEdit_xt_d.clear()
        self.lineEdit_xt_n.clear()
        self.lineEdit_xt_d_p.clear()
        self.lineEdit_xt_n_p.clear()

        self.lineEdit_et_d.clear()
        self.lineEdit_et_n.clear()
        self.lineEdit_et_d_p.clear()
        self.lineEdit_et_n_p.clear()

        self.lineEdit_ot_d.clear()
        self.lineEdit_ot_n.clear()
        self.lineEdit_ot_d_p.clear()
        self.lineEdit_ot_n_p.clear()

        self.lineEdit_pt_d.clear()
        self.lineEdit_pt_n.clear()
        self.lineEdit_pt_d_p.clear()
        self.lineEdit_pt_n_p.clear()

        self.lineEdit_st_d.clear()
        self.lineEdit_st_n.clear()
        self.lineEdit_st_d_p.clear()
        self.lineEdit_st_n_p.clear()

        self.lineEdit_at_d.clear()
        self.lineEdit_at_n.clear()
        self.lineEdit_at_d_p.clear()
        self.lineEdit_at_n_p.clear()

        self.lineEdit_it_d.clear()
        self.lineEdit_it_n.clear()
        self.lineEdit_it_d_p.clear()
        self.lineEdit_it_n_p.clear()

        self.lineEdit_mt_d.clear()
        self.lineEdit_mt_n.clear()
        self.lineEdit_mt_d_p.clear()
        self.lineEdit_mt_n_p.clear()

        self.lineEdit_sot_d.clear()
        self.lineEdit_sot_n.clear()
        self.lineEdit_sot_d_p.clear()
        self.lineEdit_sot_n_p.clear()

        self.lineEdit_ht_d.clear()
        self.lineEdit_ht_n.clear()
        self.lineEdit_ht_d_p.clear()
        self.lineEdit_ht_n_p.clear()

        self.lineEdit_x_sub.clear()
        self.lineEdit_x_sub_p.clear()

        self.lineEdit_s_sub.clear()
        self.lineEdit_s_sub_p.clear()

        self.lineEdit_d_sub.clear()
        self.lineEdit_d_sub_p.clear()

        self.lineEdit_d_tot.clear()
        self.lineEdit_d_tot_p.clear()

        #---- lineEdit clear
        self.lineEdit_x1.clear()
        self.lineEdit_x2.clear()
        self.lineEdit_x3.clear()
        self.lineEdit_x5.clear()
        self.lineEdit_x10.clear()
        self.lineEdit_r6.clear()
        self.lineEdit_rs.clear()
        self.lineEdit_re.clear()
        self.lineEdit_a9.clear()
        self.lineEdit_ak.clear()
        self.lineEdit_ah.clear()
        self.lineEdit_i9.clear()    
        self.lineEdit_ik.clear()
        self.lineEdit_ih.clear()
        self.lineEdit_od.clear()
        self.lineEdit_on.clear()
        self.lineEdit_pd.clear()
        self.lineEdit_ed.clear()
        self.lineEdit_xn.clear()
        self.lineEdit_pn.clear()
        self.lineEdit_en.clear()
        self.lineEdit_xm.clear()
        self.lineEdit_so.clear()
        self.lineEdit_sm.clear()
        self.lineEdit_hc.clear()
        self.lineEdit_hb.clear()
        self.lineEdit_hm.clear()
        self.lineEdit_cd.clear()
        self.lineEdit_cn.clear()
        self.lineEdit_md.clear()
        self.lineEdit_mn.clear()
        self.lineEdit_x1_p.clear()
        self.lineEdit_x2_p.clear()
        self.lineEdit_x3_p.clear()
        self.lineEdit_x5_p.clear()
        self.lineEdit_x10_p.clear()
        self.lineEdit_r6_p.clear()
        self.lineEdit_rs_p.clear()
        self.lineEdit_re_p.clear()
        self.lineEdit_a9_p.clear()
        self.lineEdit_ak_p.clear()
        self.lineEdit_ah_p.clear()
        self.lineEdit_od_p.clear()
        self.lineEdit_on_p.clear()
        self.lineEdit_pd_p.clear()
        self.lineEdit_ed_p.clear()
        self.lineEdit_xn_p.clear()
        self.lineEdit_pn_p.clear()
        self.lineEdit_en_p.clear()
        self.lineEdit_xm_p.clear()
        self.lineEdit_so_p.clear()
        self.lineEdit_he_p.clear()
        self.lineEdit_ct_p.clear()
        self.lineEdit_mr_p.clear()
        self.lineEdit_x1_m.clear()
        self.lineEdit_x2_m.clear()
        self.lineEdit_x3_m.clear()
        self.lineEdit_x5_m.clear()
        self.lineEdit_x10_m.clear()
        self.lineEdit_r6_m.clear()
        self.lineEdit_rs_m.clear()
        self.lineEdit_re_m.clear()
        self.lineEdit_a9_m.clear()
        self.lineEdit_ak_m.clear()
        self.lineEdit_ah_m.clear()
        self.lineEdit_or_m.clear()
        self.lineEdit_pd_m.clear()
        self.lineEdit_ed_m.clear()
        self.lineEdit_xn_m.clear()
        self.lineEdit_pn_m.clear()
        self.lineEdit_en_m.clear()
        self.lineEdit_xm_m.clear()
        self.lineEdit_so_m.clear()
        self.lineEdit_he_m.clear()
        self.lineEdit_ct_m.clear()
        self.lineEdit_mr_m.clear()        

        self.lineEdit_x1_n.clear()
        self.lineEdit_x2_n.clear()
        self.lineEdit_x3_n.clear()
        self.lineEdit_x5_n.clear()
        self.lineEdit_x10_n.clear()
        self.lineEdit_r6_n.clear()
        self.lineEdit_rs_n.clear()
        self.lineEdit_re_n.clear()
        self.lineEdit_a9_n.clear()
        self.lineEdit_ak_n.clear()
        self.lineEdit_ah_n.clear()
        self.lineEdit_or_n.clear()
        self.lineEdit_pd_n.clear()
        self.lineEdit_ed_n.clear()
        self.lineEdit_xn_n.clear()
        self.lineEdit_pn_n.clear()
        self.lineEdit_en_n.clear()
        self.lineEdit_xm_n.clear()
        self.lineEdit_so_n.clear()
        self.lineEdit_he_n.clear()
        self.lineEdit_ct_n.clear()
        self.lineEdit_mr_n.clear()
        self.lineEdit_x_d_n.clear()
        self.lineEdit_x_e_n.clear()
        self.lineEdit_x_n_n.clear()
        self.lineEdit_e_d_n.clear()
        self.lineEdit_e_e_n.clear()
        self.lineEdit_e_n_n.clear()
        self.lineEdit_c_d_n.clear()
        self.lineEdit_c_e_n.clear()
        self.lineEdit_c_n_n.clear()
        self.lineEdit_m_d_n.clear()
        self.lineEdit_m_e_n.clear()
        self.lineEdit_m_n_n.clear()
        self.lineEdit_m2_n.clear()
        self.lineEdit_p1.clear()

        self.lineEdit_ts1.clear()
        self.lineEdit_te1.clear()
        self.lineEdit_ti1.clear()

        self.lineEdit_tn1.clear()
        self.lineEdit_p2.clear()

        self.lineEdit_ts2.clear()
        self.lineEdit_te2.clear()
        self.lineEdit_ti2.clear()

        self.lineEdit_tn2.clear()
        self.lineEdit_p3.clear()

        self.lineEdit_ts3.clear()
        self.lineEdit_te3.clear()
        self.lineEdit_ti3.clear()

        self.lineEdit_tn3.clear()
        self.lineEdit_p4.clear()

        self.lineEdit_ts4.clear()
        self.lineEdit_te4.clear()
        self.lineEdit_ti4.clear()

        self.lineEdit_tn4.clear()
        self.lineEdit_p5.clear()

        self.lineEdit_ts5.clear()
        self.lineEdit_te5.clear()
        self.lineEdit_ti5.clear()

        self.lineEdit_tn5.clear()
        self.lineEdit_p6.clear()

        self.lineEdit_ts6.clear()
        self.lineEdit_te6.clear()
        self.lineEdit_ti6.clear()

        self.lineEdit_tn6.clear()
        self.lineEdit_p7.clear()

        self.lineEdit_ts7.clear()
        self.lineEdit_te7.clear()
        self.lineEdit_ti7.clear()

        self.lineEdit_tn7.clear()
        self.lineEdit_p8.clear()

        self.lineEdit_ts8.clear()
        self.lineEdit_te8.clear()
        self.lineEdit_ti8.clear()

        self.lineEdit_tn8.clear()
        self.textEdit_vac.clear()
        self.textEdit_ev.clear()
        self.textEdit_edu.clear()
        self.textEdit_rep.clear()
        self.lineEdit_ep_d.clear()
        self.lineEdit_ep_n.clear()
    
    def ProgramQuit(self):
        self.close()

if __name__ == "__main__":
    # DPI 인식 설정
    try:
        ctypes.windll.shcore.SetProcessDpiAwarenessContext(-4)  # DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2
    except AttributeError:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)  # PROCESS_PER_MONITOR_DPI_AWARE
    app = QApplication(sys.argv)

    myWindow = MainWindow()
    myWindow.show()
    sys.exit(app.exec())

