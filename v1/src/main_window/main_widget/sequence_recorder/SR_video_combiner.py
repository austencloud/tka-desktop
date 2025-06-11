import cv2
import numpy as np


class SR_VideoCombiner:
    def __init__(self, beat_video_path, video_feed_path, output_path, frame_size=640):
        self.beat_video_path = beat_video_path
        self.video_feed_path = video_feed_path
        self.output_path = output_path
        self.frame_size = frame_size

    def resize_frame_to_square(self, frame):
        """Resize a frame to the specified square size."""
        height, width = frame.shape[:2]
        scale = min(self.frame_size / height, self.frame_size / width)
        resized_frame = cv2.resize(frame, (int(width * scale), int(height * scale)))

        vertical_padding = (self.frame_size - resized_frame.shape[0]) // 2
        horizontal_padding = (self.frame_size - resized_frame.shape[1]) // 2

        top = bottom = vertical_padding
        left = right = horizontal_padding

        if (self.frame_size - resized_frame.shape[0]) % 2 != 0:
            bottom += 1
        if (self.frame_size - resized_frame.shape[1]) % 2 != 0:
            right += 1

        square_frame = cv2.copyMakeBorder(
            resized_frame,
            top,
            bottom,
            left,
            right,
            cv2.BORDER_CONSTANT,
            value=[0, 0, 0],
        )
        return square_frame

    def crop_to_square(self, frame):
        """Crop the widescreen frame to a square based on the height."""
        height, width = frame.shape[:2]
        # Determine cropping coordinates
        left = (width - height) // 2
        right = width - (width - height) // 2
        return frame[:, left:right]

    def pad_to_hd_resolution(self, frame, hd_resolution=(1920, 1080)):
        """Pad the combined square frame to HD resolution."""
        height, width = frame.shape[:2]
        # Calculate padding to reach HD resolution
        top = (hd_resolution[1] - height) // 2
        bottom = hd_resolution[1] - height - top
        left = (hd_resolution[0] - width) // 2
        right = hd_resolution[0] - width - left
        return cv2.copyMakeBorder(frame, top, bottom, left, right, cv2.BORDER_CONSTANT)

    def combine_videos(self):
        cap_beat = cv2.VideoCapture(self.beat_video_path)
        cap_video_feed = cv2.VideoCapture(self.video_feed_path)

        # Set the video capture resolution to HD or the highest possible
        cap_video_feed.set(
            cv2.CAP_PROP_FRAME_WIDTH, 1920
        )  # You can increase this for 4K
        cap_video_feed.set(
            cv2.CAP_PROP_FRAME_HEIGHT, 1080
        )  # You can increase this for 4K

        # Assume we're outputting at 1080p HD resolution
        output_resolution = (1920, 1080)
        combined_width = output_resolution[0]
        combined_height = (
            self.frame_size * 2
            if self.frame_size * 2 < output_resolution[1]
            else output_resolution[1]
        )

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(
            self.output_path, fourcc, 20.0, (combined_width, combined_height)
        )

        while True:
            ret_beat, frame_beat = cap_beat.read()
            ret_feed, frame_feed = cap_video_feed.read()

            if not ret_beat or not ret_feed:
                break

            square_beat = self.resize_frame_to_square(frame_beat)
            square_feed = self.crop_to_square(frame_feed)
            square_feed = self.resize_frame_to_square(square_feed)

            # Combine the square videos side by side
            combined_frame = np.hstack((square_beat, square_feed))
            # Pad the combined video to HD resolution
            hd_frame = self.pad_to_hd_resolution(
                combined_frame, hd_resolution=output_resolution
            )
            out.write(hd_frame)

        cap_beat.release()
        cap_video_feed.release()
        out.release()
