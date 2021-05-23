import pandas as pd

# 你需要创建一个数据集把本地预测的submission.csv导入进来。
result = pd.read_csv('../input/yourdataset/submission.csv'); result.head()

submission = pd.read_csv('../input/hpa-single-cell-image-classification/sample_submission.csv'); submission.head()

for idx in tqdm(range(len(result))):
    
    ID = result.loc[idx]['ID']
    PS = result.loc[idx]['PredictionString']
    
    act_id = np.where(submission['ID'] == ID)[0][0]
    
    submission.loc[act_id, 'PredictionString'] = PS

submission.to_csv('submission.csv', index=False)