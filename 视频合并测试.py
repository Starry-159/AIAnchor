import re
import os
import datetime
import subprocess
from http import HTTPStatus
import dashscope
from dashscope import Generation
from moviepy.editor import VideoFileClip, concatenate_videoclips

Zi_SD_output_path = r'F:\AIAnchor\Output\SadTalker_Output\test2_20241019_005124\1'

m_choice = {
                        'source_image' : r"F:\AIAnchor\Input\models\HuTao\HuTao.jpg",
        }

video_name = os.path.splitext(os.path.basename(m_choice['source_image']))[0]+'##output_enhanced.mp4'
video_path = os.path.join(Zi_SD_output_path, video_name)


print(video_path)

#"F:\AIAnchor\Output\SadTalker_Output\test2_20241019_005124\1\HuTao##output_enhanced.mp4"


# 构建一个空的视频列表
video_files = [
                r"F:\AIAnchor\Output\SadTalker_Output\test2_20241019_015345\1\HuTao##output_enhanced.mp4",
                r"F:\AIAnchor\Output\SadTalker_Output\test2_20241019_015345\2\HuaHuo##output_enhanced.mp4",
                r"F:\AIAnchor\Output\SadTalker_Output\test2_20241019_015345\3\HuTao##output_enhanced.mp4"
]

target_resolution = (960, 1280)  # 目标分辨率 3:4

VideoMerging_output_path = r'F:\AIAnchor\Output\VideoMerging_Output\test2_20241019_015345'

text_file_name = 'test.txt'
# 视频合并
# 加载视频文件
clips = []
for video in video_files:
    try:
        clip = VideoFileClip(video).resize(target_resolution)
        clips.append(clip)
    except Exception as e:
        print(f"Failed to load video {video}: {e}")
# 合并视频片段，使用 method='compose'
final_clip = concatenate_videoclips(clips, method='compose')

VideoMerging_video_path = os.path.join(VideoMerging_output_path, os.path.splitext(text_file_name)[0] + '.mp4')
try:
    final_clip.write_videofile(
        VideoMerging_video_path, 
        codec='libx264', 
        audio_codec='aac', 
        threads=4
    )
except Exception as e:
    print(f"写入视频文件时发生错误: {e}")


