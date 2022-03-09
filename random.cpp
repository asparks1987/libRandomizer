#include "random.h"

Random::Random()
{
}

double Random::getRandomDouble(){
    this->reset();
    return _doubleGen();
}

double Random::getRandomDouble(double low, double high){
    this->X=low;
    this->Y=high;
    return _doubleGen();
}

void Random::reset(){
    _resetDistrobution();
}

double Random::_doubleGen(){
    return rand()% X+-Y;
}

void Random::_resetDistrobution(){
    X=-1;
    Y=1;
}
