from flask import jsonify, render_template, request
from flask import flash, request
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from application import app
from application import cvfuntions as cvf

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Ignore  the warnings
import warnings

warnings.filterwarnings("always")
warnings.filterwarnings("ignore")


@app.route("/")
def hello():
    return render_template("index.html")


@app.route("/save")
def save():
    if request.method == "POST":
        # Get the JSON data from the request
        img_data = request.json["img_data"]

        img = cvf.convertinit(img_data)

        # Encode the modified image back to base64
        pil_image = Image.fromarray(img)
        img_data = cvf.display(pil_image)
        response = app.make_response(img_data)
        response.headers["Content-Type"] = "image/jpeg"
    return response


@app.route("/inputimg", methods=["GET", "POST"])
def inputimg():
    if request.method == "POST":
        file = request.files["imgfile"]
        print(file)
        if "imgfile" not in request.files:
            flash("No file uploaded")
            print("No file uploaded")
            return render_template("index.html")
        file = request.files["imgfile"]
        im = Image.open(file)
        img_data = cvf.display(im)
        return render_template("index.html", img_data=img_data)
    return render_template("index.html")


@app.route("/cropfun", methods=["GET", "POST"])
def cropfun():
    if request.method == "POST":
        start_x = int(request.json["x1"])
        start_y = int(request.json["y1"])
        end_x = int(request.json["x2"])
        end_y = int(request.json["y2"])

        # Get the JSON data from the request
        img_data = request.json["img_data"]

        img = cvf.convertinit(img_data)

        # Crop the image
        cropped_image = img[start_y:end_y, start_x:end_x]
        cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB)

        # Encode the modified image back to base64
        pil_image = Image.fromarray(cropped_image)
        img_data = cvf.display(pil_image)
    return jsonify({"img_data": img_data})


@app.route("/resize", methods=["GET", "POST"])
def resize():
    if request.method == "POST":
        width = int(request.json["width"])
        height = int(request.json["height"])
        method = int(request.json["method"])

        if method == 1:
            interpolation = cv2.INTER_NEAREST
        elif method == 2:
            interpolation = cv2.INTER_LINEAR
        elif method == 3:
            interpolation = cv2.INTER_CUBIC
        else:
            print(
                "Invalid interpolation method selected. Using default (Nearest Neighbor)."
            )
            interpolation = cv2.INTER_NEAREST

        # Get the JSON data from the request
        img_data = request.json["img_data"]
        img = cvf.convertinit(img_data)

        # resize the image
        resized_image = cv2.resize(img, (width, height), interpolation=interpolation)
        cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)

        # Encode the modified image back to base64
        pil_image = Image.fromarray(resized_image)
        img_data = cvf.display(pil_image)
    return jsonify({"img_data": img_data})


@app.route("/rotate", methods=["GET", "POST"])
def rotate():
    if request.method == "POST":
        angle = float(request.json["angle"])

        # Get the JSON data from the request
        img_data = request.json["img_data"]
        img = cvf.convertinit(img_data)

        # rotate the image
        rotation_matrix = cv2.getRotationMatrix2D(
            (img.shape[1] / 2, img.shape[0] / 2), angle, 1
        )
        rotated_image = cv2.warpAffine(
            img, rotation_matrix, (img.shape[1], img.shape[0])
        )
        cv2.cvtColor(rotated_image, cv2.COLOR_BGR2RGB)

        # Encode the modified image back to base64
        pil_image = Image.fromarray(rotated_image)
        img_data = cvf.display(pil_image)
    return jsonify({"img_data": img_data})


@app.route("/flip", methods=["GET", "POST"])
def flip():
    if request.method == "POST":
        flip_dir = request.json["flip_dir"]

        # Get the JSON data from the request
        img_data = request.json["img_data"]
        img = cvf.convertinit(img_data)

        # rotate the image
        if flip_dir == "h":
            flipped_image = cv2.flip(img, 1)  # Horizontal flip
        elif flip_dir == "v":
            flipped_image = cv2.flip(img, 0)  # Vertical flip
        else:
            flipped_image = img  # No flip

        cv2.cvtColor(flipped_image, cv2.COLOR_BGR2RGB)

        # Encode the modified image back to base64
        pil_image = Image.fromarray(flipped_image)
        img_data = cvf.display(pil_image)
    return jsonify({"img_data": img_data})


