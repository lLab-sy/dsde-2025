"""
Question 1 basic pandas
"""
import pandas as pd

def main():
    """
    main solver
    """
    file = input()
    func = input()

    df = pd.read_csv(file)

    if func == 'Q1':
        # Do something
        print(df.shape)
    elif func == 'Q2':
        # Do something
        print(df['score'].max())
    elif func == 'Q3':
        # Do something
        print((df['score'] >= 80).sum())
    else:
        # Do something
        print('No Output')

if __name__ == "__main__":
    main()