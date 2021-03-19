/* 
* Gazi13
* 19/03/21
* Sonuc: 19 -- 9 -- 18 -- 8 -- 15 -- 5 -- 13 -- 7 -- 15 -- 5 
*/


#include <iostream>
#include <vector>
#include <algorithm>
#include <map>
#include <string>
#include <chrono>
#include <cstring>


using namespace std; 

int main(){

// random number generate
srand ( time(NULL) );

// to save the numbers
vector<int> temp;
int old_number = -1;

for (int t=0;t<10;t++)
{
    // take a random number
    int random_x;
    random_x = rand() % 20;
    
    // check differences & if more than 5 accept it 
    if(abs(old_number-random_x)>4){

        temp.push_back(random_x);
        old_number = random_x;

    }
    // if not try again
    else{
        t--;
    }
} 

for (int i=0;i<temp.size();i++){
    cout <<temp[i]<<" -- ";
}

	
}
