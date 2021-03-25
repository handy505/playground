#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import threading
import re
import time
import serial
import optparse
import collections
import queue
import tkinter as tk

import solarpi
import serial2
import logging2
import upload
import pvinverter
import hearbeat
import debug_off as mydebug


class ViewPVDetail(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        
        self.master.wm_title("Detail")

        
        self.fields = []
        self.tab = []
        for i in range(0, 8):
            js = []
            for j in range(0, 20):
                var = tk.StringVar()
                var.set("{}, {}".format(i, j))
                js.append(var)
                if i == 0:
                    tk.Label(self, textvariable=var, width=16, fg="red", anchor=tk.E).grid(row=j, column=i)
                else:
                    if j % 2 == 0:
                        tk.Label(self, textvariable=var, width=8, fg="green").grid(row=j, column=i)
                    else:
                        tk.Label(self, textvariable=var, width=8, fg="black").grid(row=j, column=i)
            self.tab.append(js)
        
        self.tab[0][1].set("OutputPower")
        self.tab[0][2].set("ACVolPhaseA")
        self.tab[0][3].set("ACVolPhaseB")
        self.tab[0][4].set("ACVolPhaseC")
        self.tab[0][5].set("ACFrequency")
        self.tab[0][6].set("ACOutputCurrentA")
        self.tab[0][7].set("ACOutputCurrentB")
        self.tab[0][8].set("ACOutputCurrentC")
        self.tab[0][9].set("DC1InputVol")
        self.tab[0][10].set("DC2InputVol")
        self.tab[0][11].set("DC1InputCurrent")
        self.tab[0][12].set("DC2InputCurrent")
        self.tab[0][13].set("DCBusPositiveVol")
        self.tab[0][14].set("DCBusNegativeVol")
        self.tab[0][15].set("InternalTemper")
        self.tab[0][16].set("HeatSinkTemper")
        self.tab[0][17].set("InputPowerA")
        self.tab[0][18].set("InputPowerB")
        self.tab[0][19].set("TotalOutputPower")
        
        self.grid()

        
    def update(self, subject, msg=""):
        
        if isinstance(subject, pvinverter.PVInverter):

            ts = time.strftime('%H:%M:%S', time.localtime(round(time.time())))
            pvno = subject.id
            self.tab[pvno][0].set(str(subject.name))
            self.tab[pvno][1].set(str(subject.OutputPower))
            self.tab[pvno][2].set(str(subject.ACVolPhaseA))
            self.tab[pvno][3].set(str(subject.ACVolPhaseB))
            self.tab[pvno][4].set(str(subject.ACVolPhaseC))
            self.tab[pvno][5].set(str(subject.ACFrequency))
            self.tab[pvno][6].set(str(subject.ACOutputCurrentA))
            self.tab[pvno][7].set(str(subject.ACOutputCurrentB))
            self.tab[pvno][8].set(str(subject.ACOutputCurrentC))
            self.tab[pvno][9].set(str(subject.DC1InputVol))
            self.tab[pvno][10].set(str(subject.DC2InputVol))
            self.tab[pvno][11].set(str(subject.DC1InputCurrent))
            self.tab[pvno][12].set(str(subject.DC2InputCurrent))
            self.tab[pvno][13].set(str(subject.DCBusPositiveVol))
            self.tab[pvno][14].set(str(subject.DCBusNegativeVol))
            self.tab[pvno][15].set(str(subject.InternalTemper))
            self.tab[pvno][16].set(str(subject.HeatSinkTemper))
            self.tab[pvno][17].set(str(subject.InputPowerA))
            self.tab[pvno][18].set(str(subject.InputPowerB))
            self.tab[pvno][19].set(str(subject.TotalOutputPower))


class Application(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master.wm_title("tk gui")
        self.grid()
        self.create_widgets()


    def create_widgets(self):
        ROWOFFSET = 0
        tk.Label(self, text="serial", width=10, anchor=tk.E).grid(row=ROWOFFSET, column=0)
        self.varSerialTx = tk.StringVar()
        tk.Label(self, textvariable=self.varSerialTx, width=50, anchor=tk.W).grid(row=ROWOFFSET, column=1)
        self.varSerialRx = tk.StringVar()
        tk.Label(self, textvariable=self.varSerialRx, width=50, anchor=tk.W).grid(row=ROWOFFSET+1, column=1)
        self.varSerial = tk.StringVar()
        tk.Label(self, textvariable=self.varSerial, width=50, anchor=tk.W).grid(row=ROWOFFSET+2, column=1)

        ROWOFFSET = 3 
        tk.Label(self, text="s pipelines", width=10, anchor=tk.E).grid(row=ROWOFFSET, column=0)
        self.q1var = tk.StringVar()
        tk.Label(self, textvariable=self.q1var, width=50, anchor=tk.W, fg="red").grid(row=ROWOFFSET, column=1)
        
        ROWOFFSET = 4
        tk.Label(self, text="logging", width=10, anchor=tk.E).grid(row=ROWOFFSET, column=0)
        self.loggingVars1 = tk.StringVar()
        tk.Label(self, textvariable=self.loggingVars1, width=50, anchor=tk.W).grid(row=ROWOFFSET, column=1)
        self.loggingVars2 = tk.StringVar()
        tk.Label(self, textvariable=self.loggingVars2, width=50, anchor=tk.W).grid(row=ROWOFFSET+1, column=1)
        self.loggingVars3 = tk.StringVar()
        tk.Label(self, textvariable=self.loggingVars3, width=50, anchor=tk.W).grid(row=ROWOFFSET+2, column=1)

        ROWOFFSET = 7
        tk.Label(self, text="u pipelines", width=10, anchor=tk.E).grid(row=ROWOFFSET, column=0)
        self.q2var = tk.StringVar()
        tk.Label(self, textvariable=self.q2var, width=50, anchor=tk.W, fg="red").grid(row=ROWOFFSET, column=1)

        ROWOFFSET = 8
        tk.Label(self, text="fb pipelines", width=10, anchor=tk.E).grid(row=ROWOFFSET, column=0)
        self.q3var = tk.StringVar()
        tk.Label(self, textvariable=self.q3var, width=50, anchor=tk.W, fg="red").grid(row=ROWOFFSET, column=1)
        
        ROWOFFSET = 9
        tk.Label(self, text="upload", width=10, anchor=tk.E).grid(row=ROWOFFSET, column=0)
        self.varUploadEvent = tk.StringVar()
        tk.Label(self, textvariable=self.varUploadEvent, width=50, anchor=tk.W).grid(row=ROWOFFSET, column=1)
        self.varUploadMinute = tk.StringVar()
        tk.Label(self, textvariable=self.varUploadMinute, width=50, anchor=tk.W).grid(row=ROWOFFSET+1, column=1)
        self.varUploadHour = tk.StringVar()
        tk.Label(self, textvariable=self.varUploadHour, width=50, anchor=tk.W).grid(row=ROWOFFSET+2, column=1)
        self.varUploadMessage = tk.StringVar()
        tk.Label(self, textvariable=self.varUploadMessage, width=50, anchor=tk.W).grid(row=ROWOFFSET+3, column=1)
        
        
        ROWOFFSET = 13 
        tk.Label(self, text="hearbeat", width=10, anchor=tk.E).grid(row=ROWOFFSET, column=0)
        self.varHearbeat = tk.StringVar()
        tk.Label(self, textvariable=self.varHearbeat, width=50, anchor=tk.W).grid(row=ROWOFFSET, column=1)

        ROWOFFSET = 14
        tk.Label(self, text="main", width=10, anchor=tk.E).grid(row=ROWOFFSET, column=0)
        self.varMain = tk.StringVar()
        tk.Label(self, textvariable=self.varMain, width=50, anchor=tk.W).grid(row=ROWOFFSET, column=1)

        self.varThread0 = tk.StringVar()
        tk.Label(self, textvariable=self.varThread0, width=10, anchor=tk.E).grid(row=ROWOFFSET+1, column=0)
        self.varThread1 = tk.StringVar()
        tk.Label(self, textvariable=self.varThread1, width=50, anchor=tk.W).grid(row=ROWOFFSET+1, column=1)

        ROWOFFSET = 16
        tk.Button(self, text="pv detail", fg="red", command=self.detail).grid(row=ROWOFFSET, column=0, columnspan=2, sticky=tk.EW)


    def bind(self, maintask):
        self.maintask = maintask


    def detail(self):
        ''' 開新表單，做為觀察者，並將自已註冊給每個pv物件'''
        f = ViewPVDetail(master=tk.Toplevel()) # tk multi windows, use Toplevel()
        for i, pv in enumerate(self.maintask.ths.pvgroup):
            pv.attach(f)


    def quit(self):
        self.master.quit()
        

    def update(self, subject):

        if isinstance(subject, serial2.SerialTask):
            s = 'polling pv {name}/{amount}'.format(
                name=subject.processing_pv.id,
                amount=len(subject.pvgroup))
            self.varSerial.set(s)

            s = "{e}/{m}/{h}".format(
                e=subject.event_output_pipeline.qsize(),
                m=subject.minute_output_pipeline.qsize(),
                h=subject.hour_output_pipeline.qsize())
            self.q1var.set(s)

        elif isinstance(subject, pvinverter.PVInverter):
            self.varSerialTx.set(subject.txpkt)
            self.varSerialRx.set(subject.rxpkt)

        elif isinstance(subject, logging2.LoggingTask):
            s = "{e}/{m}/{h}".format(
                e=subject.event_input_pipeline.qsize(),
                m=subject.minute_input_pipeline.qsize(),
                h=subject.hour_input_pipeline.qsize())
            self.q1var.set(s)

            s = "{ue}/{um}/{uh}".format(
                ue=subject.event_output_pipeline.qsize(),
                um=subject.minute_output_pipeline.qsize(),
                uh=subject.hour_output_pipeline.qsize())
            self.q2var.set(s)

            s = "{fe}/{fm}/{fh}".format(
                fe=subject.event_feedback_pipeline.qsize(),
                fm=subject.minute_feedback_pipeline.qsize(),
                fh=subject.hour_feedback_pipeline.qsize())
            self.q3var.set(s)

            rlen = len(subject.em.rlist)
            ulen = len(subject.em.ulist)
            sec = round(time.time() - subject.em.timestamp)
            s = 'event db: {} to {}, {} waiting, {} changed({} sec)'.format(
                ulen, rlen, rlen-ulen, subject.em.changed_count, sec) 
            self.loggingVars1.set(s)
            
            rlen = len(subject.mm.rlist)
            ulen = len(subject.mm.ulist)
            sec = round(time.time() - subject.mm.timestamp)
            s = 'minute db: {} to {}, {} waiting, {} changed({} sec)'.format(
                ulen, rlen, rlen-ulen, subject.mm.changed_count, sec) 
            self.loggingVars2.set(s)

            rlen = len(subject.hm.rlist)
            ulen = len(subject.hm.ulist)
            sec = round(time.time() - subject.hm.timestamp)
            s = 'hour db: {} to {}, {} waiting, {} changed({} sec)'.format(
                ulen, rlen, rlen-ulen, subject.hm.changed_count, sec) 
            self.loggingVars3.set(s)

        elif isinstance(subject, upload.UploadTask):
            self.varUploadEvent.set("event {}".format(subject.event_post_response))
            self.varUploadMinute.set("minute {}".format(subject.minute_post_response))
            self.varUploadHour.set("hour {}".format(subject.hour_post_response))
            s = '{} to psid {}'.format(subject.status, subject.psid)
            self.varUploadMessage.set(s)

            s = "{ue}/{um}/{uh}".format(
                ue=subject.event_input_pipeline.qsize(),
                um=subject.minute_input_pipeline.qsize(),
                uh=subject.hour_input_pipeline.qsize())
            self.q2var.set(s)

            s = "{fe}/{fm}/{fh}".format(
                fe=subject.event_output_pipeline.qsize(),
                fm=subject.minute_output_pipeline.qsize(),
                fh=subject.hour_output_pipeline.qsize())
            self.q3var.set(s)


        elif isinstance(subject, hearbeat.Hearbeat):

            s = '{ts} send: {hb}, rcv: {rcv}'.format(
                ts=time.strftime('%H:%M:%S', time.localtime(round(time.time()))),
                hb=subject.hearbeat_str,
                rcv=subject.recv_data
            )
            self.varHearbeat.set(s)


        elif isinstance(subject, solarpi.MainTask):
            tdiff = subject.tm_terminate - time.time()
            secs = round(tdiff)  
            self.varMain.set('will terminat after {} seconds'.format(secs))
            
            self.varThread0.set('threads({})'.format(threading.active_count()))

            ts = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(round(time.time())))
            self.master.wm_title("tk gui {}".format(ts))


        t = threading.enumerate()
        s = ', '.join([i.name for i in t])
        self.varThread1.set(s)        


if __name__ == "__main__":

    print("tkgui")

    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
        
