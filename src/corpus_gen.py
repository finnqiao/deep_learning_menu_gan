import pandas as pd
import tqdm

df = pd.read_csv('/Users/finn/msia/deep_learning_menu_gan/data/external/menupages.csv')

df.head()

df = df.dropna()

test_texts_df = df[['menu_descriptions','menu_items','tags']]

def tagseperator(a):
    result = a['tags'].replace(" ","").split(",")
    return result

def splitDataFrameList(df,target_column,separator):
    ''' df = dataframe to split,
    target_column = the column containing the values to split
    separator = the symbol used to perform the split
    returns: a dataframe with each entry for the target column separated, with each element moved into a new row.
    The values in the other columns are duplicated across the newly divided rows.
    '''
    def splitListToRows(row,row_accumulator,target_column,separator):
        split_row = row[target_column].replace(" ","").split(separator)
        for s in split_row:
            new_row = row.to_dict()
            new_row[target_column] = s
            row_accumulator.append(new_row)
    new_rows = []
    df.apply(splitListToRows,axis=1,args = (new_rows,target_column,separator))
    new_df = pd.DataFrame(new_rows)
    return new_df

expanded_rows_df = splitDataFrameList(test_texts_df, 'tags', ',')
# expanded_rows_df['tags'] = expanded_rows_df['tags'].replace(' ','')

expanded_rows_df.head()

expanded_rows_df.shape

tag_list = list(expanded_rows_df['tags'].value_counts().nlargest(31).keys())

expanded_rows_df = expanded_rows_df[expanded_rows_df['tags'].isin(tag_list)]

expanded_rows_df.shape

expanded_rows_df['menu_descriptions'] = ' ' + expanded_rows_df['menu_descriptions'].str.replace('\d+','')
expanded_rows_df['menu_items'] = ' ' + expanded_rows_df['menu_items'].str.replace('\d+','')

# test_agg = expanded_rows_df.groupby('tags').agg('sum')

# tag_dict_item = dict.fromkeys(tag_list,'')
# tag_dict_desc = dict.fromkeys(tag_list,'')

# test_desc = ''
# for row in tqdm.tqdm(expanded_rows_df[expanded_rows_df['tags'] == 'Asian'].itertuples()):
#     test_desc += row[1]
#
# len(test_desc)
# File_object = open(r"../data/auxiliary/desc/asian_desc.txt","w+")
# File_object.write(test_desc)
# File_object.close()

for tag in tqdm.tqdm(tag_list):
    tag_desc = ''
    tag_items = ''
    for row in tqdm.tqdm(expanded_rows_df[expanded_rows_df['tags'] == tag].itertuples()):
        tag_desc += row[1]
        tag_items += row[2]
    File_object = open(r"../data/auxiliary/desc/" + tag + "_desc.txt","w+")
    File_object.write(tag_desc)
    File_object.close()
    File_object = open(r"../data/auxiliary/items/" + tag + "_items.txt","w+")
    File_object.write(tag_items)
    File_object.close()

tag_list

from collections import Counter
import re

tag_desc_common = dict.fromkeys(tag_list)
tag_items_common = dict.fromkeys(tag_list)

# c = Counter()
for tag in tqdm.tqdm(tag_list):
    tag_desc = ''
    tag_items = ''
    for row in tqdm.tqdm(expanded_rows_df[expanded_rows_df['tags'] == tag].itertuples()):
        tag_desc += row[1]
        tag_items += row[2]
    tag_desc = re.sub('[^a-zA-Z0-9 \n\.]', ' ', tag_desc)
    tag_desc = tag_desc.replace('  ',' ')
    tag_items = re.sub('[^a-zA-Z0-9 \n\.]', ' ', tag_items)
    tag_items = tag_items.replace('  ',' ')
    from collections import Counter
    # c = Counter()
    split = tag_desc.split()
    Counter = Counter(split)
    tag_desc_common[tag] = Counter.most_common(100)
    # c = Counter()
    # counter_var = c(tag_items.split())
    # tag_items_common[tag] = counter_var.most_common(100)

pd.DataFrame(tag_desc_common).to_csv('../data/auxiliary/top100_per_tag.csv')
