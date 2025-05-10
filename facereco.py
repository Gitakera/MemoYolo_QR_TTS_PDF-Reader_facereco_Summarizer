import face_recognition


def encode_face(frame):
    """Encode the face from a single frame."""
    face_locations = face_recognition.face_locations(frame)
    if len(face_locations) > 0:
        return face_recognition.face_encodings(frame, face_locations)[0]
    return None


def match_face(encoding, known_encodings):
    """Match a face encoding with known encodings."""
    matches = face_recognition.compare_faces(known_encodings, encoding)
    if True in matches:
        return matches.index(True)
    return -1