@app.route("/adjustenhance", methods=["GET", "POST"])
def adjustenhance():
    if request.method == "POST":
        brightness = float(request.json["brightness"])
        contrast = float(request.json["contrast"])

        # Get the JSON data from the request
        img_data = request.json["img_data"]
        img = cvf.convertinit(img_data)

        # Adjust brightness and contrast
        adjusted_image = cv2.convertScaleAbs(img, alpha=contrast, beta=brightness)
        adjusted_image = np.clip(adjusted_image, 0, 255)
        cv2.cvtColor(adjusted_image, cv2.COLOR_BGR2RGB)

        # Encode the modified image back to base64
        pil_image = Image.fromarray(adjusted_image)
        img_data = cvf.display(pil_image)
    return jsonify({"img_data": img_data})


@app.route("/coloradjustment", methods=["GET", "POST"])
def coloradjustment():
    if request.method == "POST":
        hue = int(request.json["hue"])
        saturation = int(request.json["saturation"])
        brightness = int(request.json["brightness"])

        # Get the JSON data from the request
        img_data = request.json["img_data"]
        img = cvf.convertinit(img_data)

        # Adjust brightness and contrast
        h, s, v = cv2.split(img)
        h = (h + hue) % 180
        s = np.clip(s + saturation, 0, 255)
        v = np.clip(v + brightness, 0, 255)
        adjusted_hsv_image = cv2.merge((h, s, v))

        # Convert the adjusted image back to BGR color space
        adjusted_image = cv2.cvtColor(adjusted_hsv_image, cv2.COLOR_HSV2BGR)
        cv2.cvtColor(adjusted_image, cv2.COLOR_BGR2RGB)

        # Encode the modified image back to base64
        pil_image = Image.fromarray(adjusted_image)
        img_data = cvf.display(pil_image)
    return jsonify({"img_data": img_data})


@app.route("/sharpeblur", methods=["GET", "POST"])
def sharpeblur():
    if request.method == "POST":
        filter = int(request.json["filter"])

        # Get the JSON data from the request
        img_data = request.json["img_data"]
        img = cvf.convertinit(img_data)

        # Adjust brightness and contrast
        if filter not in ["sharpening", "blurring"]:
            print("Invalid filter selection. Using sharpening by default.")
            filter = "sharpening"

        if filter == "sharpening":
            # Sharpening kernel
            kernel = np.array(
                [[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]], dtype=np.float32
            )
            result_image = cv2.filter2D(img, -1, kernel)
        else:
            # Blurring kernel
            kernel = np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]], dtype=np.float32) / 16
            result_image = cv2.filter2D(img, -1, kernel)

        # Convert the adjusted image back to BGR color space
        adjusted_image = cv2.cvtColor(result_image, cv2.COLOR_HSV2BGR)
        cv2.cvtColor(adjusted_image, cv2.COLOR_BGR2RGB)

        # Encode the modified image back to base64
        pil_image = Image.fromarray(adjusted_image)
        img_data = cvf.display(pil_image)
    return jsonify({"img_data": img_data})


@app.route("/noisereduction", methods=["GET", "POST"])
def noisereduction():
    if request.method == "POST":
        technique = request.json["technique"]

        # Get the JSON data from the request
        img_data = request.json["img_data"]
        img = cvf.convertinit(img_data)

        if technique not in ["1", "2", "3"]:
            print("Invalid technique selected. Using Median Filtering by default.")
            technique = "1"

        # Apply the selected noise reduction technique
        if technique == "1":
            denoised_image = cv2.medianBlur(img, 5)
            result_title = "Median Filtered Image"
        elif technique == "2":
            denoised_image = cv2.bilateralFilter(img, 9, 75, 75)
            result_title = "Bilateral Filtered Image"
        elif technique == "3":
            # Convert the image to grayscale for wavelet denoising
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Perform wavelet denoising
        denoised_image = cv2.fastNlMeansDenoising(gray_image, None, h=6)

        result_title = "Wavelet Denoised Image"
        cv2.cvtColor(denoised_image, cv2.COLOR_BGR2RGB)

        # Encode the modified image back to base64
        pil_image = Image.fromarray(denoised_image)
        img_data = cvf.display(pil_image)
    return jsonify({"img_data": img_data, "result_title": result_title})


@app.route("/cloneheal", methods=["GET", "POST"])
def cloneheal():
    if request.method == "POST":
        choice = request.json["choice"]
        x1 = int(request.json["x1"])
        y1 = int(request.json["y1"])
        x2 = int(request.json["x2"])
        y2 = int(request.json["y2"])

        # Get the JSON data from the request
        img_data = request.json["img_data"]
        img = cvf.convertinit(img_data)

        if choice not in ["1", "2"]:
            print("Invalid choice. Using cloning by default.")
            choice = "1"

        # Extract the selected area based on user-provided coordinates
        selected_area = img[y1:y2, x1:x2]

        # Perform inpainting (cloning or healing)
        if choice == "1":
            # Inpaint to clone the area (remove object)
            mask = np.zeros_like(selected_area)
            result = cv2.inpaint(img, mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)
            result_title = "Cloned Image (Object Removed)"
        else:
            # Inpaint to heal the area
            mask = 255 * np.ones_like(selected_area)
            result = cv2.inpaint(img, mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)
            result_title = "Healed Image"

        cv2.cvtColor(result, cv2.COLOR_BGR2RGB)

        # Encode the modified image back to base64
        pil_image = Image.fromarray(result)
        img_data = cvf.display(pil_image)
    return jsonify({"img_data": img_data, "result_title": result_title})


