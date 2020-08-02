import os
from tkinter import * #__all__
import tkinter.ttk as ttk
from tkinter import filedialog
import tkinter.messagebox as msgbox
from PIL import Image

root = Tk()
root.title("Nado GUI")

#파일 추가
def add_file():
    files = filedialog.askopenfilenames(title ="이미지파일을선택하세요",
                                        filetypes=(("PNG파일","*.png"),("모든파일","*.*")),
                                        initialdir=r"C:\Test_Picture")
                                         #최초에 C경로를 보여줌, r을 넣어주면 그대로 쓸수 있음
    for file in files:
        list_file.insert(END, file)

#선택 삭제
def del_file():
    for index in reversed(list_file.curselection()):
        print(list_file.curselection())
        list_file.delete(index)
# 저장경로 (폴더)
def browe_dest_path():
    folder_selected = filedialog.askdirectory()
    if folder_selected =="":  # 사용자가 취소를 누를떄
        # print("취소버튼 선택")
        return
    print(folder_selected)
    txt_dest_path.delete(0,END)
    txt_dest_path.insert(0,folder_selected)

# 이미지 통합
def merge_image():
    # 가로넓이
    img_width = cmb_width.get()
    if img_width == "원본유지":
        img_width = -1 # -1일때는 원본기준으로
    else:
        img_width = int(img_width)

    # 간격
    img_space = cmb_space.get()
    if img_space =="좁게":
        img_space = 30
    if img_space =="보통":
        img_space = 60
    if img_space =="넓게":
        img_space = 90
    else:
        img_space=0
    # 포멧
    img_format = cmb_format.get().lower() # 소문자로 변경
    #########################################################################
    print(list_file.get(0,END)) # 모든 파일 목록 가지고오기
    images = [Image.open(x) for x in list_file.get(0,END)]

    #이미지 사이즈를 리스트에 넣어서 하나씩 처리
    # image_sizes = [] # [(w,h), (w,h)...]
    if img_width > -1:
        image_sizes = [(int(img_width), int(img_width*x.size[1]/x.size[0])) for x in images]  #width 값 비율에 맞게 변경
    else:
        #원본 사이즈 활용
        image_sizes = [(x.size[0], x.size[1]) for x in images]

    width, height = zip( * (image_sizes))  # zip을 이용해서 분할하기

    #최대 넓이 , 전체 높이 구하기
    max_width, total_height = max(width), sum(height)

    #스케치북

    if img_space > 0: # 이미지 간격 옵션 적용
        total_height += (img_space * (len(images)-1))

    result_img = Image.new("RGB",(max_width, total_height), (255,255,255)) # 배경 흰색
    y_offset = 0 # 위치

    #스케치북에 이미지 붙이기
    # for img in images:
    #     result_img.paste(img,(0,y_offset))
    #     y_offset+=img.size[1]  # height 값 만큼 더해줌
    for idx,img in enumerate(images):
        #width가 원본유지가 아닐떄 이미지 크기 조정
        if img_width > -1:
            img = img.resize(image_sizes[idx])

        result_img.paste(img, (0, y_offset))  #height 값 + 사용자가 지정한 간격격
        y_offset += (img.size[1] + img_space)  # height 값 만큼 더해줌
        progress = (idx+1)/len(images) * 100 # 실제 Percent 정보를 계산
        p_var.set(progress)
        progress_bar.update()

    #포멧 옵션 처리
    file_name = "nado_phto." + img_format
    dest_path = os.path.join(txt_dest_path.get(), file_name)
    result_img.save(dest_path)
    msgbox.showinfo("알림","작업완료되었습니다")


# 시작
def start():
    # 파일목록 확인
    if list_file.size() == 0:
        msgbox.showwarning("경고","이미지파일을 추가하세요")
    # 저장경로 확인
    if len(txt_dest_path.get()) == 0:
        msgbox.showwarning("경고","저장경로를 선택 하세요")

    # 이미지 통합 작업
    merge_image()


#■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
# 파일 프레임(파일 추가, 선택 삭제)
file_frame = Frame(root)
# file_frame.pack()
file_frame.pack(fill="x",padx=5, pady=5)

btn_add_file = Button(file_frame, padx=5, pady=5, width=12, text ="파일추가", command=add_file)
btn_add_file.pack(side="left")

btn_del_file = Button(file_frame, padx=5, pady=5, width=12, text ="선택삭제",command=del_file)
btn_del_file.pack(side="right")

#리스트 프레임
list_frame = Frame(root)
list_frame.pack(fill="both",padx=5, pady=5)

scrollbar = Scrollbar(list_frame)
scrollbar.pack(side="right",fill="y")

list_file = Listbox(list_frame, selectmode="extended", height=15, yscrollcommand =scrollbar.set)
list_file.pack(side="left", fill="both", expand=True)
scrollbar.config(command=list_file.yview)

#저장경로 프레임
path_frame = LabelFrame(root, text ="저장경로")
path_frame.pack(fill="x",padx=5, pady=5, ipady=10)
# path_frame.pack(fill="x",padx=5, pady=5)

txt_dest_path = Entry(path_frame)
txt_dest_path.pack(side="left", fill="x", expand=True, ipady=5)# 높이 변경

btn_dest_path = Button(path_frame, text = "찾아보기", width=10, command = browe_dest_path)
btn_dest_path.pack(side="right")

# 옵션 프레임
frame_option = LabelFrame(root,text="옵셧")
frame_option.pack(padx=5, pady=5)

#1.가로넓이 옵션
# 가로넓이 레이블
lbl_width = Label(frame_option, text="가로넓이", width = 8)
lbl_width.pack(side="left",padx=5, pady=5)
# 가로넓이 콤보
opt_width = ["원본유지", "1024", "800", "640"]
cmb_width = ttk.Combobox(frame_option, state="readonly", values=opt_width, width = 10)
cmb_width.current(0)
cmb_width.pack(side="left",padx=5, pady=5)

#2.간격 옵션
# 간격옵션 레이블
lbl_space = Label(frame_option, text="간격", width = 8)
lbl_space.pack(side="left",padx=5, pady=5)
# 간격옵션 콤보
opt_space = ["없음", "좁게","보통","넓게"]
cmb_space = ttk.Combobox(frame_option, state="readonly", values=opt_space, width = 10)
cmb_space.current(0)
cmb_space.pack(side="left",padx=5, pady=5)

#3.파일 포멧 옵션
# 포멧 레이블
lbl_format = Label(frame_option, text="포멧", width = 8)
lbl_format.pack(side="left",padx=5, pady=5)
# 포멧 콤보
opt_format = ["PNG","JPG","BMP"]
cmb_format = ttk.Combobox(frame_option, state="readonly", values=opt_format, width = 10)
cmb_format.current(0)
cmb_format.pack(side="left",padx=5, pady=5)

#진행상황 Progress Bar

frame_progress = LabelFrame(root,text="진행상황")
frame_progress.pack(fill="x",padx=5, pady=5)

p_var = DoubleVar()
progress_bar = ttk.Progressbar(frame_progress, maximum=100, variable=p_var)
progress_bar.pack(fill="x",padx=5, pady=5)


# 실행프레임
frame_run = Frame(root)
frame_run.pack(fill="x",padx=5, pady=5)

btn_close = Button(frame_run, padx=5, pady=4, text="닫기",width=12, command = root.quit)
btn_close.pack(side="right",padx=5, pady=5)

btn_start = Button(frame_run, padx=5, pady=4, text="시작",width=12, command = start)
btn_start.pack(side="right")


root.resizable(False, False)
root.mainloop()
