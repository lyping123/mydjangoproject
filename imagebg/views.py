from django.shortcuts import render
from django.core.files.base import ContentFile
from .models import UploadedImage
from rembg import remove
from PIL import Image
import io

def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        uploaded_file = request.FILES['image']
        image_obj = UploadedImage.objects.create(image=uploaded_file)

        # Open image
        input_image = Image.open(image_obj.image)

        # Process image to remove background
        output = remove(input_image)

        # Save processed image
        img_io = io.BytesIO()
        output.save(img_io, format='PNG')  # Ensure PNG to keep transparency
        image_obj.processed_image.save(f"processed_{image_obj.id}.png", ContentFile(img_io.getvalue()), save=True)

        return render(request, 'imagebg/result.html', {'image_obj': image_obj})

    return render(request, 'imagebg/upload.html')
