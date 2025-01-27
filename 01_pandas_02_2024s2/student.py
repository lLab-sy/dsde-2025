import pandas as pd
import json

"""
    ASSIGNMENT 1 (STUDENT VERSION):
    Using pandas to explore youtube trending data from GB (GBvideos.csv and GB_category_id.json) and answer the questions.
"""

video_path = '/data/GBvideos.csv'
# video_path = '01_pandas_02_2024s2/USvideos.csv'

def drop_dup(df: pd.DataFrame):
    return df.drop_duplicates()

def Q1():
    """
        1. How many rows are there in the GBvideos.csv after removing duplications?
        - To access 'GBvideos.csv', use the path '/data/GBvideos.csv'.
    """
    # TODO: Paste your code here
    df_video = pd.read_csv(video_path)
    return drop_dup(df_video).shape[0]

def Q2(vdo_df):
    '''
        2. How many VDO that have "dislikes" more than "likes"? Make sure that you count only unique title!
            - GBvideos.csv has been loaded into memory and is ready to be utilized as vdo_df
            - The duplicate rows of vdo_df have been removed.
    '''
    # TODO: Paste your code here
    unq_df = drop_dup(vdo_df)
    return unq_df[unq_df['dislikes'] > unq_df['likes']]['title'].unique().size

def Q3(vdo_df):
    '''
        3. How many VDO that are trending on 22 Jan 2018 with comments more than 10,000 comments?
            - GBvideos.csv has been loaded into memory and is ready to be utilized as vdo_df
            - The duplicate rows of vdo_df have been removed.
            - The trending date of vdo_df is represented as 'YY.DD.MM'. For example, January 22, 2018, is represented as '18.22.01'.
    '''
    # TODO: Paste your code here
    unq_df = drop_dup(vdo_df)
    return ((unq_df['trending_date'] == '18.22.01') & (unq_df['comment_count'] > 10000)).sum()

def Q4(vdo_df):
    '''
        4. Which trending date that has the minimum average number of comments per VDO?
            - GBvideos.csv has been loaded into memory and is ready to be utilized as vdo_df
            - The duplicate rows of vdo_df have been removed.
    '''
    # TODO:  Paste your code here
    unq_df = drop_dup(vdo_df)
    avg_df = (unq_df.groupby('trending_date'))['comment_count'].mean().reset_index()
    return avg_df.loc[avg_df['comment_count'].idxmin()]['trending_date']

def Q5(vdo_df):
    '''
        5. Compare "Sports" and "Comedy", how many days that there are more total daily views of VDO in "Sports" category than in "Comedy" category?
            - GBvideos.csv has been loaded into memory and is ready to be utilized as vdo_df
            - The duplicate rows of vdo_df have been removed.
            - You must load the additional data from 'GB_category_id.json' into memory before executing any operations.
            - To access 'GB_category_id.json', use the path '/data/GB_category_id.json'.
    '''
    # TODO:  Paste your code here
    json_path = '/data/GB_category_id.json'
    # json_path = '01_pandas_02_2024s2/US_category_id.json'
    with open(json_path, 'r') as file:
        data = json.load(file)
    cate_map = {int(cate['id']) : cate['snippet']['title'] for cate in data['items']}

    unq_df = drop_dup(vdo_df)
    unq_df['category'] = unq_df['category_id'].map(cate_map)
    # daily
    total_view_df = unq_df.groupby(['trending_date', 'category'])['views'].sum().reset_index()
    sport_df = total_view_df[total_view_df['category'] == 'Sports'][['trending_date', 'views']].rename(columns={'views': 'sport_views'})
    comedy_df = total_view_df[total_view_df['category'] == 'Comedy'][['trending_date', 'views']].rename(columns={'views': 'comedy_views'})
    
    daily_df = pd.merge(sport_df, comedy_df, on='trending_date', how='inner')
    return (daily_df['sport_views'] > daily_df['comedy_views']).sum()

# video_path = '/data/GBvideos.csv'
# video_path = '01_pandas_02_2024s2/USvideos.csv'

# df_video = pd.read_csv(video_path)

# inp = input()

# match inp:
#     case 'Q1':
#         print(Q1())
#     case 'Q2':
#         print(Q2(df_video))
#     case 'Q3':
#         print(Q3(df_video))
#     case 'Q4':
#         print(Q4(df_video))
#     case 'Q5':
#         print(Q5(df_video))
    


