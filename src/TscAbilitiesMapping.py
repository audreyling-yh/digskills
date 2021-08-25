import pandas as pd
import ast

tsc=pd.read_csv('../data/ssg/link_tsc_to_items.csv')
tsc['abilities_id']=tsc['abilities_id'].apply(lambda x: ast.literal_eval(x))

# Check across the 7 tracks under ICT Skills Framework
ict_skills=pd.read_csv('../data/ict_tsc.csv')
ict_skills['abilities_id']=ict_skills['abilities_id'].apply(lambda x: ast.literal_eval(x))
ict_ex=ict_skills.explode('abilities_id')
ict_ab=ict_ex.groupby(['abilities_id'])['track'].nunique().reset_index()
ict_ab[ict_ab['track']>1] # 1062 abilities belong to more than 1 ICT track


# Check which abilities belong to both ICT and non-ICT TSCs
ict_skills['tsc_prof']=list(zip(ict_skills['tsc_id'],ict_skills['proficiency_level']))
ict_prof_list=list(set(ict_skills['tsc_prof']))

tsc['tsc_prof']=list(zip(tsc['tsc_id'],tsc['proficiency_level']))
tsc_prof_list=tsc['tsc_prof'].tolist()

ict_bool=[(True if x in ict_prof_list else False) for x in tsc_prof_list]
tsc['digital']=ict_bool

# Check which abilities belong to both digital and non-digital TSCs
tsc_exp=tsc.explode('abilities_id')
ab=pd.pivot_table(tsc_exp,
                  index=['abilities_id'],
                  values=['tsc_id','sector','digital'],
                  aggfunc=[lambda x: len(x.unique()),list])
ab.columns=ab.columns.droplevel(0)
ab.reset_index(inplace=True)

ab.columns=['abilities_id',
            'nunique_digital',
            'nunique_sector',
            'nunique_tsc_id',
            'digital',
            'sector',
            'tsc_id'
            ]

# Check which abilities belong to more than 1 TSC
ab['tsc_bool']=ab['nunique_tsc_id']>1 #true if ability belongs to more than 1 tsc
ab_tsc=ab[ab['tsc_bool']] #filter to include abilities that belong to more than 1 tsc
ab_tsc[['abilities_id','sector','tsc_id']]

# Check which abilities belong to more than 1 sector
ab['sector_bool']=ab['nunique_sector']>1 #true if ability belongs to more than 1 tsc
ab_sec=ab[ab['sector_bool']] #filter to include abilities that belong to more than 1 tsc
ab_sec[['abilities_id','sector','tsc_id']]

# Check which abilities belong to more than 1 sector
ab['digital_bool']=ab['nunique_digital']>1 #true if ability belongs to more than 1 tsc
ab_sec=ab[ab['digital_bool']] #filter to include abilities that belong to more than 1 tsc
ab_sec[['abilities_id','nunique_digital','digital']] #742 abilities belong to both digital and non-digital TSCs