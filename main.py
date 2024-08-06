import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.utils import ImageReader
from PIL import Image

class RealEstateApp:
    def __init__(self, root):
        self.root = root
        self.root.title("부동산 매물 정보 입력")
        self.data = [
            {
                "agency_name": "부동산1",
                "location": "서울시 강남구",
                "area": "50",
                "deposit": "1000",
                "rent": "50",
                "options": "풀옵션",
                "floor": "3층",
                "direction": "남향",
                "new_build": "예",
                "elevator": "예",
                "image_path": "path/to/image1.jpg"
            },
            {
                "agency_name": "부동산2",
                "location": "서울시 종로구",
                "area": "30",
                "deposit": "500",
                "rent": "30",
                "options": "반옵션",
                "floor": "2층",
                "direction": "동향",
                "new_build": "아니오",
                "elevator": "아니오",
                "image_path": "path/to/image2.jpg"
            }
        ]
        self.image_path = None
        self.create_widgets()

    def create_widgets(self):
        # 고객 정보 입력
        tk.Label(self.root, text="고객 이름").grid(row=0, column=0)
        self.client_name_entry = tk.Entry(self.root)
        self.client_name_entry.grid(row=0, column=1)
        self.client_name_entry.insert(0, "기본 이름")

        tk.Label(self.root, text="연락처").grid(row=1, column=0)
        self.client_contact_entry = tk.Entry(self.root)
        self.client_contact_entry.grid(row=1, column=1)
        self.client_contact_entry.insert(0, "010-1234-5678")

        tk.Label(self.root, text="성별").grid(row=2, column=0)
        self.client_gender_entry = tk.Entry(self.root)
        self.client_gender_entry.grid(row=2, column=1)
        self.client_gender_entry.insert(0, "남성")

        tk.Label(self.root, text="입주 시기").grid(row=3, column=0)
        self.client_movein_date_entry = tk.Entry(self.root)
        self.client_movein_date_entry.grid(row=3, column=1)
        self.client_movein_date_entry.insert(0, "2024-08-01")

        tk.Label(self.root, text="거주 인원수").grid(row=4, column=0)
        self.client_residents_entry = tk.Entry(self.root)
        self.client_residents_entry.grid(row=4, column=1)
        self.client_residents_entry.insert(0, "1명")

        tk.Label(self.root, text="방 크기").grid(row=5, column=0)
        self.client_room_size_entry = tk.Entry(self.root)
        self.client_room_size_entry.grid(row=5, column=1)
        self.client_room_size_entry.insert(0, "20평")

        tk.Label(self.root, text="보증금/월세 수준").grid(row=6, column=0)
        self.client_budget_entry = tk.Entry(self.root)
        self.client_budget_entry.grid(row=6, column=1)
        self.client_budget_entry.insert(0, "1000/50")

        tk.Label(self.root, text="위치").grid(row=7, column=0)
        self.client_location_entry = tk.Entry(self.root)
        self.client_location_entry.grid(row=7, column=1)
        self.client_location_entry.insert(0, "서울")

        tk.Label(self.root, text="기타").grid(row=8, column=0)
        self.client_etc_entry = tk.Entry(self.root)
        self.client_etc_entry.grid(row=8, column=1)
        self.client_etc_entry.insert(0, "기타 사항 없음")

        tk.Label(self.root, text="특이 사항").grid(row=9, column=0)
        self.client_notes_entry = tk.Entry(self.root)
        self.client_notes_entry.grid(row=9, column=1)
        self.client_notes_entry.insert(0, "특이 사항 없음")

        # 매물 정보 입력
        labels = [
            "공인중개사 사무소 명", "매물 주소", "전용 면적 (제곱미터)",
            "보증금 (만원)", "월세 (만원)", "옵션", "층/반지하 여부",
            "방향", "신축 여부", "엘리베이터 여부"
        ]
        self.entries = []

        for i, label in enumerate(labels):
            tk.Label(self.root, text=label).grid(row=i+10, column=0)
            entry = tk.Entry(self.root)
            entry.grid(row=i+10, column=1)
            self.entries.append(entry)

        tk.Button(self.root, text="사진 선택", command=self.select_image).grid(row=len(labels)+10, column=0)
        self.image_label = tk.Label(self.root, text="선택된 사진 없음")
        self.image_label.grid(row=len(labels)+10, column=1)

        tk.Button(self.root, text="추가", command=self.add_property).grid(row=len(labels)+11, column=0)
        tk.Button(self.root, text="PDF 생성", command=self.create_pdf).grid(row=len(labels)+11, column=1)

    def select_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image_path = file_path
            self.image_label.config(text=file_path)
        else:
            messagebox.showerror("오류", "사진을 선택해주세요.")

    def add_property(self):
        try:
            property_info = [entry.get() for entry in self.entries]
            if not all(property_info) or not self.image_path:
                messagebox.showerror("오류", "모든 필드를 입력하고 사진을 선택해야 합니다.")
                return

            property_info_dict = {
                "agency_name": self.entries[0].get(),
                "location": self.entries[1].get(),
                "area": self.entries[2].get(),
                "deposit": self.entries[3].get(),
                "rent": self.entries[4].get(),
                "options": self.entries[5].get(),
                "floor": self.entries[6].get(),
                "direction": self.entries[7].get(),
                "new_build": self.entries[8].get(),
                "elevator": self.entries[9].get(),
                "image_path": self.image_path
            }

            self.data.append(property_info_dict)
            self.clear_entries()
        except Exception as e:
            messagebox.showerror("오류", f"매물을 추가하는 중 오류가 발생했습니다: {e}")

    def clear_entries(self):
        for entry in self.entries:
            entry.delete(0, tk.END)
        self.image_label.config(text="선택된 사진 없음")
        self.image_path = None

    def create_pdf(self):
        try:
            pdf_filename = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
            if pdf_filename:
                self.generate_pdf(pdf_filename)
        except Exception as e:
            messagebox.showerror("오류", f"PDF를 생성하는 중 오류가 발생했습니다: {e}")

    def generate_pdf(self, filename):
        try:
            report = RealEstateReport(filename)
            # 고객 정보 추가
            client_info = {
                "name": self.client_name_entry.get(),
                "contact": self.client_contact_entry.get(),
                "gender": self.client_gender_entry.get(),
                "movein_date": self.client_movein_date_entry.get(),
                "residents": self.client_residents_entry.get(),
                "room_size": self.client_room_size_entry.get(),
                "budget": self.client_budget_entry.get(),
                "location": self.client_location_entry.get(),
                "etc": self.client_etc_entry.get(),
                "notes": self.client_notes_entry.get()
            }
            report.add_title("부동산 원룸 매물 소개")
            for item in self.data:
                report.add_property(item)

            report.add_cover_page(client_info)
            report.add_preference_page(client_info)
            report.add_realestate_page(client_info)
            report.add_thank_you_page(client_info)
            # report.add_client_info(client_info)
            report.save()
            messagebox.showinfo("성공", "PDF 파일이 성공적으로 생성되었습니다.")
        except Exception as e:
            messagebox.showerror("오류", f"PDF를 생성하는 중 오류가 발생했습니다: {e}")

