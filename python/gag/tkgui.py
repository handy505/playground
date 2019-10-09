import tkinter as tk
from tkinter.font import Font
import tkinter.scrolledtext as tkst
import time
import threading
import datetime
import os
import smtplib
import queue
import subprocess

import collector
import handyutil
import duplex_factory 
import hearbeat
import uploader



class MainPage(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rs485tx            = tk.StringVar()
        self.rs485rx            = tk.StringVar()
        self.status             = tk.StringVar()
        self.upload_server_ip   = tk.StringVar()
        self.mac                = tk.StringVar()
        self.psid               = tk.StringVar()
        self.gwid               = tk.StringVar()
        self.upload_response    = tk.StringVar()
        self.hearbeat_server_ip = tk.StringVar()
        self.hearbeat_tx        = tk.StringVar()
        self.hearbeat_rx        = tk.StringVar()
        self.system_time        = tk.StringVar()
        self.temp               = tk.StringVar()
        self.watchdog           = tk.StringVar()
        self.version            = tk.StringVar()

        self.rs485tx.set('RS485 Tx: xx xx xx xx')
        self.rs485rx.set('RS485 Rx: xx xx xx xx')
        self.status.set('Status: 99,a,b,c,d,e')
        self.upload_server_ip.set('Server IP:')
        self.mac.set('MAC: {}'.format(handyutil.get_bluetooth_mac()))
        self.psid.set('PSID:')
        self.gwid.set('GWID:')
        self.upload_response.set('Upload response:')
        self.hearbeat_server_ip.set('Hearbeat server IP:')
        self.hearbeat_tx.set('Hearbeat tx:')
        self.hearbeat_rx.set('Hearbeat rx:')
        self.system_time.set('System time:')
        self.temp.set('Temp:')
        self.watchdog.set('Watchdog:')
        self.version.set('Version: {}'.format(handyutil.get_version()))

        fontstyle = 'TkFixedFont'
        
        lbl = tk.Label(self, anchor=tk.W, font=fontstyle, textvariable=self.rs485tx)
        lbl.pack(side="top", fill="both", expand=False)

        lbl = tk.Label(self, anchor=tk.W, font=fontstyle, textvariable=self.rs485rx)
        lbl.pack(side="top", fill="both", expand=False)

        lbl = tk.Label(self, anchor=tk.W, font=fontstyle, textvariable=self.status)
        lbl.pack(side="top", fill="both", expand=False)

        lbl = tk.Label(self, anchor=tk.W, font=fontstyle, textvariable=self.upload_server_ip)
        lbl.pack(side="top", fill="both", expand=False)

        lbl = tk.Label(self, anchor=tk.W, font=fontstyle, textvariable=self.psid)
        lbl.pack(side="top", fill="both", expand=False)

        lbl = tk.Label(self, anchor=tk.W, font=fontstyle, textvariable=self.gwid)
        lbl.pack(side="top", fill="both", expand=False)

        lbl = tk.Label(self, anchor=tk.W, font=fontstyle, textvariable=self.upload_response)
        lbl.pack(side="top", fill="both", expand=False)

        lbl = tk.Label(self, anchor=tk.W, font=fontstyle, textvariable=self.mac)
        lbl.pack(side="top", fill="both", expand=False)

        lbl = tk.Label(self, anchor=tk.W, font=fontstyle, textvariable=self.hearbeat_server_ip)
        lbl.pack(side="top", fill="both", expand=False)

        lbl = tk.Label(self, anchor=tk.W, font=fontstyle, textvariable=self.hearbeat_tx)
        lbl.pack(side="top", fill="both", expand=False)

        lbl = tk.Label(self, anchor=tk.W, font=fontstyle, textvariable=self.hearbeat_rx)
        lbl.pack(side="top", fill="both", expand=False)

        lbl = tk.Label(self, anchor=tk.W, font=fontstyle, textvariable=self.system_time)
        lbl.pack(side="top", fill="both", expand=False)

        lbl = tk.Label(self, anchor=tk.W, font=fontstyle, textvariable=self.temp)
        lbl.pack(side="top", fill="both", expand=False)

        lbl = tk.Label(self, anchor=tk.W, font=fontstyle, textvariable=self.watchdog)
        lbl.pack(side="top", fill="both", expand=False)

        lbl = tk.Label(self, anchor=tk.W, font=fontstyle, textvariable=self.version)
        lbl.pack(side="top", fill="both", expand=False)


class ScrollableFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.canvas = tk.Canvas(self)
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.frame = tk.Frame(self.canvas)
        self.frame.pack(side=tk.LEFT, fill=tk.Y, expand=True)

        vbar = tk.Scrollbar(self.canvas, orient=tk.VERTICAL, command=self.canvas.yview)
        vbar.pack(side=tk.RIGHT, fill=tk.Y, expand=False)

        self.canvas.config(yscrollcommand=vbar.set)
        self.frameid = self.canvas.create_window((0,0), window=self.frame, anchor=tk.NW)

        self.frame.bind('<Configure>', self.configure_frame)
        self.canvas.bind('<Configure>', self.configure_canvas)
        self.canvas.bind_all('<Button-4>', self.on_mousewheel)
        self.canvas.bind_all('<Button-5>', self.on_mousewheel)

    def on_mousewheel(self, event):
        if event.num  == 5:     self.canvas.yview_scroll( 1, 'units')
        elif event.num == 4:    self.canvas.yview_scroll(-1, 'units')

    def configure_frame(self, event):
        size = (self.frame.winfo_reqwidth(), self.frame.winfo_reqheight())
        self.canvas.config(scrollregion='0 0 {} {}'.format(size[0], size[1]))
        if self.frame.winfo_reqwidth() != self.canvas.winfo_width():
            self.canvas.config(width=self.frame.winfo_reqwidth())

    def configure_canvas(self, event):
        if self.frame.winfo_reqwidth() != self.canvas.winfo_width():
            self.canvas.itemconfigure(self.frameid, width=self.canvas.winfo_width())


class InverterSummaryPage(ScrollableFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configurations = self.get_configurations()
        identifies = self.parse_inverters(self.configurations)

        self.current_inverter_id = None
        self.inverter_stringvars = {}
        self.inverter_labels = {}
        sorted_identifies = sorted(identifies, reverse=True)
        for i in range(0,200):
            try:
                identify = sorted_identifies.pop()
                svar = tk.StringVar()
                svar.set('I am Inverter-{}'.format(identify))

                lbl = tk.Label(self.frame, textvariable=svar, anchor=tk.W, font='TkFixedFont')
                lbl.pack(side=tk.TOP, fill=tk.X, expand=False)

                self.inverter_stringvars[identify] = svar 
                self.inverter_labels[identify] = lbl 
            except IndexError as ex:
                break

    def get_configurations(self):
        p = subprocess.Popen(['cat', './data/config.txt'], stdout=subprocess.PIPE)
        out, err = p.communicate()
        return out.decode('utf-8')

    def parse_inverters(self, configurations):
        try:
            result = []
            lines = configurations.splitlines() 
            for line in lines:
                if line.startswith('pv='):
                    line = line.strip()
                    valuestring = line.split('=')[1]
                    values = valuestring.split(',')
                    values = iter(values)
                    for invid, portid in zip(values, values):
                        result.append(int(invid))
            return result 
        except (IndexError, ValueError) as ex:
            print('Exception in parse_inverters()')
            return []


class MeterPage(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.illu_msg = tk.StringVar()
        self.illu_msg.set('Illumination message line')
        self.temp_msg = tk.StringVar()
        self.temp_msg.set('Temperature message line')

        fontstyle = 'TkFixedFont'
        lbl = tk.Label(self, textvariable=self.illu_msg, anchor=tk.W, font=fontstyle)
        lbl.pack(side=tk.TOP, fill=tk.BOTH, expand=False)
        lbl = tk.Label(self, textvariable=self.temp_msg, anchor=tk.W, font=fontstyle)
        lbl.pack(side=tk.TOP, fill=tk.BOTH, expand=False)


class FactoryPage(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.factory_text = tk.Text(self, height=15)
        self.factory_text.pack(side='top', fill='both', expand=True)

        self.colorbar = tk.Label(self, bg='green')
        self.colorbar.pack(side='top', fill='both', expand=True)

        tk.Button(self, text='Send Teamviewer ID', command=self.send_teamviewer_id).pack(side='top', fill='both', expand=True)
        tk.Button(self, text='Get PSID', command=self.get_psid).pack(side='top', fill='both', expand=True)

        bframe = tk.Frame(self, bg='black')
        bframe.pack(side='top', fill='both', expand=True)
        tk.Button(bframe, text='Ping www.baidu.com', command=self.ping_baidu).pack(side='left', fill='both', expand=True)
        tk.Button(bframe, text='Ping www.sina.com.cn', command=self.ping_sina).pack(side='left', fill='both', expand=True)
        tk.Button(bframe, text='Ping www.163.com', command=self.ping_163).pack(side='right', fill='both', expand=True)

        tk.Button(self, text='Clear', command=self.clear).pack(side='top', fill='both', expand=True)
        tk.Button(self, text='Delete settings/data and REBOOT', fg='red', command=self.factory_reset).pack(side='top', fill='both', expand=True)


    def send_teamviewer_id(self):
        cmd = 'sudo teamviewer passwd 1234567890'
        os.system(cmd)

        cmd = "hciconfig | grep 'BD Address' | awk {'print $3'}"
        btmac = os.popen(cmd).read().strip('\n')
        btmac = btmac.lower()
        btmac = btmac.replace(':', '')
        
        cmd  = "teamviewer info | grep 'TeamViewer ID' | awk {'print $5'}"
        tvid = os.popen(cmd).read().strip('\n')

        mailSubject = 'solarpi bt={},tv={}'.format(btmac, tvid)
        mailmsg = 'Subject:{}'.format(mailSubject)
        #print(mailmsg)
        self.send_mail(mailmsg)
        self.factory_text.delete(1.0, tk.END)
        self.factory_text.insert(tk.INSERT, mailmsg)


    def send_mail(self, msg):
        smtpDstAddr = 'handy.gspace@gmail.com'
        smtpSrcAddr = 'handy.gspace@gmail.com'

        smtpServer = 'smtp.gmail.com'
        smtpPwd = 'qvlgvipomgmdklxb'
        smtpPort = 587

        mySmtp = smtplib.SMTP(smtpServer, smtpPort)
        mySmtp.starttls()
        mySmtp.login(smtpSrcAddr, smtpPwd)
        mySmtp.sendmail(smtpSrcAddr, smtpDstAddr, msg)
        mySmtp.close()


    def get_psid(self):
        ret = handyutil.get_psid_and_gwid()
        if ret: msg = 'PSID = {}, GWID={}'.format(ret[0], ret[1])
        else:   msg = 'error' 

        self.factory_text.delete(1.0, tk.END)
        self.factory_text.insert(tk.INSERT, msg)
        if msg: self.colorbar.config(bg='green')
        else:   self.colorbar.config(bg='red')


    def ping_baidu(self):
        self.ping('www.baidu.com')

    def ping_sina(self):
        self.ping('www.sina.com.cn')

    def ping_163(self):
        self.ping('www.163.com')

    def ping(self, ip):
        cmd = 'sudo ping {} -c 3'.format(ip)
        result = os.popen(cmd).read()
        self.factory_text.delete(1.0, tk.END)
        self.factory_text.insert(tk.INSERT, result)

        if 'rtt' in result: self.colorbar.config(bg='green')
        else:               self.colorbar.config(bg='red')

    def clear(self):
        self.factory_text.delete(1.0, tk.END)


    def factory_reset(self):
        os.system('rm ./data/*')

        # log reboot
        msg = 'delete-data reboot at {}'.format(datetime.datetime.now())
        cmd = 'echo "{}" >> reboot.log'.format(msg)
        os.system(cmd)
        os.system('reboot')


class DuplexPage(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        f = Font(family='Helvetica', size=12)

        title = tk.Label(self, text='Duplex Command Patterns:', anchor=tk.W, font=f, bg='green')
        title.grid(row=0, columnspan=5, sticky=tk.E+tk.W)

        pattern1 = tk.Label(self, text='cmd@psid@devid@sn', anchor=tk.W, fg='red', font=f)
        pattern1.grid(row=1, columnspan=3, sticky=tk.E+tk.W)
        pattern2 = tk.Label(self, text='cmd@data@psid@devid@sn', anchor=tk.W, fg='red', font=f)
        pattern2.grid(row=2, columnspan=3, sticky=tk.E+tk.W)


        btn_readpvsn = tk.Button(self, text='readpvsn', command=self.readpvsn)
        btn_readpvsn.grid(row=3, column=0, sticky=tk.E+tk.W)

        tk.Button(self, text='reserve').grid(row=4, column=0, sticky=tk.E+tk.W)

        btn_readpvfw = tk.Button(self, text='readpvfw', command=self.readpvfw)
        btn_readpvfw.grid(row=3,column=1, sticky=tk.E+tk.W+tk.S+tk.N)

        btn_ivcurve = tk.Button(self, text='IV-Curve', command=self.ivcurve)
        btn_ivcurve.grid(row=3,column=2, sticky=tk.E+tk.W+tk.S+tk.N)

        btn_readpvsetting = tk.Button(self, text='readpvsetting', command=self.readpvsetting)
        btn_readpvsetting.grid(row=3,column=3, sticky=tk.E+tk.W+tk.S+tk.N)
        
        btn_readpvcountryparm = tk.Button(self, text='readpvcountryparm', command=self.readpvcountryparm)
        btn_readpvcountryparm.grid(row=3,column=4, sticky=tk.E+tk.W+tk.S+tk.N)

        btn_readpvkwh = tk.Button(self, text='readpvkwh', command=self.readpvkwh)
        btn_readpvkwh.grid(row=5,column=0, sticky=tk.E+tk.W+tk.S+tk.N)


        btn_readautovoltageenable = tk.Button(self, text='readautovoltageenable', command=self.readautovoltageenable)
        btn_readautovoltageenable.grid(row=5,column=1, sticky=tk.E+tk.W+tk.S+tk.N)

        btn_readautovoltage = tk.Button(self, text='readautovoltage', command=self.readautovoltage)
        btn_readautovoltage.grid(row=5,column=2, sticky=tk.E+tk.W+tk.S+tk.N)

        btn_readpf = tk.Button(self, text='readpf', command=self.readpf)
        btn_readpf.grid(row=5,column=3, sticky=tk.E+tk.W+tk.S+tk.N)

        btn_readpoweroutput = tk.Button(self, text='readpoweroutput', command=self.readpoweroutput)
        btn_readpoweroutput.grid(row=5,column=4, sticky=tk.E+tk.W+tk.S+tk.N)

        tk.Button(self, text='reserve').grid(row=6, column=0, sticky=tk.E+tk.W)

        tk.Label(self, text='Command:', anchor=tk.W).grid(row=7, column=0, sticky=tk.E+tk.W)

        self.ddcentry = tk.Entry(self)
        self.ddcentry.grid(row=7, column=1, columnspan=3 , sticky=tk.W+tk.E)

        btn_send = tk.Button(self, text='Send', command=self.send)
        btn_send.grid(row=7, column=4, sticky=tk.E+tk.W)

        tk.Label(self, text='Result:', anchor=tk.W).grid(row=8, column=0, sticky=tk.E+tk.W)
        self.ddc_result_entry = tk.Entry(self)
        self.ddc_result_entry.grid(row=8, column=1, columnspan=4 , sticky=tk.W+tk.E)

        self.background = None


    def readpoweroutput(self):
        self.ddcentry.delete(0, tk.END)
        self.ddcentry.insert(0, 'readpoweroutput@0@1@0')

    def readpf(self):
        self.ddcentry.delete(0, tk.END)
        self.ddcentry.insert(0, 'readpf@0@1@0')

    def readautovoltage(self):
        self.ddcentry.delete(0, tk.END)
        self.ddcentry.insert(0, 'readautovoltage@0@1@0')

    def readautovoltageenable(self):
        self.ddcentry.delete(0, tk.END)
        self.ddcentry.insert(0, 'readautovoltageenable@0@1@0')

    def readpvkwh(self):
        self.ddcentry.delete(0, tk.END)
        self.ddcentry.insert(0, 'readpvkwh@0@1@0')

    def readpvsetting(self):
        self.ddcentry.delete(0, tk.END)
        self.ddcentry.insert(0, 'readpvsetting@0@1@0')

    def readpvcountryparm(self):
        self.ddcentry.delete(0, tk.END)
        self.ddcentry.insert(0, 'readpvcountryparm@0@1@0')

    def readpvsn(self):
        self.ddcentry.delete(0, tk.END)
        self.ddcentry.insert(0, 'readpvsn@0@1@0')

    def readpvfw(self):
        self.ddcentry.delete(0, tk.END)
        self.ddcentry.insert(0, 'readpvfw@0@1@0')

    def ivcurve(self):
        self.ddcentry.delete(0, tk.END)
        self.ddcentry.insert(0,'dumpjbus@0xC200,0xC57F,0x80,1,1,22@0@1@0')

    def send(self):
        self.ddc_result_entry.delete(0, tk.END)

        ddcstring = self.ddcentry.get()
        print('send {}'.format(ddcstring))
        self.send_command(ddcstring)

        self.ddc_result_entry.insert(0, 'waiting...')
        self.ddc_result_entry.after(5*1000, self.update_ddcr_entry)


    def update_ddcr_entry(self):
        if self.background:
            dr = None
            try:
                while not self.background.ddcq2.empty():
                    dr = self.background.ddcq2.get(timeout=3)
            except queue.Empty as ex:
                pass

            self.ddc_result_entry.delete(0, tk.END)
            self.ddc_result_entry.insert(0, str(dr))


    def send_command(self, ddcstring):
        command = duplex_factory.duplex_command_factory(ddcstring)
        if command: 
            if self.background:
                self.background.ddcq1.put(command)
        else:
            print('Not support this command')


class ConfigurationPage(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.configuration_text = tk.Text(self, height=15)
        self.configuration_text.pack(side='top', fill=tk.BOTH, expand=True)
        
        conf_string = os.popen('cat ./data/config.txt').read()

        self.configuration_text.delete(1.0, tk.END)
        self.configuration_text.insert(tk.INSERT, conf_string)

    def reload(self):
        print('reload')
        conf_string = os.popen('cat ./data/config.txt').read()

        self.configuration_text.delete(1.0, tk.END)
        self.configuration_text.insert(tk.INSERT, conf_string)

    def write(self):
        print('write configuration, not implement !')


class Application(tk.Frame):
    def __init__(self, master=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lock = threading.RLock()

        self.master.wm_title("Tk GUI")
        self.master.wm_geometry("800x480")
        self.pack(side="top", fill="both", expand=True)

        self.mpage      = MainPage(self)
        self.ipage      = InverterSummaryPage(self)
        self.meter_page = MeterPage(self)
        self.fpage      = FactoryPage(self)
        self.dpage      = DuplexPage(self)
        self.cpage      = ConfigurationPage(self)

        buttonframe = tk.Frame(self)
        container   = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        self.mpage.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        self.ipage.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        self.meter_page.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        self.fpage.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        self.dpage.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        self.cpage.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        btn = tk.Button(buttonframe, text='Main', command=self.mpage.lift)
        btn.pack(side='left')
        btn = tk.Button(buttonframe, text='Inverters', command=self.ipage.lift)
        btn.pack(side='left')
        btn = tk.Button(buttonframe, text='Meters', command=self.meter_page.lift)
        btn.pack(side='left')
        btn = tk.Button(buttonframe, text='Factory', command=self.fpage.lift)
        btn.pack(side='left')
        btn = tk.Button(buttonframe, text='Duplex', command=self.dpage.lift)
        btn.pack(side='left')
        btn = tk.Button(buttonframe, text='Configuration', command=self.cpage.lift)
        btn.pack(side='left')

        #self.mpage.show()
        self.mpage.lift()


    def bind(self, background):
        self.background = background
        self.dpage.background = self.background

    def update(self, subject, *args, **kwargs):
        with self.lock:
            try:
                if type(subject).__name__ == 'MainTask': 
                    msg = 'System time: {}'.format(datetime.datetime.now().replace(microsecond=0))
                    self.mpage.system_time.set(msg)

                    temp = os.popen('vcgencmd measure_temp').read().strip('\n')
                    temp = temp.split('=')[1]
                    msg = 'Temperature: {}'.format(temp)
                    self.mpage.temp.set(msg)

                    msg = 'Watchdog(c/r/u): {}/{}/{}'.format( round(subject.cwdt_diff),
                                                              round(subject.rwdt_diff),
                                                              round(subject.uwdt_diff))
                    self.mpage.watchdog.set(msg)

                elif isinstance(subject, collector.Collector):
                    if subject.polling_pv:
                        # rs485 tx message
                        s = ''
                        txpacket = subject.polling_pv.jbus.txpacket
                        if txpacket:
                            if len(txpacket) <= 8:
                                s = ' '.join(['{:02X}'.format(b) for b in txpacket])
                            else:
                                s = '{:02X} {:02X} {:02X} ... {:02X} {:02X}'.format(
                                    txpacket[0], 
                                    txpacket[1], 
                                    txpacket[2], 
                                    txpacket[-2], 
                                    txpacket[-1])
                        msg = 'RS485 Tx: {}'.format(s)
                        self.mpage.rs485tx.set(msg)

                        # rs485 rx message
                        s = ''
                        rxpacket = subject.polling_pv.jbus.rxpacket
                        if rxpacket:
                            if len(rxpacket) > 5:
                                s = '{:02X} {:02X} {:02X} ... {:02X} {:02X}'.format(rxpacket[0], 
                                                                                    rxpacket[1], 
                                                                                    rxpacket[2], 
                                                                                    rxpacket[-2], 
                                                                                    rxpacket[-1],)
                        msg = 'RS485 Rx: {}'.format(s)
                        self.mpage.rs485rx.set(msg)


                        # inverter page
                        pv = subject.polling_pv
                        msg = '{:<5}, {:>7}, {}, A:{:016X}, E:{:016X}, {:>6.2f}W, {:>6}KWH ({}/{})'.format( 
                            pv.name,
                            'online' if pv.online else 'offline',
                            time.strftime('%H:%M:%S', time.localtime(pv.last_update_timestamp)),
                            pv.alarm,
                            pv.error,
                            pv.OutputPower,
                            pv.TotalOutputPower,
                            pv.success_comm_counts,
                            pv.total_comm_counts)

                        self.ipage.inverter_stringvars[int(pv.id)].set(msg)
                        for lbl in self.ipage.inverter_labels.values():
                            lbl.config(fg='black')

                        self.ipage.inverter_labels[int(pv.id)].config(fg='red')

                        
                    if subject.imeter:
                        rec = subject.imeter.read(push_buffer=False)
                        #print('imeter: {}'.format(rec))
                        if rec: msg = '{:<12} {}'.format('Illu Record:', rec)
                        else:   msg = '{:<12} {}'.format('Illu Record:', 'None')
                        self.meter_page.illu_msg.set(msg)

                    if subject.tmeter:
                        rec = subject.tmeter.read(push_buffer=False)
                        if rec: msg = '{:<12} {}'.format('Temp Record:', rec)
                        else:   msg = '{:<12} {}'.format('Temp Record:', 'None')
                        self.meter_page.temp_msg.set(msg)

                    #msg = 'Status: {}'.format(subject.pvgroup.make_pvgroup_status_message())
                    msg = 'Status: {}'.format(subject.create_status_message_of_inverters())
                    self.mpage.status.set(msg)

                elif isinstance(subject, uploader.Uploader):
                    # upload message
                    msg = 'Upload(e/m/h): {}/{}/{}'.format( subject.event_post_response,
                                                            subject.minute_post_response,
                                                            subject.hour_post_response,)
                    self.mpage.upload_response.set(msg)

                    # server ip
                    self.server_ip_cache = subject.server_ip
                    msg = 'Server IP: {}'.format(subject.server_ip)
                    self.mpage.upload_server_ip.set(msg)

                    # psid
                    msg = 'PSID: {}'.format(subject.psid)
                    self.mpage.psid.set(msg)

                    # gwid
                    msg = 'GWID: {}'.format(subject.gwid)
                    self.mpage.gwid.set(msg)

                elif isinstance(subject, hearbeat.Hearbeat):
                    # server ip
                    msg = 'Hearbeat Server IP: {}'.format(subject.server_ip)
                    self.mpage.hearbeat_server_ip.set(msg)
                    
                    # send
                    active_datetime = datetime.datetime.fromtimestamp(subject.hearbeat_active_timestamp)
                    #msg = '{}: {}'.format(active_datetime, subject.hearbeat_message)
                    msg = '{:<11}: {} {}'.format('debug 9900', active_datetime, subject.hearbeat_message)
                    self.mpage.hearbeat_tx.set(msg)

                    # receive
                    received_datetime = datetime.datetime.fromtimestamp(subject.recieve_data_timestamp)
                    #msg = '{}: {}'.format(received_datetime, subject.recv_data)
                    msg = '{:<11}: {}: {}'.format('debug 9900', received_datetime, subject.recv_data)
                    self.mpage.hearbeat_rx.set(msg)

            except ValueError as ex:
                print('gui exception: {}'.format(repr(ex)))


if __name__ == "__main__":
    root = tk.Tk()
    main = Application(root)
    root.mainloop()
