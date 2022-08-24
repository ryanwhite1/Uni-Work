#include "Question1.cpp"
#include "Question2.cpp"
#include <string>

int main(){
    std::string filename;
    // We want to run the question 1 code three times, to get a few different results based on user input. 
    for (int i = 0; i < 3; i++){
        if (i == 0) filename = "Q1data1.dat";
        if (i == 1) filename = "Q1data2.dat";
        if (i == 2) filename = "Q1data3.dat";
        question1(filename);
    }
    question2();    // We need only run the question 2 code once
    return 0;
}