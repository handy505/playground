#!/usr/bin/env python3
# -*- coding: utf-8 -*-
class MainTask(threading.Thread, observer.Observerable):
    def __init__(self):
        observer.Observerable.__init__(self)
        threading.Thread.__init__(self)
        self.looping = True

        self.initialize_gpio()

        self.check_files()

        self.check_hardware()

        self.configurations = self.read_configurations()
        print('Configuration: ----------------------')
        print(self.configurations)
        print('-------------------------------------')

        # Ablerex Inverters
        self.ablerex_inverters = pvinverter.create_ablerex_inverters(self.configurations)
        #self.ablerex_inverters = ablerex.create_ablerex_inverter_simulators(since=1, to=3)

        # KACO Inverters
        self.kaco_inverters = kaco.create_kaco_inverters(self.configurations)
        #self.kaco_inverters = kaco.create_kaco_inverter_simulators(since=4, to=10)

        # All inverters
        self.inverters = self.ablerex_inverters + self.kaco_inverters

        #print('Create Inverters:')
        [print('Create inverters: {}'.format(inv)) for inv in self.inverters]

        # Create Meters (Illumination/Termperature)
        self.imeter = meter_factory.create_illumination_meter(self.configurations)
        self.tmeter = meter_factory.create_temperature_meter(self.configurations)
        print('Create illuMeter: {}'.format(self.imeter))
        print('Create tempMeter: {}'.format(self.tmeter))


        #while True: time.sleep(3)


        # python use thread for block IO, not parallel calculate
        self.sta_que = queue.Queue(maxsize=1) # status queue, 2017/03 add 
        self.sque = queue.Queue(maxsize=1)

        # pipeline between collector and serverservice/bluetooth
        self.ddcq1 = queue.Queue()
        self.ddcq2 = queue.Queue()

        # queues
        cbus = Bus()
        ubus = Bus()
        fbus = Bus()

        # new queues
        cbus2 = BusDB()
        ubus2 = BusDB()
        fbus2 = BusDB()

        # collector thread 
        self.cthread = collector.Collector( illumeter=self.imeter,
                                            tempmeter=self.tmeter,
                                            outputbus=cbus,
                                            outputbus2=cbus2,
                                            sopp=self.sta_que,
                                            sopp2=self.sque,
                                            imm_importpp=self.ddcq1,
                                            imm_exportpp=self.ddcq2,
                                            kaco_inverters=self.kaco_inverters,
                                            ablerex_inverters=self.ablerex_inverters,
                                          )

        # concat thread
        self.concatthread = None
        if self.is_concat_mode(self.configurations):
            self.concatthread = concatenate.ConcatThread( imeter=self.imeter,
                                                          tmeter=self.tmeter,
                                                          inverters=self.ablerex_inverters)

        # recorder thread
        self.rthread = recorder.Recorder( inputbus=cbus,
                                          outputbus=ubus,
                                          feedbackbus=fbus,
                                          event_filepath=self.event_filepath,
                                          minute_filepath=self.minute_filepath,
                                          hour_filepath=self.hour_filepath,
                                          illu_filepath=self.illu_filepath,
                                          illu_hour_filepath=self.illu_hour_filepath, 
                                          temp_filepath=self.temp_filepath,
                                          temp_hour_filepath=self.temp_hour_filepath)


        #self.rthread2 = recorderdb.RecorderDB(cbus2, ubus2, fbus2)


        # uploader thread
        PV_SERVER_IP = '59.127.196.135'
        WIND_SERVER_IP = '61.216.58.146'
        self.uthread = uploader.Uploader( inputbus=ubus,
                                          outputbus=fbus,
                                          sipp=self.sta_que,
                                          server_ip=PV_SERVER_IP)

        #self.uthread2 = uploaderdb.Uploader(ubus2, fbus2, self.sque)

        # hearbeat thread, keep lone connection with server
        PV_HEARBEAT_SERVER_IP = '61.216.58.150'
        WIND_HEARBEAT_SERVER_IP = WIND_SERVER_IP
        self.hthread = hearbeat.Hearbeat(server_ip=PV_HEARBEAT_SERVER_IP, datasrc=self)


        # invoke external bluetooth stack
        os.system('sudo node ../aking/Bluetooth5/NodeBle/index.js &')

        # bluetooth BLE, for iOS
        self.bt8001_thread = btclient.BTClient(port=8001, data_source=self)
        self.bluetooth_access_time = 0


        # toggle wdt at startup
        GPIO.output(WDT_PIN, not GPIO.input(WDT_PIN))
        self.clear_wdt_timestamp = time.time() 

        self.ftdi_exist = True

        # fan control
        self.pwm = GPIO.PWM(FAN_CONTROL, 100)
        self.pwm.start(0)
        self.fan_control_timestamp = time.time()

        # bluetooth control
        self.bluetooth_access_time = 0


    def initialize_gpio(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(RS485_LED_PIN, GPIO.OUT)
        GPIO.setup(ERROR_LED_PIN, GPIO.OUT)
        GPIO.setup(ERROR_LED_555_PIN, GPIO.OUT)
        GPIO.setup(NETWORK_LED_PIN, GPIO.OUT)
        GPIO.setup(DRY_OUTPUT_A_PIN, GPIO.OUT)
        GPIO.setup(DRY_OUTPUT_B_PIN, GPIO.OUT)
        GPIO.setup(DRY_OUTPUT_C_PIN, GPIO.OUT)
        GPIO.setup(WDT_PIN, GPIO.OUT)
        GPIO.setup(FAN_CONTROL, GPIO.OUT)

        GPIO.setup(DRY_INPUT_A_PIN, GPIO.IN)
        GPIO.setup(DRY_INPUT_B_PIN, GPIO.IN)

        # gpio init stat
        GPIO.output(ERROR_LED_555_PIN, GPIO.HIGH)
        GPIO.output(RS485_LED_PIN, GPIO.HIGH)
        GPIO.output(ERROR_LED_PIN, GPIO.HIGH)
        GPIO.output(NETWORK_LED_PIN, GPIO.HIGH)
        GPIO.output(FAN_CONTROL, GPIO.HIGH)

    def is_concat_mode(self, configurations):
        lines = configurations.splitlines()
        for line in lines:
            if line.startswith('concat=1'):
                return True
        return False


    def bind(self, gui=None):
        self.gui = gui


    def fan_control(self):
        try:
            temp = os.popen('vcgencmd measure_temp').read().strip('\n')
            temp = temp.split('=')[1]
            temp = temp[:-2]
            temp = int(float(temp))
            if temp > 75:
                self.pwm.ChangeDutyCycle(100)
            elif temp > 60:
                self.pwm.ChangeDutyCycle(50)
            else:
                self.pwm.ChangeDutyCycle(0)

        except Exception as ex:
            print('Exception in fan control(): {}'.format(repr(ex)))


    def run(self):
        print('Main thread is running...')

        # observer pattern
        for observer in self.observers:
            self.cthread.attach(observer)
        for observer in self.observers:
            self.rthread.attach(observer)
        for observer in self.observers:
            self.uthread.attach(observer)
        for observer in self.observers:
            self.hthread.attach(observer)
        for observer in self.observers:
            self.bt8001_thread.attach(observer)

        # start sub-threads
        self.cthread.start()       
        if self.concatthread: 
            self.concatthread.start()
        self.rthread.start()
        self.uthread.start()
        self.hthread.start()
        self.bt8001_thread.start()

        # another path
        #self.rthread2.start()
        #self.uthread2.start()

        while self.looping:

            # fan control
            if time.time() - self.fan_control_timestamp > 10:
                self.fan_control()
                self.fan_control_timestamp = time.time()

            # led
            '''if self.is_collector_hearlth(): GPIO.output(RS485_LED_PIN, GPIO.LOW)
            else:                           GPIO.output(RS485_LED_PIN, GPIO.HIGH)

            if self.is_recorder_hearlth():  GPIO.output(ERROR_LED_PIN, GPIO.LOW)
            else:                           GPIO.output(ERROR_LED_PIN, GPIO.HIGH)

            if self.is_hearbeat_hearlth():  GPIO.output(NETWORK_LED_PIN, GPIO.LOW)
            else:                           GPIO.output(NETWORK_LED_PIN, GPIO.HIGH)
            '''
            if self.is_collector_hearlth(): self.turn_off_rs485_led()
            else:                           self.turn_on_rs485_led()

            if self.is_recorder_hearlth():  self.turn_off_error_led()
            else:                           self.turn_on_error_led()

            if self.is_hearbeat_hearlth():  self.turn_off_network_led()
            else:                           self.turn_on_network_led()


            # watchdog tick condition
            if self.cthread.high_priority_command_executing:
                # for inverter programming and iv-curve processing (2018-09-17)
                GPIO.output(WDT_PIN, not GPIO.input(WDT_PIN))
                self.clear_wdt_timestamp = time.time()
            else:
                cwatchdog = self.is_collector_watchdog_checked()
                rwatchdog = self.is_recorder_watchdog_checked()
                uwatchdog = self.is_uploader_watchdog_checked()
                if cwatchdog and rwatchdog and uwatchdog:
                    GPIO.output(WDT_PIN, not GPIO.input(WDT_PIN))
                    self.clear_wdt_timestamp = time.time()
                
            # watchdog issue, soft reset before hardware reset, avoid file broken.
            #if time.time() - self.clear_wdt_timestamp > (60 * 2):
            diff = time.time() - self.clear_wdt_timestamp 
            if (60*60) > diff > (60*2):
                msg = 'soft wdt reboot at {} (c:{}, r:{}, u:{})'.format(
                    datetime.datetime.now().replace(microsecond=0), 
                    round(self.cwdt_diff,3),
                    round(self.rwdt_diff,3),
                    round(self.uwdt_diff,3))
                cmd = 'echo "{}" >> reboot.log'.format(msg)
                os.system(cmd)
                os.system('reboot')

            # ftdi
            if not self.is_ftdi_exist():
                msg = 'ftdi disconnect reboot at {}'.format(datetime.datetime.now().replace(microsecond=0))
                cmd = 'echo "{}" >> reboot.log'.format(msg)
                os.system(cmd)
                os.system('reboot')

            # bluetooth issue, violence solution
            # reboot system after bleutooth connect, WHAT THE FUCK !!!
            if self.bluetooth_access_time != 0:
                bluetimediff = time.time() - self.bluetooth_access_time
                if bluetimediff > (3*60):
                    msg = 'bluetooth-linked reboot at {}'.format(datetime.datetime.now().replace(microsecond=0))
                    cmd = 'echo "{}" >> reboot.log'.format(msg)
                    os.system(cmd)
                    os.system('reboot')

            self.notify()
            time.sleep(1)

        # close sub-threads
        print('close sub threads')

        self.cthread.looping = False 
        self.cthread.join()
        print('collector thread join')
        self.notify()

        if self.concatthread:
            self.concatthread.looping = False
            self.concatthread.join()
            print('concat thread join')
        
        self.rthread.looping = False 
        self.rthread.join()
        self.notify()
        
        self.uthread.looping = False 
        self.uthread.join()
        self.notify()
        
        self.hthread.looping = False 
        self.hthread.join()
        self.notify()

        # close gui
        if self.gui: 
            self.gui.close()

        GPIO.cleanup()


    def is_ftdi_exist(self):
        cmd = 'ls /dev/ttyUSB*'
        ret = os.popen(cmd).read()
        devs = ret.split('\n')
        if devs[0] == '/dev/ttyUSB0' and devs[1] == '/dev/ttyUSB1':
            return True
        else:
            return False

    def is_collector_hearlth(self):
        return self.cthread.hearlth

    def is_recorder_hearlth(self):
        return self.is_recorder_watchdog_checked()

    def is_uploader_hearlth(self):
        return self.uthread.network_hearlth

    def is_hearbeat_hearlth(self):
        #return self.hthread.connected
        '''result = self.hthread.connected
        print('debug hearbeat connected: {} at {}'.format(result, datetime.datetime.now()))
        return result'''

        diff = time.time() - self.hthread.recieve_data_timestamp 
        #print('debug hearbeat diff: {}'.format(diff))
        if diff < (60*5):   return True
        else:               return False


    def is_collector_watchdog_checked(self):
        self.cwdt_diff = time.time() - self.cthread.watchdog_checked_timestamp
        return True if self.cwdt_diff < (3*60) else False

    def is_recorder_watchdog_checked(self):
        self.rwdt_diff = time.time() - self.rthread.watchdog_checked_timestamp
        return True if self.rwdt_diff < (3*60) else False

    def is_uploader_watchdog_checked(self):
        self.uwdt_diff = time.time() - self.uthread.watchdog_checked_timestamp
        return True if self.uwdt_diff < (6*60) else False

    def generate_default_configuration(self):
        os.system('touch {}'.format(self.CONFIGURATION_FILEPATH))
        try:
            lines = []
            lines.append('pv=')
            lines.append('concat=0')
            lines.append('illu-dcbox=')
            lines.append('temp-dcbox=')
            with open(self.CONFIGURATION_FILEPATH, 'w', encoding='utf-8') as fw:
                fw.writelines(['{}\n'.format(line) for line in lines])
        except Exception as ex:
            print(repr(ex))


    def check_files(self):
        # check path exist
        self.data_path = './data'
        if not os.path.exists(self.data_path):
            print('Enviroment check: ./data not exist, fix it')
            os.system('mkdir {}'.format(self.data_path) )

        self.CONFIGURATION_FILEPATH = './data/config.txt'
        if not os.path.exists(self.CONFIGURATION_FILEPATH):
            print('Enviroment check: ./data/config.txt not exist, fix it')
            self.generate_default_configuration()

        cmd = "file ./data/config.txt | awk {'print $2'}"
        is_empty_file = (os.popen(cmd).read().strip() == 'empty')
        if is_empty_file:
            print('Enviroment check: ./data/config.txt is empty, fix it')
            self.generate_default_configuration()

        self.event_filepath = './data/event.txt'
        if not os.path.exists(self.event_filepath):
            print('Enviroment check: ./data/event.txt not exist, fix it')
            os.system('touch {}'.format(self.event_filepath))

        self.minute_filepath = './data/minute.txt'
        if not os.path.exists(self.minute_filepath): 
            print('Enviroment check: ./data/minite.txt not exist, fix it')
            os.system('touch {}'.format(self.minute_filepath))
        
        self.hour_filepath = './data/hour.txt'
        if not os.path.exists(self.hour_filepath): 
            print('Enviroment check: ./data/hour.txt not exist, fix it')
            os.system('touch {}'.format(self.hour_filepath))
            
        self.illu_filepath = './data/illu.txt'
        if not os.path.exists(self.illu_filepath ): 
            print('Enviroment check: ./data/illu.txt not exist, fix it')
            os.system('touch {}'.format(self.illu_filepath))

        self.illu_hour_filepath = './data/illuhour.txt'
        if not os.path.exists(self.illu_hour_filepath ): 
            print('Enviroment check: ./data/illuhour.txt not exist, fix it')
            os.system('touch {}'.format(self.illu_hour_filepath))

        self.temp_filepath = './data/temp.txt'
        if not os.path.exists(self.temp_filepath ): 
            print('Enviroment check: ./data/temp.txt not exist, fix it')
            os.system('touch {}'.format(self.temp_filepath))

        self.temp_hour_filepath = './data/temphour.txt'
        if not os.path.exists(self.temp_hour_filepath ): 
            print('Enviroment check: ./data/temphour.txt not exist, fix it')
            os.system('touch {}'.format(self.temp_hour_filepath))


    def check_hardware(self):
        # Check Hardware FTDI Serial Port Exist
        try:
            ser0 = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, timeout=0.8)
        except OSError as ex:
            print('Exception: Fail to get /dev/ttyUSB0:{}'.format(repr(ex)))
            sys.exit()


    def read_configurations(self):
        # Load configurations
        p = subprocess.Popen(['cat', './data/config.txt'], stdout=subprocess.PIPE)
        out, err = p.communicate()
        result = out.decode('utf-8')
        return result


    def turn_off_relay_a(self): GPIO.output(DRY_OUTPUT_A_PIN, GPIO.LOW)
    def turn_on_ralay_a(self):  GPIO.output(DRY_OUTPUT_A_PIN, GPIO.HIGH)
        
    def turn_off_relay_b(self): GPIO.output(DRY_OUTPUT_B_PIN, GPIO.LOW)
    def turn_on_ralay_b(self):  GPIO.output(DRY_OUTPUT_B_PIN, GPIO.HIGH)

    def turn_off_relay_c(self): GPIO.output(DRY_OUTPUT_C_PIN, GPIO.LOW)
    def turn_on_ralay_c(self):  GPIO.output(DRY_OUTPUT_C_PIN, GPIO.HIGH) 

    def turn_off_rs485_led(self):   GPIO.output(RS485_LED_PIN, GPIO.LOW)
    def turn_on_rs485_led(self):    GPIO.output(RS485_LED_PIN, GPIO.HIGH)

    def turn_off_error_led(self):   GPIO.output(ERROR_LED_PIN, GPIO.LOW)
    def turn_on_error_led(self):    GPIO.output(ERROR_LED_PIN, GPIO.HIGH)

    def turn_off_network_led(self): GPIO.output(NETWORK_LED_PIN, GPIO.LOW)
    def turn_on_network_led(self):  GPIO.output(NETWORK_LED_PIN, GPIO.HIGH)


def main():
    parser = optparse.OptionParser()
    parser.add_option(
        '-c', '--console',
        action='store_true',
        dest='consolemode',
        help='console mode')
    opts, args = parser.parse_args()


    if opts.consolemode:
        print('Run in CONSOLE mode')
        mainthread = MainTask()
        mainthread.start()
        sys.exit()
    else:
        print('Run with TK GUI')
        import tkinter as tk
        import tkgui
        root = tk.Tk()
        app = tkgui.Application(master=root)

        mainthread = MainTask()
        mainthread.attach(app)
        mainthread.start()

        app.bind(mainthread)
        app.mainloop()

if __name__ == "__main__":
    main()
