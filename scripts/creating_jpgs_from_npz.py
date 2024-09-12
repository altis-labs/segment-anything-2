import os
import numpy as np
import shutil
from PIL import Image
from tqdm import tqdm


def process_directories(root_dir):
    for patient_id in tqdm(os.listdir(root_dir)):
        patient_dir = os.path.join(root_dir, patient_id)

        if not os.path.isdir(patient_dir):
            continue

        for study_uid in os.listdir(patient_dir):
            study_dir = os.path.join(patient_dir, study_uid)

            if not os.path.isdir(study_dir):
                continue

            for series_uid in os.listdir(study_dir):
                series_dir = os.path.join(study_dir, series_uid)
                converted_npz_dir = os.path.join(series_dir, 'converted_npz')

                if not os.path.exists(converted_npz_dir):
                    # Delete the patient_id/study_uid/series_uid directory if 'converted_npz' does not exist
                    print(f"Deleting directory: {series_dir}")
                    shutil.rmtree(series_dir)
                else:
                    # Create 'video' directory next to 'converted_npz' if it exists
                    video_dir = os.path.join(series_dir, 'video')
                    os.makedirs(video_dir, exist_ok=True)

                    # Process each slice folder inside 'converted_npz'
                    for slice_dir in os.listdir(converted_npz_dir):
                        slice_path = os.path.join(converted_npz_dir, slice_dir)

                        if os.path.isdir(slice_path):
                            npz_file = os.path.join(slice_path, 'raw_image.npz')

                            if os.path.exists(npz_file):
                                # Load the .npz file
                                data = np.load(npz_file)
                                raw_image = data['arr_0']  # Assuming the array is stored under 'arr_0'

                                # Convert the raw image into a JPEG and save it
                                img = Image.fromarray(raw_image)
                                jpg_filename = os.path.join(video_dir, f"{slice_dir}.jpg")
                                img.save(jpg_filename)
                                print(f"Saved {jpg_filename}")

if __name__ == '__main__':
    root_directory = '/home/ubuntu/segment-anything-2/data'  # Replace with your actual root directory path
    process_directories(root_directory)
