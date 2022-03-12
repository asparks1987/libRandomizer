#include "random.h"
#include <time.h>



Random::Random()
{
    srand (time ( NULL));
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
    double range = (Y - X);
    double div = RAND_MAX / range;
    return X + (rand() / div);
}

void Random::_resetDistrobution(){
    X=0;
    Y=1;
}
