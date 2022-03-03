import pandas as pd


class ProcessICTJobs:
    def __init__(self, ict_roles_filepath, role_ssoc_mapping_filepath):
        self.ict_roles_filepath = ict_roles_filepath
        self.role_ssoc_mapping_filepath = role_ssoc_mapping_filepath

    def run(self):
        ict_roles, mapping = self.read_data()
        mapping = self.clean_role_ssoc_mapping(mapping)
        ict_roles = self.clean_roles(ict_roles)

        df = self.map_role_to_ssoc(ict_roles, mapping)
        df.to_csv(self.ict_roles_filepath, index=False)

    def read_data(self):
        # read ICT roles
        ict_roles = pd.read_csv(self.ict_roles_filepath)

        # read DOS SFw role to SSOC mapping
        mapping = pd.read_excel(self.role_ssoc_mapping_filepath, skiprows=7)

        return ict_roles, mapping

    def clean_role_ssoc_mapping(self, mapping):
        # filter to SFw ICT roles
        exceptions = ['Network engineer', 'Radio frequency engineer', 'Automation engineer', 'Applications programmer',
                      'Systems engineer (computer)', 'Software engineer', 'Artificial intelligence (AI) engineer']
        mapping = mapping[
            (mapping['SSOC 2020 Alphabetical Index Description'].str.contains('SFw-Infocomm Technology')) |
            (mapping['SSOC 2020 Alphabetical Index Description'].isin(exceptions))]

        # clean occupation titles
        mapping['job_title'] = mapping['SSOC 2020 Alphabetical Index Description'].apply(
            lambda x: x.replace('(SFw-Infocomm Technology)', '').lower().split('/'))
        mapping = mapping.explode('job_title')

        # remove anything in brackets
        mapping['job_title'] = mapping['job_title'].apply(lambda x: x.replace('(ai) ', '').split('(')[0].strip())

        # clean
        mapping = mapping[['SSOC 2020 Alphabetical Index Description', 'job_title', 'SSOC 2020']]

        return mapping

    def clean_roles(self, ict_roles):
        # clean job roles
        ict_roles['job_title'] = ict_roles['job_role'].apply(lambda x: x.split('/'))
        ict_roles = ict_roles.explode('job_title')

        # manual cleaning
        ict_roles['job_title'] = ict_roles['job_title'].apply(self.map_job_title)
        ict_roles['job_title'] = ict_roles['job_title'].str.lower()

        return ict_roles

    def map_job_title(self, title):
        # manual mapping
        if title == 'Artificial Intelligence':
            title = 'Artificial Intelligence Engineer'
        elif title == 'Senior Artificial Intelligence':
            title = 'Artificial Intelligence Engineer'
        elif 'Forensics' in title:
            title = title.replace('Forensics', 'Forensic')
        elif title == 'Security Architect':
            title = title.replace('Security', 'Principal Security')
        elif title == 'Senior Security Engineer':
            title = title.replace('Senior ', '')
        elif title == 'Vulnerability Assessment And Penetration Testing Analyst':
            title = 'Security Penetration Tester'
        elif title == 'Vulnerability Assessment And Penetration Testing Manager':
            title = 'Security Penetration Testing Manager'
        elif title == 'Threat Analysis Manager':
            title = 'Threat Investigation Manager'
        elif title == 'Artificial Intelligence Applied Researcher':
            title = 'Data Scientist'
        elif title == 'Data Architect':
            title = 'Data Engineer'
        elif 'Machine Learning Engineer' in title:
            title = title.replace('Machine Learning', 'Artificial Intelligence')
        elif title == 'Associate Infrastructure Engineer':
            title = title.replace('Associate ', '')
        elif title == 'Associate Network Engineer':
            title = title.replace('Associate ', '')
        elif title == 'Associate Radio Frequency Engineer':
            title = title.replace('Associate ', '')
        elif title == 'Automation And Orchestration Engineer':
            title = 'Automation Engineer'
        elif title == 'Infrastructure Engineering Manager':
            title = 'Infrastructure Manager'
        elif title == 'Infrastructure Architect':
            title = 'Senior Infrastructure Architect'
        elif 'Applications Support Engineer' in title:
            title = 'Applications programmer'
        elif 'Data Centre Operations Engineer' in title:
            title = 'Data Centre Engineer'
        elif 'Operations Centre Support Engineer' in title:
            title = 'Infrastructure Engineer'
        elif 'Database Support Engineer' in title:
            title = 'Data Engineer'
        elif 'Infrastructure Support Engineer' in title:
            title = 'Infrastructure Engineer'
        elif title == 'Associate Embedded Systems Engineer':
            title = title.replace('Associate ', '')
        elif 'Systems Support Engineer' in title:
            title = 'Systems Engineer'
        elif title == 'Software Architect':
            title = 'Applications Architect'
        elif title == 'Associate Software Engineer':
            title = title.replace('Associate ', '')
        elif title == 'Devops Engineer':
            title = 'Applications Developer'
        elif title == 'Software Engineering Manager':
            title = 'Software Engineer'
        elif title == 'Associate Ui Designer':
            title = title.replace('Associate ', '')
        elif title == 'Business Architect':
            title = 'Business Analyst'
        elif title == 'Solutions Architect':
            title = 'Principal Solutions Architect'
        elif title == 'Head Of It Audit':
            title = 'IT Audit Manager'
        elif title == 'Associate Ux Designer':
            title = title.replace('Associate ', '')
        elif title == 'Project Manager':
            title = 'Product Manager'
        elif title == 'Head of Quality':
            title = 'Quality Manager'
        elif title == 'Quality Assurance Engineer':
            title = 'Software Quality Assurance Engineer'
        elif title == 'Quality Assurance Manager':
            title = 'Software Quality Assurance Manager'
        elif title == 'Quality Engineering Manager':
            title = 'Software Quality Assurance Manager'
        elif title == 'Associate Data Engineer':
            title = title.replace('Associate ', '')
        elif title == 'Artificial Intelligence Scientist':
            title = 'Data Scientist'
        elif title == 'Head Of Data Science And Artificial Intelligence':
            title = 'Chief Data Scientist'
        elif title == 'Sysops Engineer':
            title = 'Infrastructure Engineer'
        elif title == 'Head Of Operations And Support':
            title = 'Head of Infrastructure'
        elif title == 'Operations And Support Manager':
            title = 'Infrastructure Manager'
        elif title == 'Head of Software Engineering':
            title = 'Head of Applications Development'
        elif title == 'Head Of Quality':
            title = 'Quality Manager'

        return title

    def map_role_to_ssoc(self, ict_roles, mapping):
        # for each ICT job role, match to an SSOC5D
        df = ict_roles.merge(mapping, on=['job_title'], how='left')
        df['SSOC 2020'].fillna('0', inplace=True)
        df = df.groupby(['track', 'subtrack', 'occupation', 'job_role', 'job_role_description'])[
            'SSOC 2020'].unique().reset_index()
        df['SSOC 2020'] = df['SSOC 2020'].apply(list)

        return df
