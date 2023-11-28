import shutil  # to save it locally

import requests  # to get image from the web


def download_image(img_url, filename):
    # Open the url image, set stream to True, this will return the stream content.
    r = requests.get(img_url, stream = True)
    # Check if the image was retrieved successfully
    if r.status_code == 200:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True
        # Open a local file with wb ( write binary ) permission.
        with open(filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
        print('Image successfully downloaded: ', filename)
    else:
        print('Image Couldn\'t be retreived')
