# models/diagnosis.py
from models.text_model import TextDiagnosisModel
from models.image_model import ImageDiagnosisModel

# Initialize models (in production, load trained weights)
text_model = TextDiagnosisModel()
image_model = ImageDiagnosisModel()

def diagnose_patient(data):
    """
    Process text-based input using mnemonics such as WWHAM, ASMETHOD, ENCORE, and SIT DOWN SIR.
    A simple rule-based check for danger symptoms is included.
    """
    if 'danger_symptoms' in data and data['danger_symptoms'].strip().lower() in ['yes', 'true']:
        return "Severe symptoms detected. Please consult a doctor immediately."
    
    # Use the ML text model (this is a placeholder that would normally preprocess the data and predict)
    prediction = text_model.predict(data)
    return prediction

def diagnose_image(image_path):
    """
    Process an uploaded image (CT, MRI, etc.) for diagnosis using a convolutional neural network.
    """
    prediction = image_model.predict(image_path)
    return prediction
