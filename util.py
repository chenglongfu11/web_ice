import ctypes
import json
import time
from win32 import win32process
import sys
import os
import config


# path_to_ice = "D:\\Program Files (x86)\\ice48_Beta15(tmp)\\bin\\"
# path_to_ice = "D:\\ida\\bin\\"
# path_to_ice = "C:\\Program Files (x86)\\IDA\\bin\\"
path_to_ice = config.APP_PATH
command = path_to_ice + "ida-ice.exe \"" + path_to_ice + "ida.img\" -G 1"
startObj = win32process.STARTUPINFO()
ret = win32process.CreateProcess(None,command,None,None,0,0,None,None,startObj)
pid = str(ret[2])
# print(pid)
time.sleep(5)
#Add path_to_ice to PATH variable, is removed when program finishes
os.environ['PATH'] = path_to_ice + os.pathsep + os.environ['PATH']

ida_lib = ctypes.CDLL(path_to_ice + 'idaapi2.dll')


ida_lib.connect_to_ida.restype = ctypes.c_bool
ida_lib.connect_to_ida.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
ida_lib.switch_remote_connection.restype = ctypes.c_bool
ida_lib.switch_remote_connection.argtypes = [ctypes.c_char_p]
ida_lib.switch_api_version.restype = ctypes.c_bool
ida_lib.switch_api_version.argtypes = [ctypes.c_long]
ida_lib.call_ida_function.restype = ctypes.c_long
ida_lib.call_ida_function.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
ida_lib.ida_disconnect.restype = ctypes.c_bool
ida_lib.ida_disconnect.argtypes = []
ida_lib.get_err.restype = ctypes.c_long
ida_lib.get_err.argtypes = [ctypes.c_char_p, ctypes.c_int]
ida_lib.childNodes.restype = ctypes.c_long
ida_lib.childNodes.argtypes = [ctypes.c_long, ctypes.c_char_p, ctypes.c_int]
ida_lib.parentNode.restype = ctypes.c_long
ida_lib.parentNode.argtypes = [ctypes.c_long, ctypes.c_char_p, ctypes.c_int]
ida_lib.setParentNode.restype = ctypes.c_long
ida_lib.setParentNode.argtypes = [ctypes.c_long, ctypes.c_long, ctypes.c_char_p, ctypes.c_int]
ida_lib.hasChildNodes.restype = ctypes.c_long
ida_lib.hasChildNodes.argtypes = [ctypes.c_long, ctypes.c_char_p, ctypes.c_int]
ida_lib.firstChild.restype = ctypes.c_long
ida_lib.firstChild.argtypes = [ctypes.c_long, ctypes.c_char_p, ctypes.c_int]
ida_lib.lastChild.restype = ctypes.c_long
ida_lib.lastChild.argtypes = [ctypes.c_long, ctypes.c_char_p, ctypes.c_int]
ida_lib.nextSibling.restype = ctypes.c_long
ida_lib.nextSibling.argtypes = [ctypes.c_long, ctypes.c_char_p, ctypes.c_int]
ida_lib.previousSibling.restype = ctypes.c_long
ida_lib.previousSibling.argtypes = [ctypes.c_long, ctypes.c_char_p, ctypes.c_int]
ida_lib.childNodesLength.restype = ctypes.c_long
ida_lib.childNodesLength.argtypes = [ctypes.c_long, ctypes.c_char_p, ctypes.c_int]
ida_lib.setNodeValue.restype = ctypes.c_long
ida_lib.setNodeValue.argtypes = [ctypes.c_long, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
ida_lib.cloneNode.restype = ctypes.c_long
ida_lib.cloneNode.argtypes = [ctypes.c_long, ctypes.c_char_p, ctypes.c_int]
ida_lib.insertBefore.restype = ctypes.c_long
ida_lib.insertBefore.argtypes = [ctypes.c_long, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
ida_lib.createNode.restype = ctypes.c_long
ida_lib.createNode.argtypes = [ctypes.c_long, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
ida_lib.contains.restype = ctypes.c_long
ida_lib.contains.argtypes = [ctypes.c_long, ctypes.c_long, ctypes.c_char_p, ctypes.c_int]
ida_lib.domAncestor.restype = ctypes.c_long
ida_lib.domAncestor.argtypes = [ctypes.c_long, ctypes.c_long, ctypes.c_char_p, ctypes.c_int]
ida_lib.item.restype = ctypes.c_long
ida_lib.item.argtypes = [ctypes.c_long, ctypes.c_long, ctypes.c_char_p, ctypes.c_int]
ida_lib.appendChild.restype = ctypes.c_long
ida_lib.appendChild.argtypes = [ctypes.c_long, ctypes.c_long, ctypes.c_char_p, ctypes.c_int]
ida_lib.removeChild.restype = ctypes.c_long
ida_lib.removeChild.argtypes = [ctypes.c_long, ctypes.c_long, ctypes.c_char_p, ctypes.c_int]
ida_lib.replaceChild.restype = ctypes.c_long
ida_lib.replaceChild.argtypes = [ctypes.c_long, ctypes.c_long, ctypes.c_char_p, ctypes.c_int]
ida_lib.setAttribute.restype = ctypes.c_long
ida_lib.setAttribute.argtypes = [ctypes.c_char_p, ctypes.c_long, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
ida_lib.getAttribute.restype = ctypes.c_long
ida_lib.getAttribute.argtypes = [ctypes.c_char_p, ctypes.c_long, ctypes.c_char_p, ctypes.c_int]
ida_lib.openDocument.restype = ctypes.c_long
ida_lib.openDocument.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
ida_lib.openDocByTypeAndName.restype = ctypes.c_long
ida_lib.openDocByTypeAndName.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
ida_lib.saveDocument.restype = ctypes.c_long
ida_lib.saveDocument.argtypes = [ctypes.c_long, ctypes.c_char_p, ctypes.c_long, ctypes.c_char_p, ctypes.c_int]
ida_lib.runSimulation.restype = ctypes.c_long
ida_lib.runSimulation.argtypes = [ctypes.c_long, ctypes.c_long, ctypes.c_char_p, ctypes.c_int]
ida_lib.pollForQueuedResults.restype = ctypes.c_long
ida_lib.pollForQueuedResults.argtypes = [ctypes.c_char_p, ctypes.c_int]
ida_lib.getZones.restype = ctypes.c_long
ida_lib.getZones.argtypes = [ctypes.c_long, ctypes.c_char_p, ctypes.c_int]
ida_lib.getWindows.restype = ctypes.c_long
ida_lib.getWindows.argtypes = [ctypes.c_long, ctypes.c_char_p, ctypes.c_int]
ida_lib.getChildrenOfType.restype = ctypes.c_long
ida_lib.getChildrenOfType.argtypes = [ctypes.c_long, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
ida_lib.findNamedChild.restype = ctypes.c_long
ida_lib.findNamedChild.argtypes = [ctypes.c_long, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
ida_lib.exitSession.restype = ctypes.c_long
ida_lib.exitSession.argtypes = [ctypes.c_char_p, ctypes.c_int]
ida_lib.getAllSubobjectsOfType.restype = ctypes.c_long
ida_lib.getAllSubobjectsOfType.argtypes = [ctypes.c_long, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
ida_lib.runIDAScript.restype = ctypes.c_long
ida_lib.runIDAScript.argtypes = [ctypes.c_long, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
ida_lib.copyObject.restype = ctypes.c_long
ida_lib.copyObject.argtypes = [ctypes.c_long, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
ida_lib.findObjectsByCriterium.restype = ctypes.c_long
ida_lib.findObjectsByCriterium.argtypes = [ctypes.c_long, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
ida_lib.findUseOfResource.restype = ctypes.c_long
ida_lib.findUseOfResource.argtypes = [ctypes.c_long, ctypes.c_char_p, ctypes.c_int]
ida_lib.printReport.restype = ctypes.c_long
ida_lib.printReport.argtypes = [ctypes.c_long, ctypes.c_char_p, ctypes.c_long, ctypes.c_char_p, ctypes.c_int]




#Utility functions

def ida_poll_results_queue (time_interval):
  size = 5000
  doc_str = ctypes.create_string_buffer(size)
  poll_result = False
  while poll_result == False:
    time.sleep(time_interval)
    poll_res = ida_lib.pollForQueuedResults(doc_str, len(doc_str))
    poll_result2 = json.loads(doc_str.value.decode("utf-8"))
    if isinstance(poll_result2, list):
      poll_result = poll_result2[0]['value']
    else:
      return ""
  return poll_result2[1]['value']

def call_ida_api_function (fun, *args):
  "Just send in the function name and its unique arguments (not out buffer and out buffer length)"
  p = ctypes.create_string_buffer(5000)
  args = args + (p,len(p))
  res = fun(*args)
  if res == 0:
    return ida_poll_results_queue(0.1)
  elif res > 0 :
    p = ctypes.create_string_buffer(res)
    res = fun(*args)
    if res == 0:
      return ida_poll_results_queue(0.1)
    else:
      return ""
  else:
      res2 = ida_lib.get_err(p,len(p))
      return p.value.decode("utf-8")

def call_ida_api_function_j (fun, *args):
  "Just send in the function name and its unique arguments (not out buffer and out buffer length)"
  p = ctypes.create_string_buffer(5000)
  args = args + (p,len(p))
  res = fun(*args)
  if res == 0:
    return p
  else:
    p = ctypes.create_string_buffer(res)
    res = fun(*args)
    if res == 0:
      return p
    else:
      return ""



def ida_poll_results_queue_j (time_interval):
  size = 5000
  doc_str = ctypes.create_string_buffer(size)
  poll_result = False
  while poll_result == False:
    time.sleep(time_interval)
    poll_res = ida_lib.pollForQueuedResults(doc_str, len(doc_str))
    poll_result2 = json.loads(doc_str.value.decode("utf-8"))
    if isinstance(poll_result2, list):
      poll_result = poll_result2[0]['value']
    else:
      return ""
  return json.dumps(poll_result2[1])

def ida_get_named_child(par,name):
  site_res = call_ida_api_function(ida_lib.findNamedChild, par, name.encode())
  return site_res

def ida_get_value(par):
  val = call_ida_api_function(ida_lib.getAttribute,b"VALUE", par)
  return val

def ida_get_name(par):
  val = call_ida_api_function(ida_lib.getAttribute,b"NAME", par)
  return val

def ida_checkerr():
  p = ctypes.create_string_buffer(5000)
  err_p = ida_lib.get_err(p,len(p))
  print("the error is "+p.value.decode("utf-8"))

def ida_checkstatus():
  p = ctypes.create_string_buffer(5000)
  status = ida_lib.getIDAStatus(p, len(p))
  print("the IDA status is " +p.value.decode("utf-8"))