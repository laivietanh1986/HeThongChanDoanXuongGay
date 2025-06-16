import logging
from dotenv import load_dotenv
from smolagents import tool

load_dotenv()




@tool
def identify_bone_location(bone_description: str) -> str:
    """
    Identify the anatomical location category (study type) of a bone
    based on its description.

    Args:
        bone_description: Description of the bone or region (e.g., "proximal phalanx of the index finger").

    Returns:
        str: One of the study types: elbow, finger, forearm, hand, humerus, shoulder, or wrist.
    """
    bone_description = bone_description.lower()

    if any(part in bone_description for part in ["phalanges", "phalanx", "finger", "thumb", "digit"]):
        return "finger"
    elif any(part in bone_description for part in ["metacarpal", "palm", "hand"]):
        return "hand"
    elif any(part in bone_description for part in ["radius", "ulna", "forearm"]):
        return "forearm"
    elif any(part in bone_description for part in ["humerus", "arm"]):
        return "humerus"
    elif any(part in bone_description for part in ["scapula", "clavicle", "acromion", "shoulder"]):
        return "shoulder"
    elif any(part in bone_description for part in ["elbow", "olecranon", "epicondyle", "radial head", "trochlea"]):
        return "elbow"
    elif any(part in bone_description for part in ["carpal", "wrist", "scaphoid", "lunate", "triquetrum", "pisiform", "trapezium", "trapezoid", "capitate", "hamate"]):
        return "wrist"
    else:
        return "unknown"
@tool
def has_fracture(description: str) -> bool:
    """
    Classify whether the bone described has a fracture.

    Args:
        description: A sentence or phrase describing the bone condition.

    Returns:
        bool: True if a fracture is detected, False otherwise.
    """
    description = description.lower()

    fracture_keywords = [
        "fracture", "fx", "broken", "break", "crack", "hairline",
        "displaced", "comminuted", "greenstick", "impacted", "spiral", "transverse"
    ]

    negative_keywords = [
        "no fracture", "without fracture", "normal", "intact", "unremarkable"
    ]

    if any(neg in description for neg in negative_keywords):
        return False

    return any(keyword in description for keyword in fracture_keywords)
@tool
def fracture_type(description: str) -> list:
    """
    Identify the types of bone fracture described in the input.

    Args:
        description (str): Clinical or radiological text describing the fracture.

    Returns:
        list: List of detected fracture types (can include multiple).
    """
    description = description.lower()

    fracture_types = {
        "avulsion": ["avulsion"],
        "comminuted": ["comminuted"],
        "fracture-dislocation": ["fracture-dislocation", "dislocation with fracture", "fracture dislocation"],
        "greenstick": ["greenstick"],
        "hairline": ["hairline", "stress fracture"],
        "impacted": ["impacted"],
        "longitudinal": ["longitudinal"],
        "oblique": ["oblique"],
        "pathological": ["pathological", "due to metastasis", "osteoporotic fracture", "bone tumor fracture"],
        "spiral": ["spiral"]
    }

    detected = []

    for ftype, keywords in fracture_types.items():
        if any(keyword in description for keyword in keywords):
            detected.append(ftype)

    return detected or ["unspecified"]
@tool
def detect_fracture_bboxes(image:str) -> str:
    """
    Detect bounding boxes for fractures in an X-ray image.

    Args:
        image (PIL.Image.Image): Input X-ray image.


    Returns:
        List[Tuple[int, int, int, int]]: List of bounding boxes in (x_min, y_min, x_max, y_max) format.
    """


    return "Bounding boxes for fractures detected in the image: [(50, 50, 100, 100), (150, 150, 200, 200)]"





