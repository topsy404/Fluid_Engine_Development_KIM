#include <iostream>
#include <vector>
#include <string>
#include <cassert>

#define assertm(exp, msg) assert(((void)msg, exp))

#include <thread>
#include <chrono>
#include <cmath>
#include <fstream>

const size_t kBufferSize = 80;
const int frames = 100;
const double M_PI = 3.1415926;

const std::string kGrayScaleTable = " 123456789";
const size_t kGrayScaleTableSize = kGrayScaleTable.length();

void accumulateWaveToHeightField(const double x,
                                 const double waveLength,
                                 const double maxHeight,
                                 std::vector<double> &heightField) {
    const double quarteWaveLength = 0.25 * waveLength;
    double position, distance, height;

    const int start = std::max(0, static_cast<int>((x - quarteWaveLength) * kBufferSize));
    const int end = std::min((int) kBufferSize - 1, static_cast<int>((x + quarteWaveLength) * kBufferSize));
    for (int i = start; i < end + 1; i++) {
        position = i * 1.0 / kBufferSize;
        distance = std::min(1.0, std::fabs(position - x) / quarteWaveLength);
        height = std::cos(distance * M_PI / 2) * maxHeight;
        heightField[i] += height;
    }

}

void draw(const std::vector<double> &heightField) {
    std::string buffer(kBufferSize, ' ');
    // Convert height field to grayscale
    for (size_t i = 0; i < kBufferSize; ++i) {
        double height = heightField[i];
        size_t tableIndex = std::min(
                static_cast<size_t>(floor(kGrayScaleTableSize * height)),
                kGrayScaleTableSize - 1);
        buffer[i] = kGrayScaleTable[tableIndex];
    }
    // Clear old prints
    for (size_t i = 0; i < kBufferSize; ++i) {
        printf("\b");
    }
    // Draw new buffer
    printf("%s", buffer.c_str());
    std::ofstream ofs;
    ofs.open("./result.txt", std::fstream::app);
    ofs << buffer.append("\n");
    ofs.close();


    fflush(stdout);
}

void updateWave(const double timeInterval, double *x, double *speed) {
    (*x) += timeInterval * (*speed);
    if (*x > 1.0) {
        (*speed) *= -1;
        (*x) = 1.0 + timeInterval * (*speed);
    } else if (*x < 0) {
        (*speed) *= -1;
        (*x) = timeInterval * (*speed);
    }
}


int main() {
    double x = 0.0, y = 1.0, speedX = 1.0, speedY = -0.5;
    const double waveLengthX = 0.8, waveLengthY = 1.2, maxHeightX = 0.5, maxHeightY = 0.4;
    const int fps = 100;
    const double timeInterval = 1.0 / fps;
    std::vector<double> heightField(kBufferSize);
    for (int i = 0; i < frames; i++) {
        updateWave(timeInterval, &x, &speedX);
        updateWave(timeInterval, &y, &speedY);
        // clean height file
        std::fill(heightField.begin(), heightField.end(), 0.0);
        accumulateWaveToHeightField(x, waveLengthX, maxHeightX, heightField);
        accumulateWaveToHeightField(y, waveLengthY, maxHeightY, heightField);

        // Draw height field
        draw(heightField);

        // Wait
        std::this_thread::sleep_for(std::chrono::milliseconds(100 / fps));

    }


}