import json
import os
import time

import numpy as np
import redis
import settings
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import decode_predictions, preprocess_input
from tensorflow.keras.preprocessing import image

# Connect to Redis and assign to variable db                        
# Uses settings.py to get Redis settings like host, port, etc.
db = redis.Redis(
    host=settings.REDIS_IP,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB_ID,
    decode_responses=True
)

# Load the ML model and assign it to the model variable
# Uses ResNet50 pre-trained on ImageNet
model = ResNet50(include_top = True, weights="imagenet")


def predict(image_name):
    """
    Load an image, preprocess it, and get predictions from the ML model.

    Parameters
    ----------
    image_name : str
        Image filename.

    Returns
    -------
    class_name, pred_probability : tuple(str, float)
        Model predicted class as a string and the corresponding confidence score.
    """

    try:
        # Load image from the specified upload folder
        img_path = os.path.join(settings.UPLOAD_FOLDER, image_name)
        img = image.load_img(img_path, target_size=(224, 224))

        # Convert the image to a NumPy array and preprocess it
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
        img_array = preprocess_input(img_array)  # Apply ResNet50 preprocessing

        # Get model predictions
        predictions = model.predict(img_array)

        # Decode predictions using ResNet50's decode_predictions method
        decoded_predictions = decode_predictions(predictions, top=1)[0][0]
        # Extract class name and probability
        _, class_name, pred_probability = decoded_predictions 
        pred_probability = float(round(pred_probability, 4))    
    
        return class_name, pred_probability
    except Exception as e:
        print(f"Error predicting image: {e}")
        return None, None


def classify_process():
    """
    Continuously listens for new jobs from Redis, processes them using the ML model,
    and stores the results back in Redis.
    """
    while True:
        try:  
            #  Take a new job from Redis queue
            _, job_data = db.brpop(settings.REDIS_QUEUE)  # Blocking pop from Redis queue

            #  Decode the Json data for the given job
            job = json.loads(job_data)
            job_id = job["id"]
            image_name = job["image_name"]

            #  Run ML model prediction(use predict () function)
            class_name, pred_probability = predict(image_name)

            if class_name and pred_probability:
              # Prepare a new JSON with the results
                output = {
                    "prediction": class_name,
                    "score": pred_probability,
                }

                # Store the job results in Redis using the job ID as the key
                db.set(job_id, json.dumps(output))
            else:
                print(f"Failed to process Job {job_id}")

            # Sleep for a bit
            time.sleep(settings.SERVER_SLEEP)
        except Exception as e:
            print(f"Error in classify_process: {e}")
            time.sleep(5) # wait until start again

if __name__ == "__main__":
    # Now launch process
    print("Launching ML service...")
    classify_process()

