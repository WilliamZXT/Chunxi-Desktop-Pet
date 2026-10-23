"""Real-time, local-only Qt endurance recorder. Never compress the clock."""
import ctypes
from ctypes import wintypes
from datetime import datetime,timezone
import json
from pathlib import Path
import time

from PySide6.QtCore import QObject,QTimer


class MEMORY(ctypes.Structure):
    _fields_=[('cb',wintypes.DWORD),('PageFaultCount',wintypes.DWORD)]+[(name,ctypes.c_size_t) for name in ('PeakWorkingSetSize','WorkingSetSize','QuotaPeakPagedPoolUsage','QuotaPagedPoolUsage','QuotaPeakNonPagedPoolUsage','QuotaNonPagedPoolUsage','PagefileUsage','PeakPagefileUsage','PrivateUsage')]


def process_metrics():
    kernel=ctypes.WinDLL('kernel32',use_last_error=True)
    kernel.GetCurrentProcess.restype=wintypes.HANDLE
    process=kernel.GetCurrentProcess()
    psapi=ctypes.WinDLL('psapi',use_last_error=True)
    psapi.GetProcessMemoryInfo.argtypes=[wintypes.HANDLE,ctypes.POINTER(MEMORY),wintypes.DWORD]
    info=MEMORY();info.cb=ctypes.sizeof(info)
    if not psapi.GetProcessMemoryInfo(process,ctypes.byref(info),info.cb):
        raise ctypes.WinError(ctypes.get_last_error())
    handles=wintypes.DWORD()
    kernel.GetProcessHandleCount.argtypes=[wintypes.HANDLE,ctypes.POINTER(wintypes.DWORD)]
    if not kernel.GetProcessHandleCount(process,ctypes.byref(handles)):
        raise ctypes.WinError(ctypes.get_last_error())
    user=ctypes.WinDLL('user32')
    user.GetGuiResources.argtypes=[wintypes.HANDLE,wintypes.DWORD]
    return {'working_set_bytes':info.WorkingSetSize,'private_bytes':info.PrivateUsage,'handles':handles.value,'gdi':user.GetGuiResources(process,0),'user':user.GetGuiResources(process,1),'cpu_seconds':time.process_time()}


class SoakRecorder(QObject):
    def __init__(self,window,seconds:float,output:Path):
        super().__init__(window)
        self.window,self.seconds,self.output=window,seconds,output
        self.started=time.monotonic();self.wall_started=datetime.now(timezone.utc).isoformat()
        self.samples=[];self.seen=set();self.actions=set();self.errors=[]
        self.last_tick=self.started;self.max_gap=0.;self.finished=False
        self.check_timer=QTimer(self);self.check_timer.setInterval(500)
        self.check_timer.timeout.connect(self.tick)
        self.sample_timer=QTimer(self);self.sample_timer.setInterval(60_000)
        self.sample_timer.timeout.connect(self.sample)
        self.sample();self.check_timer.start();self.sample_timer.start()
        window.destroyed.connect(lambda:self.finish(False))

    def tick(self):
        now=time.monotonic();self.max_gap=max(self.max_gap,now-self.last_tick);self.last_tick=now
        self.seen.add(self.window.machine.state.value)
        if self.window.machine.action:self.actions.add(self.window.machine.action)
        if now-self.started>=self.seconds:
            self.finish(True)
            self.window.close()

    def sample(self):
        try:self.samples.append({'elapsed_seconds':round(time.monotonic()-self.started,3),**process_metrics()})
        except Exception as error:self.errors.append(str(error))
        self.write('running')

    def write(self,status):
        elapsed=time.monotonic()-self.started
        growth=(self.samples[-1]['private_bytes']-self.samples[min(5,len(self.samples)-1)]['private_bytes']) if self.samples else 0
        enough=elapsed>=self.seconds and self.seconds>=7200
        report={'status':status,'started_utc':self.wall_started,'target_seconds':self.seconds,'actual_elapsed_seconds':round(elapsed,3),'real_time_clock':True,'time_acceleration':False,'state_injection':False,'states_observed':sorted(self.seen),'actions_observed':sorted(self.actions),'max_event_loop_gap_seconds':round(self.max_gap,3),'private_growth_after_warmup_bytes':growth,'errors':self.errors,'samples':self.samples,'long_run_gate_passed':status=='completed' and enough and self.max_gap<120 and not self.errors and growth<64*1024*1024}
        self.output.parent.mkdir(parents=True,exist_ok=True)
        temporary=self.output.with_suffix('.tmp')
        temporary.write_text(json.dumps(report,indent=2),encoding='utf-8');temporary.replace(self.output)

    def finish(self,completed:bool):
        if self.finished:return
        self.finished=True;self.check_timer.stop();self.sample_timer.stop()
        try:self.samples.append({'elapsed_seconds':round(time.monotonic()-self.started,3),**process_metrics()})
        except Exception as error:self.errors.append(str(error))
        self.write('completed' if completed else 'interrupted')
