import os
import docx2txt
import pandas as pd
from glob import glob


class ExtractICTRoles:
    def __init__(self, docx_folder, ict_roles_path):
        self.docx_folder = docx_folder
        self.ict_roles_path = ict_roles_path

        self.df = None

    def run(self):
        files = self.collect_docx()
        self.docx_to_txt(files)
        self.df.to_csv(self.ict_roles_path, index=False)

    def collect_docx(self):
        # collect a list of docx documents filepaths
        files = list(set([y for x in os.walk(self.docx_folder) for y in glob(os.path.join(x[0], '*.docx'))]))
        return files

    def docx_to_txt(self, files):
        # convert each docx file to a txt file
        tracks, subtracks, occs, titles, descs = [[] for _ in range(5)]
        for i in files:
            txt = docx2txt.process(i)
            track, subtrack, occ, title, desc = self.process_txt(txt)

            # exclude CTO/CIO and some roles
            if 'Chief' not in title:
                tracks.append(track)
                subtracks.append(subtrack)
                occs.append(occ)
                titles.append(title)
                descs.append(desc)

        # compile into 1 df
        self.df = pd.DataFrame(
            data={'track': tracks, 'subtrack': subtracks, 'occupation': occs, 'job_role': titles,
                  'job_role_description': descs})
        self.df.sort_values(by=['track', 'subtrack', 'job_role'], ascending=True, inplace=True)

        # drop sales and marketing roles
        self.df = self.df[self.df['track'] != 'Sales and Marketing']

    def process_txt(self, txt):
        # role track
        track = None
        track_txt = txt.split('Track\n\n', 1)
        if len(track_txt) > 1:
            track = track_txt[1].split('\n')[0].strip()

        # role sub-track
        subtrack = None
        subtrack_txt = txt.split('Sub-track\n\n', 1)
        if len(subtrack_txt) > 1:
            subtrack = subtrack_txt[1].split('\n')[0].strip()
        else:
            subtrack_txt = txt.split('Sub-Track\n\n', 1)
            if len(subtrack_txt) > 1:
                subtrack = subtrack_txt[1].split('\n')[0].strip()

        # clean associate systems support engineer
        subtrack = 'Systems Support' if track == 'Systems Support' else subtrack
        track = 'Operations and Support' if track == 'Systems Support' else track

        # occupation group
        occ = None
        occ_txt = txt.split('Occupation\n\n', 1)
        if len(occ_txt) > 1:
            occ = occ_txt[1].split('\n')[0].strip()
        occ = occ.replace('Infocomm Technology', 'ICT')

        # role title
        sentences = txt.split('\n')
        title = sentences[1].replace('SKILLS MAP – ', '').title()

        # role description
        desc = txt.split('Critical Work Functions')[0].split('Job Role Description')[1].strip()

        return track, subtrack, occ, title, desc
