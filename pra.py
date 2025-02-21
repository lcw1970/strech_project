import os
from datetime import datetime
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox

is_alert_running = False  # 카운트다운 진행 여부 추적
after_id = None  # after() 호출의 ID를 저장할 변수

# 알림을 띄우는 함수
def show_toast():
    global is_alert_running
    messagebox.showinfo("알림!", "스트레칭 해")
    is_alert_running = False  # 알림 후 카운트다운 상태 변경
    start_alerts()  # 다시 카운트다운 시작

# 카운트다운 함수 (분:초 형식)
def countdown(remaining):
    global after_id

    if remaining >= 0:
        minutes = remaining // 60
        seconds = remaining % 60
        countdown_label.configure(text=f"다음 스트레칭까지: {minutes}분 {seconds}초")
        after_id = root.after(1000, countdown, remaining - 1)  # 1초 후 재실행
    else:
        show_toast()  # 카운트다운 끝난 후 알림

def start_alerts():
    global is_alert_running

    if not is_alert_running:  # 카운트다운이 진행 중이지 않을 때만 실행
        try:
            # 사용자가 입력한 시간(분)을 초로 변환
            user_input_time = int(time_input.get()) * 60  # 분을 초로 변환
            next_alert_label.pack_forget()  # "대기 중" 레이블 숨기기
            is_alert_running = True  # 카운트다운 시작 상태로 설정
            countdown(user_input_time)  # 카운트다운 시작
        except ValueError:
            messagebox.showerror("입력 오류", "올바른 시간을 입력해주세요.")  # 입력값이 숫자가 아닌 경우 오류 메시지
    else:
        messagebox.showinfo("알림", "이미 카운트다운이 실행 중입니다.")  # 카운트다운이 진행 중일 때 경고

def reset_timer():
    global is_alert_running, after_id

    # 카운트다운 진행 중이면 중단
    if after_id is not None:
        root.after_cancel(after_id)  # after() 호출 취소

    root.quit()
    start_gui()

    
    


# UI 실행 함수
def start_gui():
    global root, next_alert_label, countdown_label, time_input
    root = ctk.CTk()
    root.title("스트레칭 알리미")
    
    # 아이콘 설정 (exe에서도 동작하도록 경로 확인)
    icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "date3.ico")
    if os.path.exists(icon_path):
        root.iconbitmap(icon_path)

    # 현재 시간 레이블
    time_label = ctk.CTkLabel(root, text="", font=("Arial", 14))
    time_label.pack(pady=10)

    # 다음 스트레칭까지 남은 시간 레이블
    next_alert_label = ctk.CTkLabel(root, text="다음 스트레칭까지: 대기 중", font=("Arial", 14))
    next_alert_label.pack(pady=10)

    # 초 단위 카운트다운 레이블
    countdown_label = ctk.CTkLabel(root, text="", font=("Arial", 14))
    countdown_label.pack(pady=10)

    # 시간 입력 필드 (분 단위로 입력 받기)
    time_input_label = ctk.CTkLabel(root, text="스트레칭 시간을 분 단위로 입력하세요:", font=("Arial", 12))
    time_input_label.pack(pady=10)

    time_input = ctk.CTkEntry(root, font=("Arial", 14))
    time_input.pack(pady=10)

    # 현재 시간을 1초마다 갱신하는 함수
    def update_time():
        now = datetime.now()
        time_label.configure(text=f"현재 시간: {now.strftime('%Y-%m-%d %H:%M:%S')}")
        root.after(1000, update_time)

    # 시작 버튼
    start_button = ctk.CTkButton(root, text="시작", command=start_alerts, width=200, height=40)
    start_button.pack(side="left", padx=10, pady=10)

    # 리셋 버튼
    reset_button = ctk.CTkButton(root, text="리셋", command=reset_timer, width=200, height=40)
    reset_button.pack(side="left", padx=10, pady=10)

    # 종료 버튼
    exit_button = ctk.CTkButton(root, text="종료", command=root.quit, width=200, height=40)
    exit_button.pack(side="left", padx=10, pady=10)

    root.after(1000, update_time)  # 1초마다 시간 업데이트
    root.mainloop()

if __name__ == "__main__":
    start_gui()
