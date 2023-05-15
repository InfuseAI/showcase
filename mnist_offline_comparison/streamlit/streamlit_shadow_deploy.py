import pandas as pd

import streamlit as st

def main():
    st.set_page_config(page_title="MNIST shadow deployment", page_icon=":pencil2:", layout="wide")

    st.title('MNIST shadow deployment')
    
    st.header("Prediction Result: ")
    df = pd.read_csv("./result/shadow_deployment_result.csv")
    st.dataframe(df)
    
    st.header("Metrics: ")

    # 計算相同accuracy
    acc_list = []
    for i in range(2, len(df)+1):
        acc = (df.iloc[:, 0] == df.iloc[:, i]).mean()
        acc_list.append(acc)

    # 創建新表格
    new_data = {
        'column': list(df.columns)[2:],
        'accuracy': acc_list
    }

    new_df = pd.DataFrame(new_data)

    st.dataframe(new_df)

if __name__ == "__main__":
    main()