import csv

TXID_INDEX = 0
FEE_INDEX = 1
WEIGHT_INDEX = 2
PARENTID_INDEX = 3

filename = "mempool.csv"
filePath = "block.csv"

def block_constructor():
    dictionary = {}
    txn_list = []
    weight = 0
    max_weight = 4000000
    
    with open(filename, "rt") as csv_file:
        reader = csv.reader(csv_file)
        parentids = None
        
        for line in reader:
            parts = line[0].split(',')
            txid = parts[TXID_INDEX]
            fee = int(parts[FEE_INDEX])
            weight = int(parts[WEIGHT_INDEX])
            if(parts[PARENTID_INDEX]):
                parentids = parts[PARENTID_INDEX]
            
            txn_list.append([txid, fee, weight, parentids])
            
    sorted_list = sort_list(txn_list)
    # reinitialize weight
    weight = 0
    
    with open(filePath, "w") as file:
        track_recent_weight = 0
        while weight + track_recent_weight < max_weight:    
            for txns in sorted_list:
                if txns[PARENTID_INDEX] and check_parent(dictionary, txns[PARENTID_INDEX]) == False:       
                    continue
                else:
                    if weight + txns[WEIGHT_INDEX] <= max_weight:
                        weight += txns[WEIGHT_INDEX]
                        dictionary[txns[TXID_INDEX]] = True
                        track_recent_weight = txns[WEIGHT_INDEX]
                        print(f"{txns[0]}")
                        file.write(f"{txns[0]}\n")               
                    
    print("weight", weight)

def sort_list(txn_list):
    sorted_list = sorted(txn_list, key=lambda x: x[1], reverse=True)
    return sorted_list

def check_parent(dict, parentids):
    parentids = parentids.split(';')
    for id in parentids:
        if id not in dict or not dict.get(id):
            return False
    return True

block_constructor()
