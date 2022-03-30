#ifndef RANDOM_H
#define RANDOM_H
#include <stdlib.h>


class Random
{
    public:
        Random();
        double getRandomDouble();
        double getRandomDouble(double low, double high);
        void reset();

    protected:

    private:
        int X,Y;
        double _doubleGen();
        void _resetDistrobution();
};

#endif // RANDOM_H
