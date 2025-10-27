#include <map>
#include <list>
#include <iostream>
#include <cassert>
#include <sstream>

using int_str = std::pair<int , std::string>;

namespace name1
{
    int x = 2;
    int_str type = {x,"hello"};
} // namespace name1


namespace name2
{
    int x = 3;
    int_str type = {x,"hell"};;
} // namespace name2


int main() {
    
    std::string cars[] = {"car1","car2","car3"};
    int number_cars[] = {1,2,3};

    std::map<std::string, int> m;


    int array_max_length = std::max(std::size(cars),std::size(number_cars));
    for(int x = 0; x < array_max_length; x++){
        m[cars[x]] = number_cars[x];
    }
    


    for (auto& p : m)
        std::cout << p.first << " " << p.second << std::endl;


    std::list<std::string> planes;

    for(int i=0; i<5;i++){

        std::stringstream ss;
        ss << "plane" << i;
        planes.push_front(ss.str());
    }

    for (std::string plane: planes)
        std::cout << plane << std::endl;


    return 1;
} 