@app.route("/textbox", methods=["GET", "POST"])
def textbox():
    if request.method == "POST":
        text = request.json["text"]
        fontsize = int(request.json["fontsize"])
        textcolor = request.json["textcolor"]
        x = int(request.json["x"])
        y = int(request.json["y"])

        # Get the JSON data from the request
        img_data = request.json["img_data"]
        img = cvf.convertinit(img_data)

        # Create a new image with the same size as the background
        result = img.copy()

        # width, height = result.size
        result = Image.fromarray(result)

        # Create a drawing context
        draw = ImageDraw.Draw(result)

        # Load a font
        font = ImageFont.load_default()

        # Draw the text on the image at the user-specified position
        draw.text((x, y), text, fill=textcolor, font=font)

        # cv2.cvtColor(result, cv2.COLOR_BGR2RGB)

        # Encode the modified image back to base64
        # pil_image = Image.fromarray(result)
        img_data = cvf.display(result)
        # img_data = cvf.display(pil_image)
    return jsonify({"img_data": img_data})


@app.route("/imgbeautify", methods=["GET", "POST"])
def imgbeautify():
    if request.method == "POST":
        # Get the JSON data from the request
        img_data = request.json["img_data"]
        img = cvf.convertinit(img_data)

        def beautify_image(input_image):
            # Convert image to grayscale
            # Convert image to grayscale
            gray = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)

            # Apply bilateral filter to smoothen and enhance edges
            smooth = cv2.bilateralFilter(input_image, d=9, sigmaColor=75, sigmaSpace=75)

            # Combine the smoothed and grayscale images
            beautified = cv2.addWeighted(input_image, 1.5, smooth, -0.5, 0, gray)

            return beautified

        # Apply beautification filters
        beautified_image = beautify_image(img)

        cv2.cvtColor(beautified_image, cv2.COLOR_BGR2RGB)

        # Encode the modified image back to base64
        pil_image = Image.fromarray(beautified_image)
        img_data = cvf.display(pil_image)
    return jsonify({"img_data": img_data})


@app.route("/imgcartoon", methods=["GET", "POST"])
def imgcartoon():
    if request.method == "POST":
        # Get the JSON data from the request
        img_data = request.json["img_data"]
        img = cvf.convertinit(img_data)

        # Function to cartoonify an image
        def cartoonify_image(input_image):
            # Convert the image to grayscale
            gray = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)

            # Apply bilateral filter to smooth the image while preserving edges
            smooth = cv2.bilateralFilter(input_image, d=9, sigmaColor=75, sigmaSpace=75)

            # Apply median blur to reduce noise
            gray = cv2.medianBlur(gray, 5)

            # Detect edges using adaptive thresholding
            edges = cv2.adaptiveThreshold(
                gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9
            )

            # Combine the smoothed and edge images to create the cartoon effect
            cartoon = cv2.bitwise_and(smooth, smooth, mask=edges)

            return cartoon

        # Apply the cartoonify filter
        cartoonified_image = cartoonify_image(img)
        cv2.cvtColor(cartoonified_image, cv2.COLOR_BGR2RGB)

        # Encode the modified image back to base64
        pil_image = Image.fromarray(cartoonified_image)
        img_data = cvf.display(pil_image)
    return jsonify({"img_data": img_data})


@app.route("/facedetection", methods=["GET", "POST"])
def facedetection():
    if request.method == "POST":
        # Get the JSON data from the request
        img_data = request.json["img_data"]
        img = cvf.convertinit(img_data)

        # Load the Haar Cascade for face detection
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

        # Function to perform face detection
        def detect_faces(image):
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(
                gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
            )
            return faces

        # Detect faces in the image
        faces = detect_faces(img)

        if len(faces) > 0:
            # Draw rectangles around the detected faces
            for x, y, w, h in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

            cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Encode the modified image back to base64
            pil_image = Image.fromarray(img)
            img_data = cvf.display(pil_image)
            return jsonify({"img_data": img_data})

        else:
            print("No faces detected in the image.")
            return jsonify(
                {"img_data": img_data, "data": "No faces detected in the image."}
            )
