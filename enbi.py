import os
from datetime import datetime
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox

is_alert_running = False  # 카운트다운 진행 여부 추적
time_input_label = None

# UI를 어둡게 하는것
ctk.set_appearance_mode("dark") 

def on_ok_button_click(alert_window):
    global is_alert_running
    alert_window.destroy()  # 알림 창 닫기
    is_alert_running = False  # 상태 초기화
    start_alerts()  # 다시 시작
# 알림을 띄우는 함수
def show_toast():
    global is_alert_running
    # 알림 창 생성
    alert_window = tk.Toplevel(root)
    alert_window.title("비상!")
    alert_window.geometry("250x150")
    alert_window.attributes('-topmost', True)  # 항상 맨 위에 위치하도록 설정

    # 아이콘 설정
    icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "date3.ico")
    alert_window.iconbitmap(icon_path)  # date3.ico 아이콘 사용

    # 알림 창의 배경색을 root와 동일하게 설정
    alert_window.config(bg=root.cget('bg'))

    # 알림 텍스트 레이블
    label = ctk.CTkLabel(alert_window, text="몸을 풀어야된당 삐", font=("Roboto", 18,"bold"), text_color="white", bg_color=root.cget('bg'))
    label.pack(pady=20)

    # 확인 버튼을 root의 기본 색상으로 설정
    ok_button = tk.Button(alert_window, text="확인", command=lambda: on_ok_button_click(alert_window), width=12, height=2, 
                          bg=root.cget('bg'), fg='blue', font=("Arial", 12, "bold"))
    ok_button.pack(pady=20)


# 카운트다운 함수 (분:초 형식)
def countdown(remaining):
    global is_alert_running

    if remaining >= 0:
        minutes = remaining // 60
        seconds = remaining % 60
        countdown_label.configure(text=f"은비 허리 부서지기까지.. {minutes}분 {seconds}초")
        root.after(1000, countdown, remaining - 1)  # 1초 후 재실행
    else:
        show_toast()  # 카운트다운 끝난 후 알림

def start_alerts():
    global is_alert_running
    global time_input_label, time_input
    if not is_alert_running:  # 카운트다운이 진행 중이지 않을 때만 실행
        try:
            # 사용자가 입력한 시간(분)을 초로 변환
            user_input_time = int(time_input.get()) * 60  # 분을 초로 변환
            next_alert_label.pack_forget()  # "대기 중" 레이블 숨기기
            is_alert_running = True  # 카운트다운 시작 상태로 설정
            countdown(user_input_time)  # 카운트다운 시작
            time_input.pack_forget()  # 시간 입력 필드 숨기기
            time_input_label.pack_forget()  # 시간 입력 레이블 숨기기
        except ValueError:
            messagebox.showerror("입력 오류", "올바른 시간을 입력해주세요.")  # 입력값이 숫자가 아닌 경우 오류 메시지
    else:
        messagebox.showinfo("알림", "이미 카운트다운이 실행 중입니다.")  # 카운트다운이 진행 중일 때 경고

# UI 실행 함수
def start_gui():
    global root, next_alert_label, countdown_label, time_input, time_input_label
    root = ctk.CTk()
    root.title("은비 허리 지키미")
    
    # 아이콘 설정 (exe에서도 동작하도록 경로 확인)
    icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "date3.ico")
    if os.path.exists(icon_path):
        root.iconbitmap(icon_path)

    # 현재 시간 레이블
    time_label = ctk.CTkLabel(root, text="", font=("Roboto", 14))
    time_label.pack(pady=10)

    # 다음 스트레칭까지 남은 시간 레이블
    next_alert_label = ctk.CTkLabel(root, text="다음 스트레칭까지: 대기 중", font=("Roboto", 14))
    next_alert_label.pack(pady=10)

    # 초 단위 카운트다운 레이블
    countdown_label = ctk.CTkLabel(root, text="", font=("Roboto", 14))
    countdown_label.pack(pady=10)

    # 시간 입력 필드 (분 단위로 입력 받기)
    time_input_label = ctk.CTkLabel(root, text="스트레칭 시간을 분 단위로 입력하세요:", font=("Roboto", 12))
    time_input_label.pack(pady=10)

    time_input = ctk.CTkEntry(root, font=("Roboto", 14))
    time_input.pack(pady=10)

    # 현재 시간을 1초마다 갱신하는 함수
    def update_time():
        now = datetime.now()
        time_label.configure(text=f"현재 시간: {now.strftime('%Y-%m-%d %H:%M:%S')}")
        root.after(1000, update_time)

    # 시작 버튼
    start_button = ctk.CTkButton(root, text="시작", command=start_alerts, width=200, height=40)
    start_button.pack(side="left", padx=10, pady=10)

    # 종료 버튼
    exit_button = ctk.CTkButton(root, text="종료", command=root.quit, width=200, height=40)
    exit_button.pack(side="left", padx=10, pady=10)

    root.after(1000, update_time)  # 1초마다 시간 업데이트
    root.mainloop()

if __name__ == "__main__":
    start_gui()
