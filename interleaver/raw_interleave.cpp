/*
 * Interleave ACFR RAW files based on the timestamp
 *
 * Christian Lees
 * 9/1/14
 */
 
#include <adt_raw_file.hpp>
#include <fstream>
#include <iostream>
#include <list>

using namespace std;
using namespace auv_data_tools;

class rawFile {
    public:
    Raw_File *file;
    Data *data;
};

int main(int argc, char **argv) {
    if(argc < 3) {
        cerr << "Usage: raw_interleave [input 1] [input 2] ... [input n]" << endl;
        return 1;
    }
    
    int numFiles = argc - 1;
    list<rawFile*> inFiles;
    for(int i=0; i<numFiles; i++) {
        rawFile *inFile = new rawFile;;
        inFile->file = new Raw_File(10);
        inFile->file->open_file(argv[i + 1]);
        inFiles.push_back(inFile);
    }

    // get the first element from each file    
    for(list<rawFile*>::iterator it=inFiles.begin(); it!=inFiles.end(); ++it) {
        (*it)->data = (*it)->file->get_next();
        if((*it)->data == NULL)
            inFiles.remove(*it);
       // (*it)->data->print(cout);
       // cout << endl;
    }
    
    
    while(inFiles.size() > 0) {
        // find the one with the lowest time
        rawFile *lowest = *inFiles.begin();
        for(list<rawFile*>::iterator it=inFiles.begin(); it!=inFiles.end(); ++it) {
            if((*it)->data->get_timestamp() < lowest->data->get_timestamp())
                lowest = *it;
        }
                
        // print the lowest and then get the next one in that file
        lowest->data->print(cout);
        cout << endl;
        
        lowest->data = lowest->file->get_next();
        if(lowest->data == NULL)
            inFiles.remove(lowest);
    }                
    
}
