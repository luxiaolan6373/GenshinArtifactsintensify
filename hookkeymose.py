from pynput import keyboard
from pynput import mouse

class HookKeyMose:

    def __init__(self,hookMouse=False,hookKey=True):
        '''
        可通过集成本类  然后重写on_函数来实现hook回返
        '''



        if hookMouse==True:
            self.listen_mouse_nblock()
        if hookKey==True:
            self.listen_key_nblock()

    def on_press(self,key):

        """定义按下时候的响应，参数传入key"""
        pass
        '''try:
            print(f'{key.char} down')
        except AttributeError:
            print(f'{key} down')'''


    def on_release(self,key):
        """定义释放时候的响应"""
        pass
        #print(f'{key} up')


    def on_move(self,x, y):
        pass
        #print('move to', x, y)


    def on_click(self,x, y, button, pressed):
        pass
        #print('click at', x, y, button, pressed)


    def on_scroll(self,x, y, dx, dy):
        pass
        #print('scroll at', x, y, 'by', dx, dy)


    # 监听写法1
    def listen_key_block(self):
        with keyboard.Listener(
                on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()  # 加入线程池，阻塞写法


    # 监听写法2
    def listen_key_nblock(self):
        listener = keyboard.Listener(
            on_press=self.on_press, on_release=self.on_release
        )
        listener.start()  # 启动线程


    def listen_mouse_nblock(self):
        listener = mouse.Listener(
            on_move=None,  # 因为on_move太多输出了，就不放进来了，有兴趣可以加入
            on_click=self.on_click,
            on_scroll=self.on_scroll
        )
        listener.start()


if __name__ == '__main__':

    while True:  # 这里应该用一个循环维持主线程，否则主线程结束了子线程就自动结束了
        pass