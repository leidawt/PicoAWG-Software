import serial
import serial.tools.list_ports
import time
from math import pi, sin, exp, sqrt, floor
from random import random
# from scipy import signal
from tinynumpy import tinynumpy as np


class Pico:
    def __init__(self):
        self.devices = []
        self.pico_device = ""
        self.ser = None

    def list_ports(self):
        devices = []
        pico_device = ""
        for p in list(serial.tools.list_ports.comports()):
            devices.append(p.device)
            # https://github.com/raspberrypi/usb-pid
            # Vendor-ID = 0x2E8A Product-ID	= 0x0005
            if p.vid == 0x2E8A and p.pid == 0x0005:
                pico_device = p.device
        self.devices = devices
        self.pico_device = pico_device
        return devices, pico_device

    def is_open(self):
        if self.ser is not None:
            if self.ser.isOpen():
                return True
            else:
                return False
        else:
            return False

    def connect(self, device):
        self.ser = serial.Serial(
            port=device,
            baudrate=115200,
            parity=serial.PARITY_ODD,
            stopbits=serial.STOPBITS_TWO,
            bytesize=serial.SEVENBITS
        )

    def disconnect(self):
        if self.ser is not None:
            self.ser.close()

    def send_command(self, command):
        if self.ser is not None:
            if self.ser.isOpen():
                command = command + '\r\n'
                self.ser.write(command.encode('utf-8'))
                print("send: {}".format(command))

    def reset(self):
        self.send_command("machine.reset()")
        time.sleep(3)
        for _ in range(10):  # try 10 times
            time.sleep(1)
            # reconnect serial
            try:
                self.connect(self.pico_device)
                print("connected")
                break
            except:
                print("retry...")

    def set_wave(self, wave_type, wave_args, arb_data=None):
        if wave_type == "Sine":
            command = f"wave1.func = sine;wave1.amplitude = {wave_args['amplitude']};wave1.offset = {wave_args['offset']};wave1.pars = [];setupwave(wavbuf[ibuf], {wave_args['freq']}, wave1);ibuf = (ibuf+1) % 2"
        elif wave_type == "Pulse":
            command = f"wave1.func = pulse;wave1.amplitude = {wave_args['amplitude']};wave1.offset = {wave_args['offset']};wave1.pars = [{wave_args['risetime']},{wave_args['uptime']},{wave_args['falltime']}];setupwave(wavbuf[ibuf], {wave_args['freq']}, wave1);ibuf = (ibuf+1) % 2"
        elif wave_type == "Noise":
            command = f"wave1.func = noise;wave1.amplitude = {wave_args['amplitude']};wave1.offset = {wave_args['offset']};wave1.pars = [{wave_args['quality']}];setupwave(wavbuf[ibuf], {wave_args['freq']}, wave1);ibuf = (ibuf+1) % 2"
        elif wave_type == "Sinc":
            command = f"wave1.func = sinc;wave1.amplitude = {wave_args['amplitude']};wave1.offset = {wave_args['offset']};wave1.pars = [{wave_args['width']}];setupwave(wavbuf[ibuf], {wave_args['freq']}, wave1);ibuf = (ibuf+1) % 2"
        elif wave_type == "Arb":
            # send arb data first
            self.send_arb_lut(arb_data, wave_args)
            command = f"wave1.func = None;wave1.amplitude = {wave_args['amplitude']};wave1.offset = {wave_args['offset']};wave1.pars = [];setupwave(wavbuf[ibuf], {wave_args['freq']}, wave1);ibuf = (ibuf+1) % 2"
        else:
            return

        self.send_command(command)

    def get_sample_rate(self, f):
        dac_clock = 125000000
        maxnsamp = 4096
        f = float(f)
        div = dac_clock/(f*maxnsamp)
        if div < 1.0:
            clkdiv = 1
        else:
            clkdiv = int(div)+1
        return dac_clock/clkdiv

    def send_arb_lut(self, arb_data, wave_args):
        dac_clock = 125000000
        maxnsamp = 4096
        f = float(wave_args['freq'])
        amplitude = float(wave_args['amplitude'])
        offset = float(wave_args['offset'])
        # calculate nsamp, amplitude, offset
        div = dac_clock/(f*maxnsamp)
        if div < 1.0:  # can't speed up clock, duplicate wave instead
            dup = int(1.0/div)
            nsamp = int((maxnsamp*div*dup+0.5)/4)*4  # force multiple of 4
            clkdiv = 1
        else:  # stick with integer clock division only
            clkdiv = int(div)+1
            nsamp = int((maxnsamp*div/clkdiv+0.5)/4)*4  # force multiple of 4
            dup = 1

        # gain set
        if amplitude >= 2:
            amplitude = 0.5
            offset = 0
        elif amplitude <= 0.2:
            if offset == 0:
                amplitude = amplitude/0.2*0.5
            else:
                amplitude = amplitude/2*0.5
                offset = offset/2
        else:
            k = 1-offset/amplitude
            amplitude = 0.5*k
            offset = 0.5-0.5*k

        # handle arb_data
        # resample to nsamp points
        # arb_data = signal.resample(arb_data, nsamp)
        arb_data = self._resample(arb_data, nsamp)
        # norm to [-1, 1]
        arb_data = (arb_data-arb_data.min()) / \
            (arb_data.max()-arb_data.min())*2-1

        # calculate lut table
        buf = bytearray(nsamp*2)
        for iword in range(int(nsamp/2)):
            # v = v*w.amplitude*m
            # v = v+w.offset+s
            val1 = int(
                16383*(arb_data[(dup*(iword*2+0)) % nsamp]*amplitude+offset))+8192
            val2 = int(
                16383*(arb_data[(dup*(iword*2+1)) % nsamp]*amplitude+offset))+8192

            word = val1 + (val2 << 14)
            buf[iword*4+0] = (word & (255 << 0)) >> 0
            buf[iword*4+1] = (word & (255 << 8)) >> 8
            buf[iword*4+2] = (word & (255 << 16)) >> 16
            buf[iword*4+3] = (word & (255 << 24)) >> 24

        # 分组发出
        group_size = 256
        num_groups = (nsamp*2) // group_size
        remaining_samples = (nsamp*2) % group_size
        r = [group_size for _ in range(num_groups)]
        if remaining_samples > 0:
            r.append(remaining_samples)

        st = 0
        for n in r:
            command = "temp=bytearray(("
            for d in buf[st:(st+n)]:
                command += "{:d},".format(d)
            command += "))"
            # print(command)
            self.send_command(command)
            self._wait_exec_done()
            self.send_command("data_mov({}, {})".format(st, n))
            self._wait_exec_done()
            st += n

    def get_preview_data(self, wave_type, wave_args, arb_data=None):
        n_points = 200
        if wave_type == "Sine":
            pars = []
            return [self._sine(x/n_points, pars) for x in range(n_points)]
        elif wave_type == "Pulse":
            pars = [wave_args["risetime"],
                    wave_args["uptime"], wave_args["falltime"]]
            pars = [float(each) for each in pars]
            return [self._pulse(x/n_points, pars) for x in range(n_points)]
        elif wave_type == "Noise":
            pars = [wave_args["quality"]]
            return [self._noise(x/n_points, pars) for x in range(n_points)]

        elif wave_type == "Sinc":
            pars = [float(wave_args["width"])]
            return [self._sinc(x/n_points, pars) for x in range(n_points)]

        elif wave_type == "Arb":
            return self._resample(arb_data, 100)

        else:
            return []

    def _sine(self, x, pars):
        return sin(x*2*pi)

    def _pulse(self, x, pars):  # risetime,uptime,falltime
        if x < pars[0]:
            return x/pars[0]
        if x < pars[0]+pars[1]:
            return 1.0
        if x < pars[0]+pars[1]+pars[2]:
            return 1.0-(x-pars[0]-pars[1])/pars[2]
        return 0.0

    def _gaussian(self, x, pars):
        return exp(-((x-0.5)/pars[0])**2)

    def _sinc(self, x, pars):
        if x == 0.5:
            return 1.0
        else:
            return sin((x-0.5)/pars[0])/((x-0.5)/pars[0])

    def _exponential(self, x, pars):
        return exp(-x/pars[0])

    def _noise(self, x, pars):  # p0=quality: 1=uniform >10=gaussian
        return sum([random()-0.5 for _ in range(pars[0])])*sqrt(12/pars[0])

    def _wait_exec_done(self):
        while True:
            # 读取一个字节
            byte_data = self.ser.read(1)

            # 判断是否接收到指定的字节序列
            if byte_data == b'\x3E':
                # 接收到第一个字节
                if self.ser.read(3) == b'\x3E\x3E\x20':
                    # print("接收到指定字节序列")
                    break

    def _resample(self, arb_data, nsamp):
        # resample nsamp points
        len_arb_data = len(arb_data)
        step = len_arb_data / nsamp
        return np.array([arb_data[min(floor(i*step), len_arb_data)] for i in range(nsamp)])


if __name__ == '__main__':
    pico = Pico()
    pico.list_ports()
    pico.connect(pico.pico_device)
    # pico.set_wave
