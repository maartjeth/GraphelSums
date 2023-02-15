import argparse
import json
import os
from bs4 import BeautifulSoup


class TitlesCNN:

    def __init__(self, data_folder, output_dict):
        self.title_dict = {}
        self.data_folder = data_folder
        self.output_dict = output_dict

    def find_title(self, file):
        html = open(file, encoding='latin1').read()
        soup = BeautifulSoup(html)
        hash_name = os.path.basename(file)[:-5]

        title_div = soup.find(id='cnnHeaderLeftCol')
        if title_div:
            title = title_div.h1.text
        else:  # Nesting turned out faster
            h1_set = soup.find_all('h1')
            if h1_set:
                for h1 in h1_set:
                    if h1.text != 'CNN':
                        title = h1.text
            else:
                title_div = soup.find(itemprop='headline name')
                if title_div:
                    title = title_div.text
                else:
                    print('Nothing: {}'.format(file))

        self.title_dict[hash_name] = title

    def fill_title_dict(self):
        count = 0
        for file in os.scandir(self.data_folder):
            if count % 500 == 0:
                print('Working on document: {}'.format(count))
            self.find_title('{}{}'.format(self.data_folder, file.name))
            count += 1

    def save_dict_to_json(self):
        with open(self.output_dict, 'w') as output_dict:
            json.dump(self.title_dict, output_dict)

    def main(self):
        print('Filling the title dict...')
        self.fill_title_dict()
        print('Saving to json...')
        self.save_dict_to_json()
        print('Done!')


class TitlesDM:

    def __init__(self, data_folder, output_dict):
        self.title_dict = {}
        self.data_folder = data_folder
        self.output_dict = output_dict

    def find_title(self, file):
        html = open(file, encoding='latin1').read()
        soup = BeautifulSoup(html)
        hash_name = os.path.basename(file)[:-5]

        h1_set = soup.find_all('h1')
        if h1_set:
            title = h1_set[0].text
        else:
            print('Nothing: {}'.format(file))

        self.title_dict[hash_name] = title

    def fill_title_dict(self):
        count = 0
        for file in os.scandir(self.data_folder):
            if count % 500 == 0:
                print('Working on document: {}'.format(count))
            self.find_title('{}{}'.format(self.data_folder, file.name))
            count += 1

    def save_dict_to_json(self):
        with open(self.output_dict, 'w') as output_dict:
            json.dump(self.title_dict, output_dict)

    def main(self):
        print('Filling the title dict...')
        self.fill_title_dict()
        print('Saving to json...')
        self.save_dict_to_json()
        print('Done!')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get titles')
    parser.add_argument('--data_folder_cnn', required=True)
    parser.add_argument('--output_dict_cnn', required=True)
    parser.add_argument('--data_folder_dm', required=True)
    parser.add_argument('--output_dict_dm', required=True)

    args = parser.parse_args()

    # Get CNN titles
    titles_cnn = TitlesDM(args.data_folder_cnn, args.output_dict_cnn)
    titles_cnn.main()

    # Get DM titles
    titles_dm = TitlesDM(args.data_folder_dm, args.output_dict_dm)
    titles_dm.main()
