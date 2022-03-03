import os
import pandas as pd
from glob import glob
from docx import Document

import helper


class ExtractICTSkills:
    def __init__(self, docx_folder, ict_skills_path, other_ict_skills_path, sfw_path):
        self.docx_folder = docx_folder
        self.ict_skills_path = ict_skills_path
        self.other_ict_skills_path = other_ict_skills_path
        self.sfw_path = sfw_path

        self.df = pd.DataFrame()

    def run(self):
        # ICT sector skills
        files = self.collect_docx()
        self.docx_to_txt(files)
        self.remove_skills()

        # non-ICT sector digital skills
        self.get_nonict_digital_skills()
        self.df = self.df[self.df['sector'] != 'critical core skills']

        self.df.to_csv(self.ict_skills_path, index=False)

    def get_nonict_digital_skills(self):
        # get non-ICT sector digital skills (identified by yao jun)
        df = pd.read_excel(self.other_ict_skills_path)
        df = df[df['Digital'] == 1]
        df.drop(columns=['Digital', 'proficiency_description', 'skill_id'], inplace=True)
        df.rename(columns={'skill_category': 'tsc_category', 'tsc/ccs_title': 'tsc_title'},
                  inplace=True)

        # get the knowledge and abilities of the tscs
        sfw = pd.read_excel(self.sfw_path, sheet_name='TSC_K&A')
        key_cols = ['Sector', 'Category', 'TSC Title', 'Proficiency Level', 'Proficiency Description']
        sfw = sfw.groupby(key_cols)['Knowledge', 'Ability'].agg(['unique']).reset_index()
        sfw.columns = sfw.columns.droplevel(1)
        sfw.drop_duplicates(subset=key_cols, inplace=True)
        sfw = sfw.applymap(lambda x: x.lower() if type(x) == str else x)
        sfw['Knowledge'] = sfw['Knowledge'].apply(list)
        sfw['Ability'] = sfw['Ability'].apply(list)
        sfw.rename(columns={'Sector': 'sector',
                            'Category': 'tsc_category',
                            'TSC Title': 'tsc_title',
                            'Proficiency Level': 'proficiency_level',
                            'Proficiency Description': 'proficiency_description',
                            'Knowledge': 'knowledge_list',
                            'Ability': 'abilities_list'}, inplace=True)

        df = sfw.merge(df, on=['sector', 'tsc_category', 'tsc_title', 'proficiency_level'], how='right')

        # combine with ICT skills
        self.df = pd.concat([self.df, df], ignore_index=True)

    def collect_docx(self):
        # collect a list of docx documents filepaths
        files = list(set([y for x in os.walk(self.docx_folder) for y in glob(os.path.join(x[0], '*.docx'))]))
        return files

    def docx_to_txt(self, files):
        # convert docx table to df
        for i in files:
            doc = Document(i)
            df = self.process_doc(doc)
            self.df = pd.concat([self.df, df], ignore_index=True)

    def process_doc(self, doc):
        # convert to table form
        table = doc.tables[0]

        # tsc category
        row = table.rows[0]
        category = row.cells[1].text.strip()

        # tsc title
        row = table.rows[1]
        tsc = row.cells[1].text.strip()

        # tsc description
        row = table.rows[2]
        desc = row.cells[1].text.strip()

        # tsc proficiency description - level 1
        row = table.rows[5]
        prof1 = row.cells[1].text.strip()
        prof1 = self.split_string(prof1)

        # tsc proficiency description - level 2
        row = table.rows[5]
        prof2 = row.cells[2].text.strip()
        prof2 = self.split_string(prof2)

        # tsc proficiency description - level 3
        row = table.rows[5]
        prof3 = row.cells[3].text.strip()
        prof3 = self.split_string(prof3)

        # tsc proficiency description - level 4
        row = table.rows[5]
        prof4 = row.cells[4].text.strip()
        prof4 = self.split_string(prof4)

        # tsc proficiency description - level 5
        row = table.rows[5]
        prof5 = row.cells[5].text.strip()
        prof5 = self.split_string(prof5)

        # tsc proficiency description - level 6
        row = table.rows[5]
        prof6 = row.cells[6].text.strip()
        prof6 = self.split_string(prof6)

        # knowledge list - level 1
        row = table.rows[6]
        know1 = row.cells[1].text.strip()
        know1 = self.split_string(know1)

        # knowledge list - level 2
        row = table.rows[6]
        know2 = row.cells[2].text.strip()
        know2 = self.split_string(know2)

        # knowledge list - level 3
        row = table.rows[6]
        know3 = row.cells[3].text.strip()
        know3 = self.split_string(know3)

        # knowledge list - level 4
        row = table.rows[6]
        know4 = row.cells[4].text.strip()
        know4 = self.split_string(know4)

        # knowledge list - level 5
        row = table.rows[6]
        know5 = row.cells[5].text.strip()
        know5 = self.split_string(know5)

        # knowledge list - level 6
        row = table.rows[6]
        know6 = row.cells[6].text.strip()
        know6 = self.split_string(know6)

        # abilities list - level 1
        row = table.rows[7]
        ab1 = row.cells[1].text.strip()
        ab1 = self.split_string(ab1)

        # abilities list - level 2
        row = table.rows[7]
        ab2 = row.cells[2].text.strip()
        ab2 = self.split_string(ab2)

        # abilities list - level 3
        row = table.rows[7]
        ab3 = row.cells[3].text.strip()
        ab3 = self.split_string(ab3)

        # abilities list - level 4
        row = table.rows[7]
        ab4 = row.cells[4].text.strip()
        ab4 = self.split_string(ab4)

        # abilities list - level 5
        row = table.rows[7]
        ab5 = row.cells[5].text.strip()
        ab5 = self.split_string(ab5)

        # abilities list - level 6
        row = table.rows[7]
        ab6 = row.cells[6].text.strip()
        ab6 = self.split_string(ab6)

        # compile and clean
        df = pd.DataFrame(data={'tsc_category': category,
                                'tsc_title': tsc,
                                'tsc_description': desc,
                                'sector': 'infocomm technology',
                                'proficiency_level': list(range(1, 7)),
                                'proficiency_description': [prof1, prof2, prof3, prof4, prof5, prof6],
                                'knowledge_list': [know1, know2, know3, know4, know5, know6],
                                'abilities_list': [ab1, ab2, ab3, ab4, ab5, ab6]
                                })

        df = df[df['proficiency_description'] != '']

        return df

    def remove_skills(self):
        # remove some ICT sector skills
        self.df = helper.get_ict_skills(self.df)

    def split_string(self, string):
        if len(string) > 0:
            string = [x.strip() for x in string.split('\n')]

        return string
