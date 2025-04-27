import pandas as pd
df = pd.read_csv("data/product_df.csv")
matches = df[(df['MATL_FORM']=='TUBE') & (df['SHAPE']=='SQUARE') & (df['WALL_1']==0.25) & (df['SIDE_1']==3.0)]
print(matches[['SKU','SKU_DESC','GRADE','MATL_LENGTH_TYPE','LGTH_NOM','LGTH_NOM_UNIT','TYPE']].to_dict(orient='records'))