#!/Users/vadimmonroe/Desktop/Programming/_WORK_PROJECTS/4_RTSP_cameras/venv/bin/python3.9

import sys

from settings import *
import cv2
from ffpyplayer.player import MediaPlayer

"""
system arguments variables:
python cameras.py level_1

examples:
python cameras.py rec
python cameras.py show
"""
command = 'show' if len(sys.argv) == 1 else sys.argv[1]


def show_must_go_on() -> None:
    cameras = [f'rtsp://{ip_cam[0]}:554/user={login}&password={password}&channel={_}&stream=0.sdp' for _ in range(1, 5)]
    cameras.append(f'rtsp://{ip_cam[1]}:554/user={login}&password={password}&channel=1&stream=0.sdp')

    list_cam = [cv2.VideoCapture(_) for _ in cameras]

    """Настройки записи в файлы, fps=200 для быстрого просмотра и сокращения памяти"""
    output = [cv2.VideoWriter(f'archive/video_{i}.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 200, (360, 240)) for i in
              range(1, 6)]

    print('watch')
    file_count = 0
    player = MediaPlayer(cameras[3])

    while True:
        try:
            for num, cam in enumerate(list_cam):
                working, img = list_cam[num].read()
                if working:
                    img = cv2.resize(img, (360, 240))
                    audio_frame, val = player.get_frame()
                    if command == 'show':
                        cv2.imshow(str(num), img)
                        if val != 'eof' and audio_frame is not None:
                            img342, t = audio_frame
                    if command == 'rec':
                        output[num].write(img)
                else:
                    list_cam[num] = cv2.VideoCapture(cameras[num])
                # print(num, list_cam[num], working)

        except Exception as E1:
            print('E1', E1)
            break

        file_count += 1
        # print('Кадр {0:04d}'.format(file_count))

        key = cv2.waitKey(20)
        if (key == ord('q')) or key == 27:
            [_.release() for _ in list_cam]
            [_.release() for _ in output]
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    show_must_go_on()
