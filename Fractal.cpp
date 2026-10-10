#include <complex>
#include <iostream>
#include <random>

class Fractal
{
private:
    std::complex<double> C;

    std::random_device rd;
    std::mt19937 gen;
    std::uniform_real_distribution<long double> distrib;
    std::uniform_real_distribution<long double> offset;

    std::array<unsigned, 2> res;
    unsigned lod;
    double h = 2.5;
    double B = 20.0;

public:
    Fractal(unsigned &width, unsigned &height, unsigned depth) : res{width, height}, lod(depth), gen(rd()), distrib(0.0L, (long double) 2.0 * M_PI), offset(0.995L, 1.10L)
    {
        core();
    }

    Fractal() : res{1680, 1050}, lod(250), gen(rd()), distrib(0.0L, (long double) 2.0 * M_PI), offset(0.995L, 1.10L)
    {
        core();
    }

    Fractal(unsigned depth) : res{1680, 1050}, lod(depth), gen(rd()), distrib(0.0L, (long double) 2.0 * M_PI), offset(0.995L, 1.10L)
    {
        core();
    }

    Fractal(unsigned &width, unsigned &height) : res{width, height}, lod(250), gen(rd()), distrib(0.0L, (long double) 2.0 * M_PI), offset(0.995L, 1.10L)
    {
        core();
    }

    void core()
    {
        std::complex<double> tmp(0.0, distrib(gen));
        C = static_cast<double>(offset(gen)) * (exp(tmp) / 2.0) - (exp(2.0 * tmp) / 4.0);

        double w = h * static_cast<double>(res[0]) / res[1];
        unsigned long i, j;

        std::vector<std::complex<double>> z(res[0]);
        std::vector<double> n(res[0], 2.0 * lod);

        auto it1 = z.begin();
        auto it2 = n.begin();

        for (i = 0; i < res[1]; ++i)
        {

            for (j = 0; it1 != z.end(); ++it1, ++j)
            {
                auto& zn = *it1;

                zn = std::complex<double>((j * w / res[0]) - (w / 2.0), (h / 2.0) - (i * h / res[1]));
            }

            it1 = z.begin();

            for (j = 0; j < lod; ++j)
            {
                for (; it1 != z.end(); ++it1, ++it2)
                {
                    auto& zn = *it1;
                    auto& v = *it2;

                    if (v != 2.0 * lod)
                    {
                        continue;
                    }
                    else if (abs(zn) <= B)
                    {
                        zn = (zn * zn) + C;
                    }
                    else
                    {
                        v = j - (log(log(abs(zn)) / log(B)) / log(2.0));
                    }
                }

                it1 = z.begin();
                it2 = n.begin();
            }

            for (auto& v : n)
            {
                std::cout << v << ' ';
            }

            std::cout << '\n';

            n.assign(n.size(), 2.0 * lod);

        }

    }

};

int main()
{
    unsigned h, w, d;

    std::cin >> w >> h >> d;

    if (w && h && d)
    {
        Fractal julia(w, h, d);
    }
    else if (d)
    {
        Fractal julia(d);
    }
    else
    {
        Fractal julia;
    }

    return 0;
}