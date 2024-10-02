import socketio

sio = socketio.Client()

pc = 'some_pc_id'

@sio.event
def connect():
    print('Connection established!')

@sio.event
def disconnect():
    print('Disconnected from server')

@sio.event
def connect_error(data):
    print('Connection error:', data)

def send_screenshot(image_data):
    sio.emit('screenshot', {'image': image_data, 'pc': pc})

sio.connect('http://localhost:5000/test', namespaces=['/test'], queries={'pc': pc})

# 假设有一个函数capture_screenshot()用于捕获屏幕截图
# while True:
#     image_data = capture_screenshot()
#     send_screenshot(image_data)

# 保持连接
try:
    while True:
        sio.wait()
except KeyboardInterrupt:
    print('Disconnected by user')
