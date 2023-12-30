import requests
import time

# Replace with the actual URL where your Flask app is running
url = 'https://algotive-kluster-cars-v1-5rxxsuinqa-zf.a.run.app/analyze-image' 

# Replace 'path_to_image.jpg' with the actual path to an image file
files = {'image': open('/Users/santuario/Documents/Projects/Andela/data/image-cars/0002_c002_00030615_1.jpg', 'rb')}

# Start the timer
start_time = time.time()

# Post the request
response = requests.post(url, files=files)

# End the timer
end_time = time.time()

# Calculate the response time
response_time = end_time - start_time

# Check if the request was successful
if response.status_code == 200:
    print('Response received successfully.')
    print('Response:', response.json())
else:
    print('Error:', response.text)

print('Response time: {:.2f} seconds'.format(response_time))
