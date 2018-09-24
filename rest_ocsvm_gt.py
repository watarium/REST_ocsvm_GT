from sklearn.externals import joblib
import pandas as pd
import numpy as np
import urllib.parse
from flask import Flask, jsonify, request
app = Flask(__name__)

clf = joblib.load('ocsvm_gt.pkl')
base_dummies = pd.read_csv('data_dummies.csv')


# If you run this code on the other computer, you might need to remove commentout below.
# Sometimes mode.predict function does not load correctly.
# import numpy as ap
# X = np.zeros((10, max_len))
# model.predict(X, batch_size=32)


@app.route('/preds', methods=['POST'])
def preds():
    # loading
    response = jsonify()
    new_data = []
    new_data.append(request.form['date'])
    new_data.append('account_' + request.form['account'])
    new_data.append('ip_' + request.form['ip'])
    new_data.append('service_' + request.form['service'])
    new_data.append('process_' + request.form['process'])
    new_data.append('objectname_' + request.form['objectname'])
    new_data.append('sharedname_' + request.form['sharedname'])

    base_df = pd.DataFrame(columns=base_dummies.columns[2:-3])
    base_df.loc[0] = 0

    for colname in new_data:
         if colname in base_df.columns:
             base_df[colname][0] = 1
    base_df['eventID'][0] = request.form['event_id']
    base_df = base_df.astype(np.int32)


    pred_data = base_df.values

    result = clf.predict(pred_data)
    if result == 1:
        print('normal')
        response.status_code = 201
    elif result == -1:
        print('outlier')
        response.status_code = 202

    # save
    # with open('request.log', mode='a') as f:
    #     f.write(str(response.status_code) + str(prediction) + ',' + str(reqstr) + '\n')

    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0')
