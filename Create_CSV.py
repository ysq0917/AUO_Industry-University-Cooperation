import numpy as np
import pandas as pd
import csv
import random
import argparse
import os

def get_parser():
    parser = argparse.ArgumentParser(description="Create CSV")
    
    parser.add_argument('--num_classes', default=32, type=int,
                       help="The number of classes you need")
    parser.add_argument('--num_train', default=450, type=int,
                       help="The number of images in trainset")
    parser.add_argument('--num_test', default=50, type=int,
                       help="The number of images in testset")
    parser.add_argument('--dataset_path', default="./", type=str,
                       help="The path to the dataset folder")
    parser.add_argument('--image_path', default="images", type=str,
                       help="The path to the images subfolder in dataset")
    parser.add_argument('--delimiter', default=",", type=str,
                       help="the delimiter in the csv file")
    parser.add_argument('--header', default=True, action='store_false',
                       help="whether to use the header")
    parser.add_argument('-c', default="", type=str,
                       help="csv file")
    parser.add_argument('-p', default=False, action='store_true',
                       help="use proportion split")
    parser.add_argument('--proportion', default=0.1, type=int,
                       help="Test set size proportion")
    parser.add_argument('-s', default=False, action='store_true',
                       help="use proportion split")
    
    return parser
    

def Create_CSV(args, class_list):
    
    file_names = os.listdir(args.dataset_path + args.image_path)
    
    # Get the labels from the file names
    labels = [int(i[1:4]) for i in file_names]
    class_num = len(set(labels))
    class_order = list(set(labels))
    print(class_num)
    print(class_list)
    
    # intialize the samples list
    samples = [list() for i in range(class_num+1)]
    
    # assign different images to its class list
    for i in range(len(file_names)):
        samples[class_order.index(labels[i])].append(file_names[i])
    
    # sample the images from the original dataset
    dataset_samples = [list() for i in range(len(class_list))]
    for i in range(len(class_list)):
        for j in range(len(class_list[i])):
            # print(j)
            # if s is True, use fixed amounts of train and test samples
            if args.s:
                dataset_samples[i].extend(random.sample(samples[class_order.index(class_list[i][j])], args.num_train + args.num_test))
            # else use all the samples
            else:
                dataset_samples[i].extend(samples[class_order.index(class_list[i][j])])
    
    # split the iamges into train and validation
    train_samples = [list() for i in range(len(class_list))]
    val_samples = [list() for i in range(len(class_list))]
    for i in range(len(class_list)):
        # split by proportion ex: 9 : 1
        if args.p:
            split = int(len(dataset_samples[i]) * args.proportion)
            random.shuffle(dataset_samples[i])
        else:
            split = args.num_test
        
        train_samples[i] = dataset_samples[i][:-split]
        val_samples[i] = dataset_samples[i][-split:]
        print(len(train_samples[i]), len(val_samples[i]))
    
    # write the csv file for the train and validation set
    with open(args.dataset_path+'/train.csv', mode='w') as train_file, open(args.dataset_path+'/val.csv', mode='w') as val_file:
        train_writer = csv.writer(train_file, delimiter=args.delimiter, quotechar='"', quoting=csv.QUOTE_MINIMAL)
        val_writer = csv.writer(val_file, delimiter=args.delimiter, quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
        if args.header:
            title = ['image', 'label']
            train_writer.writerow(title)
            val_writer.writerow(title)
        
        for i in range(len(class_list)):
            for image_name in train_samples[i]:
                train_writer.writerow([os.path.join(args.image_path, image_name), i])
            for image_name in val_samples[i]:
                val_writer.writerow([os.path.join(args.image_path, image_name), i])
    
    
def main():
    
    args = get_parser().parse_args()
    print(args)
    print(args.num_train + args.num_test)
    
    
    
    if args.num_classes == 20:
        class_order = [1, 4, 5, 6, 7, 9, 10, 11, 13, 18, 19, 20, 21, 22, 24, 25, 26, 27, 28, 29]
    elif args.num_classes == 19:
        class_order = [1, 4, 5, 6, 7, 9, 10, 11, 13, 18, 19, 20, 21 ,22, 24, 25, 26, 27, 28]
    elif args.num_classes == 26:
        class_order = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 18, 20, 21, 22, 23, 24, 27, 28, 29, 30]
    elif args.num_classes == 35:
        class_order = [1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 13, 14, 17, 18, 19, 20, 21, 22, 23, 25, 26, 28, 29, 30, 31, 32, 33, 36, 37, 39, 44, 45, 51, 52, 55]
    elif args.num_classes == 33:
        class_order = [[1, 25, 13], [2], [3], [4], [5], [6], [7, 47], [8], [10], [14], [23], [29], [31], [32], [44], [51], [28], [9], [12, 39], [19], [17, 62], [18], [20], [21], [22], [26], [30], [33], [36], [37], [45], [52], [55]]
    else:
        class_order = np.arange(1, 33)
    
    
    print(len(class_order))
    
    Create_CSV(args, class_order)
    
    

if __name__ == '__main__':
    main()

# Train set : Test set = 9 : 1
# python3 Create_CSV.py --dataset_path /vol/Chris/AUO_Data_1116/ --num_classes 33 --image_path "./A" -p