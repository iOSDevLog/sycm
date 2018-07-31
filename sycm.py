# -*- coding: utf-8 -*-
import time
import os
import csv
from datetime import datetime,timedelta
import tkinter as tk
from tkinter import messagebox as msg
from date_utils import *
from topkeywords_stream import fetchStreamTopKeywords
from topkeywords_deal import fetchDealTopKeywords

class Timer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("生意参谋")
        self.geometry("500x800")
        self.resizable(False, False)

        self.standard_font = (None, 16)

        self.main_frame = tk.Frame(self, width=500, height=800, bg="lightgrey")

        self.val1_label = tk.Label(self.main_frame, text="竞品1 ID", bg="lightgrey", fg="black", font=self.standard_font)
        self.val1_entry = tk.Entry(self.main_frame, bg="white", fg="black", font=self.standard_font)

        self.val2_label = tk.Label(self.main_frame, text="竞品2 ID", bg="lightgrey", fg="black", font=self.standard_font)
        self.val2_entry = tk.Entry(self.main_frame, bg="white", fg="black", font=self.standard_font)

        self.start_date_label = tk.Label(self.main_frame, text="开始日期", bg="lightgrey", fg="black", font=self.standard_font)
        self.start_date_entry = tk.Entry(self.main_frame, bg="white", fg="black", font=self.standard_font)

        self.end_date_label = tk.Label(self.main_frame, text="结束日期:", bg="lightgrey", fg="black", font=self.standard_font)
        self.end_date_entry = tk.Entry(self.main_frame, bg="white", fg="black", font=self.standard_font)

        self.start_button = tk.Button(self.main_frame, text="运行", bg="lightgrey", fg="black", command=self.start, font=self.standard_font)

        progress = tk.StringVar()
        self.progress_label = tk.Label(self.main_frame, text="当前处理日期:", bg="lightgrey", fg="black", font=self.standard_font)
        self.progress_entry = tk.Entry(self.main_frame, bg="white", fg="black", font=self.standard_font, textvariable=progress)

        self.main_frame.pack(fill=tk.BOTH, expand=1)

        self.val1_label.pack(fill=tk.X, pady=10)
        self.val1_entry.pack(fill=tk.X, padx=50, pady=(0,20))
        self.val1_entry.insert(0,"25649816644")

        self.val2_label.pack(fill=tk.X, pady=10)
        self.val2_entry.pack(fill=tk.X, padx=50, pady=(0,20))
        self.val2_entry.insert(0,"524007275779")

        self.start_date_label.pack(fill=tk.X, pady=10)
        self.start_date_entry.pack(fill=tk.X, padx=50, pady=(0,20))
        self.start_date_entry.insert(0,"2018-07-01")

        self.end_date_label.pack(fill=tk.X, pady=10)
        self.end_date_entry.pack(fill=tk.X, padx=50, pady=(0,20))
        self.end_date_entry.insert(0,"2018-07-29")

        self.start_button.pack(fill=tk.X, padx=50)

        self.progress_label.pack(fill=tk.X, pady=10)
        self.progress_entry.pack(fill=tk.X, padx=50, pady=(0,20))

    def start(self):
        start_date_string = self.start_date_entry.get()
        end_date_string = self.end_date_entry.get()
        rival1Id = self.val1_entry.get()
        rival2Id = self.val2_entry.get()
        start_date = stringToDate(start_date_string)
        end_date = stringToDate(end_date_string)
        print(dateToString(start_date))
        print(dateToString(end_date))
        self.progress_entry.delete(0, tk.END)
        self.progress_entry.insert(0,"开始处理")

        stream1s = []
        deal1s = []
        stream2s = []
        deal2s = []

        date_string = start_date_string + "_" + end_date_string

        for i in range((end_date - start_date).days):

            day = start_date + timedelta(days=i)
            stringDay = dateToString(day)
            # print(day)
            progress = stringDay
            self.progress_entry.delete(0, tk.END)
            self.progress_entry.insert(0, progress)
            (stream1, stream2) = fetchStreamTopKeywords(stringDay, int(rival1Id), int(rival2Id))
            (deal1, deal2) = fetchDealTopKeywords(stringDay, int(rival1Id), int(rival2Id))
            stream1s.extend(stream1)
            stream2s.extend(stream2)
            deal1s.extend(deal1)
            deal2s.extend(deal2)

            with open('引流/' + str(rival1Id) + '_' + date_string + '.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                for stream in stream1s:
                    writer.writerow([stream.keyword.value , stream.uv.value])

            with open('引流/' + str(rival2Id) + '_' + date_string + '.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                for stream in stream2s:
                    writer.writerow([stream.keyword.value , stream.uv.value])

            with open('交易/' + str(rival1Id) + '_' + date_string + '.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                for deal in deal1s:
                    writer.writerow([deal.keyword.value , deal.pay_item_cnt.value])

            with open('交易/' + str(rival2Id) + '_' + date_string + '.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                for deal in deal2s:
                    writer.writerow([deal.keyword.value , deal.pay_item_cnt.value])

        self.progress_entry.delete(0, tk.END)
        self.progress_entry.insert(0,"完成")


def mkdir(path):
	folder = os.path.exists(path)

	if not folder:
		os.makedirs(path)
		print("创建成功")
	else:
		print("文件夹已经存在")


if __name__ == "__main__":
    file = "引流"
    mkdir(file)
    file = "交易"
    mkdir(file)

    timer = Timer()
    timer.mainloop()
