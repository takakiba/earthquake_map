import cv2
import glob
import tqdm


def make_movie(image_file_path, frame_rate=30.0, video_name='video', image_format='png'):
	filelist = glob.glob(image_file_path + '/*.' + image_format)
	filelist.sort()

	im0 = cv2.imread(filelist[0])
	height, width, color = im0.shape

	fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
	video = cv2.VideoWriter('{0}.mp4'.format(video_name), fourcc, frame_rate, (width, height))

	for file in tqdm.tqdm(filelist):
		img = cv2.imread(file)
		video.write(img)


if __name__ == '__main__':
    make_movie('data/test_api_002', video_name='EQ_movie')
