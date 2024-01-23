from rest_framework import generics
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import UploadedImage
from .serializers import UploadedImageSerializer
from roboflow import Roboflow
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.transforms import Affine2D
from PIL import Image
import io
import os 
# /home/saad-alam/Documents/Nodelays_Works_pace/data_matrix/3 (1).png
class UploadImageView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = UploadedImageSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            # Get the path to the uploaded image
            uploaded_image_path = serializer.data['image']

            # Roboflow integration
            rf = Roboflow(api_key="gEhnvEfmjEMDgnRqLBWl")
            project = rf.workspace().project("dm-detection")
            model = project.version(1).model

            # Read the uploaded image
            print(uploaded_image_path)
            parent_directory_path = "media/images"
            image_path  = os.path.join(parent_directory_path,"image_3_p4N3Zod.png")
            image_size = ""
            background = np.ones(image_size, dtype=np.uint8) * 255

            # Infer on the local image
            data_matrix = model.predict(image_path, confidence=0, overlap=1).json()['predictions']
            x_data = []
            y_data = []
            for i, dictionary in enumerate(data_matrix, start=1):
                globals()[f'dic{i}'] = dictionary
                keys = list(dictionary.keys())
                values = list(dictionary.values())
                if values[6] == 1:
                    x_data.append(values[0])
                    y_data.append(values[1])

            # Calculate Coordinates of Modules
            points = list(zip(x_data, y_data))

            #  Calculate the average distances between consecutive points in x and y direction
            x_dist = [x_data[i + 1] - x_data[i] for i in range(len(x_data) - 1)]
            y_dist = [y_data[i + 1] - y_data[i] for i in range(len(y_data) - 1)]

            # Generate squares around points
            def plot_squares(coordinates, side_length):
                for coord in coordinates:
                    x_data, y_data = coord
                    square = plt.Rectangle((x_data - side_length/2, y_data - side_length/2),
                                        side_length, side_length, edgecolor='black', facecolor='black')
                    plt.gca().add_patch(square)

            side_length = 0
            limit = range(9, 10)
            for i in x_dist:
                if i in limit:
                    side_length = abs(np.median(limit))

            # Plotting squares around the coordinates
            plot_squares(points, side_length)
            plt.gca().invert_yaxis()
            # plt.savefig(image_path.strip(image_path.split("/")[-1]) + "result_DM8.png")
            # plt.show()
            # Rest of your processing code...

            # Save the processed image with a unique name
            result_image_path = os.path.join(parent_directory_path, "result_DM8.png")
            # plt.savefig(result_image_path)
            # plt.show()

            # Return the processed image path or any other response as needed
            return Response({"message": "Image processed successfully", "result_image_path": result_image_path}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request, *args, **kwargs):
        return Response({"message": "GET request handled successfully"})
        
    # Your logic for handling GET requests


class ListUploadedImagesView(generics.ListAPIView):
    queryset = UploadedImage.objects.all()
    serializer_class = UploadedImageSerializer