class RealEstateReport:
    def __init__(self, filename):
        self.filename = filename
        self.canvas = canvas.Canvas(filename, pagesize=A4)
        self.width, self.height = A4
        pdfmetrics.registerFont(TTFont('NanumGothic', 'NanumGothic.ttf'))
        self.background_coverPage = '00_coverPage.png'
        self.background_preferencePage = '01_preferencePage.png'
        self.background_realestatePage = '02_realestatePage.png'
        self.background_finalPage = '03_finalPage.png'
        self.index_number = 0

    def draw_background(self):
        if self.index_number == 0:
            self.canvas.drawImage(self.background_coverPage, 0, 0, width=self.width, height=self.height)
        elif self.index_number == 1:
            self.canvas.drawImage(self.background_preferencePage, 0, 0, width=self.width, height=self.height)
        elif self.index_number == 2:
            self.canvas.drawImage(self.background_realestatePage, 0, 0, width=self.width, height=self.height)
        elif self.index_number == 3:
            self.canvas.drawImage(self.background_finalPage, 0, 0, width=self.width, height=self.height)
        self.index_number += 1

    def add_title(self, title):
        self.canvas.setFont("NanumGothic", 20)
        self.canvas.setFillColor(HexColor("#000000"))
        self.canvas.drawString(72, self.height - 72, title)

    def add_client_info(self, client_info):
        y_position = self.height - 100
        self.canvas.setFont("NanumGothic", 12)
        self.canvas.setFillColor(HexColor("#000000"))
        self.canvas.drawString(72, y_position, f"이름 / 연락처 / 성별: {client_info['name']} / {client_info['contact']} / {client_info['gender']}")
        y_position -= 50
        self.canvas.drawString(72, y_position, f"입주 시기 / 거주 인원수: {client_info['movein_date']} / {client_info['residents']}")
        y_position -= 50
        self.canvas.drawString(72, y_position, f"방 크기: {client_info['room_size']}")
        y_position -= 50
        self.canvas.drawString(72, y_position, f"보증금/월세 수준: {client_info['budget']}")
        y_position -= 50
        self.canvas.drawString(72, y_position, f"위치: {client_info['location']}")
        y_position -= 50
        self.canvas.drawString(72, y_position, f"기타 : {client_info['etc']}")
        y_position -= 50
        self.canvas.drawString(72, y_position, f"특이사항: {client_info['notes']}")
        y_position -= 200

    def add_realestate_info(self, data):
        y_position = self.height - 100
        self.canvas.setFont("NanumGothic", 12)
        self.canvas.setFillColor(HexColor("#000000"))

        for item in data:
            print(item["area"])
            # self.canvas.drawString(72, y_position, f"보증금/월세: {item['deposit']} / {item['rent']} / {item['floor']}")
            # y_position -= 20
            # self.canvas.drawString(72, y_position, f"전용 면적: {item['area']} 제곱미터 (5평)")
            # y_position -= 20
            # self.canvas.drawString(72, y_position, f"위치: {item['location']} 방향: 창측 기준 {item['direction']} (아침 채광 우수)")
            # y_position -= 20
            # self.canvas.drawString(72, y_position, f"신축 여부: {item['new_build']} (1999년 준공)")
            # y_position -= 20
            # self.canvas.drawString(72, y_position, f"옵션: {item['options']}")
            # y_position -= 20
            # self.canvas.drawString(72, y_position, f"반지하/지상층: {item['floor']} 이상")
            # y_position -= 20
            # self.canvas.drawString(72, y_position, f"엘리베이터 유무: {item['elevator']}")
            # y_position -= 40
            #
            # if item['image_path']:
            #     try:
            #         self.add_image(item['image_path'], 72, y_position - 150, 200, 150)
            #         y_position -= 200
            #     except Exception as e:
            #         self.canvas.drawString(72, y_position, f"사진 추가 중 오류 발생: {e}")
            #
            # if y_position < 100:
            #     self.canvas.showPage()
            #     y_position = self.height - 100

    def add_property(self, item):
        self.canvas.setFont("NanumGothic", 12)
        y_position = self.height - 150
        self.draw_background()
        self.canvas.setFillColor(HexColor("#000000"))  # 검은색 텍스트
        self.canvas.drawString(72, y_position, f"부동산 명: {item['agency_name']}")
        y_position -= 20
        self.canvas.drawString(72, y_position, f"위치: {item['location']}")
        y_position -= 20
        self.canvas.drawString(72, y_position, f"전용 면적: {item['area']} 제곱미터")
        y_position -= 20
        self.canvas.drawString(72, y_position, f"보증금/월세: {item['deposit']} / {item['rent']}")
        y_position -= 20
        self.canvas.drawString(72, y_position, f"옵션: {item['options']}")
        y_position -= 20
        self.canvas.drawString(72, y_position, f"층/반지하 여부: {item['floor']}")
        y_position -= 20
        self.canvas.drawString(72, y_position, f"방향: {item['direction']}")
        y_position -= 20
        self.canvas.drawString(72, y_position, f"신축 여부: {item['new_build']}")
        y_position -= 20
        self.canvas.drawString(72, y_position, f"엘리베이터 여부: {item['elevator']}")
        y_position -= 20

        if item['image_path']:
            try:
                self.add_image(item['image_path'], 72, y_position - 150, 200, 150)
                y_position -= 200
            except Exception as e:
                self.canvas.drawString(72, y_position, f"사진 추가 중 오류 발생: {e}")

        if y_position < 100:
            self.canvas.showPage()
            y_position = self.height - 100

    def add_image(self, image_path, x, y, width, height):
        try:
            image = Image.open(image_path)
            image = image.resize((width, height), Image.ANTIALIAS)
            self.canvas.drawImage(ImageReader(image), x, y, width, height)
        except Exception as e:
            print(f"이미지 추가 중 오류 발생: {e}")

    def add_cover_page(self, client_name):
        self.index_number = 0
        self.canvas.showPage()  # 새로운 페이지 시작
        self.draw_background()

        self.canvas.setFont("NanumGothic", 12)

        self.canvas.drawString(72, self.height - 720, "2024.07.01 고객 열람용")

        self.canvas.setFont("NanumGothic", 55)
        self.canvas.setFillColor(HexColor("#000000"))
        self.canvas.drawString(72, self.height - 210, f"{client_name['name']} 고객님")
        self.canvas.setFont("NanumGothic", 55)
        self.canvas.drawString(72, self.height - 250, "원룸 LIST")

    def add_preference_page(self, client_info):
        self.index_number = 1
        self.canvas.showPage()  # 새로운 페이지 시작
        self.draw_background()
        self.add_client_info(client_info)

    def add_realestate_page(self, data):
        self.index_number = 2
        self.canvas.showPage()  # 새로운 페이지 시작
        self.draw_background()
        self.add_realestate_info(data)


    def add_thank_you_page(self, client_info):
        self.index_number = 3
        self.canvas.showPage()  # 새로운 페이지 시작
        self.draw_background()
        self.canvas.setFont("NanumGothic", 20)
        self.canvas.setFillColor(HexColor("#000000"))
        self.canvas.drawString(72, self.height - 72, f"{client_info['name']} 고객님 감사합니다!")


    def save(self):
        self.canvas.save()

if __name__ == "__main__":
    root = tk.Tk()
    app = RealEstateApp(root)
    root.mainloop()
