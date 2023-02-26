import argparse
import pandas as pd
from PIL import Image
TEST = False

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--not_combine', required=False,
                                            action='store_false',
                                            help='separates combines multiple entries into different infographic')
    parser.add_argument('-s', '--subset', required=False,
                                            default='all',
                                            help='subset of entries to be made into infographic(s), entered as one string separated by spaces')
    parser.add_argument('-g', '--groups', required=False,
                                            default='both',
                                            choices=('teams', 'drivers', 'both'),
                                            help='infographics will include just teams, just drivers, or both')
    args = parser.parse_args()
    return args

def get_df(df, df_type):
    columns = df.columns
    newdf_cols = ['Name:']
    newdf_newcols = ['Name']
    if df_type == 'teams':
        tag = "Teams~"
        crop_index = 17
    elif df_type == 'drivers':
        tag = "Drivers~"
        crop_index = 19
    else:
        raise Exception("I do not know what you mean by {}".format(df_type))
    for col in columns:
        if tag in col:
            newdf_newcols.append(col[crop_index:-1])
            newdf_cols.append(col)
        else:
            continue
    newdf = df[newdf_cols]
    newdf.columns = newdf_newcols
    newdf = newdf.set_index('Name')

    return newdf

def make_infographic(df, combine, df_type, rows):
    if df_type == 'teams':
        width = 1100
    else:
        width = 2200

    if combine:
        height = 100* len(rows)
        infographic = Image.new('RGB', (width, height))
        graphic_offset = 0

    for person in rows:
        #create image to hold infographic row
        new_im = Image.new('RGB', (width, 100))

        #obtain predictions in order submitted by "person"
        predictions = df.sort_values(by=person, axis=1).columns
        
        offset = 0
        img_name = 'images/' + person + '.jpg'
        img = Image.open(img_name)
        new_im.paste(img, (offset, 0))
        offset += img.width
        
        for item in predictions:
            img_name = 'images/' + item + '.png'
            img = Image.open(img_name)
            img = img.resize((100, 100))
            new_im.paste(img, (offset, 0))
            offset += img.width

        # add row to infographic
        if combine:
            infographic.paste(new_im, (0, graphic_offset))
            graphic_offset += new_im.height
        else:
            new_im_name = 'preds/' + person + '_' + df_type + 'preds.png'
            new_im.save(new_im_name)
    if combine:
        infoname = 'preds/' + df_type + '_preds.png'
        infographic.save(infoname)

def main():

    # args
    args = parse_args()

    # read in predictions file
    df = pd.read_excel("Preseason Predictions! (Responses).xlsx")

    # hardcoded correct names
    # df.at[0, 'Name:'] = 'jonah'
    # df.at[1, 'Name:'] = 'helena'
    # df.at[2, 'Name:'] = 'david'


    # get drivers and/or teams dataframes
    drivers_df = get_df(df, 'drivers')
    teams_df = get_df(df, 'teams')

    # define entries and check subset
    rows = teams_df.index
    if args.subset != 'all':
        rows = args.subset.split(' ')
        # check subset
        for row in rows:
            if row not in teams_df.index:
                raise Exception("who is {}".format(row))
    if TEST:
        rows = ['jonah'] # for testing

    # make infographics for teams
    if args.groups == 'teams' or 'both':
        # make teams infographic
        make_infographic(teams_df, args.not_combine, 'teams', rows)


    # make infographics for drivers
    if args.groups == 'drivers' or 'both':
        # make drivers infographic
        make_infographic(drivers_df, args.not_combine, 'drivers', rows)

if __name__ == '__main__':
    main()