#include <iostream>
#include <dlib/image_processing/frontal_face_detector.h>

using namespace dlib;

int main() {
    frontal_face_detector detector = get_frontal_face_detector();
    return 0;
}
