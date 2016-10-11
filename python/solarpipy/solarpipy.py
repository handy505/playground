#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading
import serial
import logging
import upload


def main():
    """
    主程式
    維護系統運作，如網路斷線偵測、重連。
    serial port取得遠端機器狀態
    考量網路斷線時，需log在本地端，待網路恢復後，再將未上傳之紀錄上傳至server
    於是，衍生了logging_task與upload_task
    每小時紀錄理論上應由伺服端計算，現實上有效能考量，故由本地端做每小時快取後上傳。
    """

    ths = serial.SerialTask()
    thl = logging.LoggingTask()
    thu = upload.UploadTask()


    ths.start()
    thl.start()
    thu.start()


    ths.join()
    thl.join()
    thu.join()

if __name__ == "__main__":
    main()